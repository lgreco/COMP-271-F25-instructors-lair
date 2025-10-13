import ast
import csv
import json
import pathlib
import textwrap

import pytest
import time
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

# Path for grade report
GRADE_FILE = pathlib.Path("grades.csv")


# ---------------------------------------------------------------
def _points_from_item(item):
    # Accept both @pytest.mark.points(5) and @pytest.mark.points(value=5)
    marker = item.get_closest_marker("points")
    if marker is None:
        return 0
    if marker.args:
        try:
            return float(marker.args[0])
        except Exception:
            return 0
    return float(marker.kwargs.get("value", 0))


def pytest_configure(config):
    # store running totals and details on config so plugin is stateless across tests
    if not hasattr(config, "_grading"):
        config._grading = {"total": 0, "earned": 0, "details": []}


def pytest_runtest_makereport(item, call):
    # called for setup/call/teardown; we only care about the 'call' phase (the test run)
    if call.when != "call":
        return
    cfg = item.config
    passed = call.excinfo is None
    pts = _points_from_item(item)
    cfg._grading["total"] += pts
    if passed:
        cfg._grading["earned"] += pts

    if passed:
        error_msg = None
    else:
        error_msg = str(call.excinfo.value)
    cfg._grading["details"].append(
        {
            "nodeid": item.nodeid,
            # "name": item.name,
            "points": pts,
            "passed": passed,
            "error": error_msg,
        }
    )


def pytest_addoption(parser):
    parser.addoption(
        "--name",
        action="store",
        type=str,
        default=None,
        help="Student name",
    )

    parser.addoption(
        "--UVID",
        action="store",
        type=str,
        default=None,
        help="Student UVID",
    )

    return

def pytest_sessionstart(session):
    # Initialize CSV file at start
    with GRADE_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        # time.ctime(), name, uvid, tests, tests_failed, earned_score, total_score
        writer.writerow(["timestamp", "name", "UVID", 'num_tests', 'tests_failed', 'score', 'total'])

def pytest_sessionfinish(session, exitstatus):
    print(f"\nGrades written to {GRADE_FILE.resolve()}")


def parse_error_msg(error: str):
    """
    Parse the AssertionError on test case fails and return only the part about Expected and Actual Outputs
    """
    ix = error.find('assert')
    if ix != -1:
        line = error[:ix]
    else:
        line = error

    indentation = '  '
    return textwrap.indent(line.strip(), indentation)


# Hook: collect results after each test module (i.e., per student)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    results = {}
    g = config._grading
    name = config.getoption("--name")
    uvid = config.getoption("--UVID")


    # Write per-student summary
    total_tests = len(g['details'])

    if total_tests == 0:
        # test the config.stats dict
        total_tests = len(terminalreporter.stats[''])
        tests_passed = 0
        total_score = sum(t.keywords['points'] for t in terminalreporter.stats['error'])
        earned_score = 0
    else:
        tests_passed = len([1 for testcase in g['details'] if testcase['passed']])
        earned_score = g["earned"]
        total_score = g["total"]

    tests_failed = total_tests - tests_passed

    terminalreporter.write_sep(
        "=", f"Name: {name!r} UVID: {uvid!r} Score: {earned_score:.2g}/{total_score:.2g}  Tests passed: {tests_passed}/{total_tests}"
    )

    payload = {
        "name": name,
        "UVID": uvid,
        "earned": earned_score,
        "total": total_score,
        "details": g["details"],
    }

    # write JSON
    json_path = f'./graded_submissions/{uvid}_results.json'
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    # write feedback based on failed test cases
    feedback_path = f"./graded_submissions/{uvid}_feedback.txt"
    feedback_list = [
        f'Coding score: {payload["earned"]:.2g}/{payload["total"]:.2g}',
    ]  # list of lines of feedback

    for test_case in g['details']:
        if test_case['passed']:
            continue
        feedback_list.extend([
            f'* Failed {test_case["nodeid"].split("::")[-1]!r} (-{test_case["points"]:.2g} points)',
            parse_error_msg(test_case["error"]),
        ])
    if len(feedback_list) > 1:
        feedback_list.insert(1, 'Deductions: ')
    else:
        feedback_list.append('Well done!')

    with open(feedback_path, "w") as f:
        f.write('\n'.join(feedback_list))

    with GRADE_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        # for student, res in results.items():
        #     score = g['earned']
        # "timestamp", "name", "UVID", 'num_tests', 'tests_failed', 'score', 'total'
        writer.writerow([time.ctime(), name, uvid, total_tests, tests_failed, earned_score, total_score])



def test_syntax(student_file):
    src = open(student_file).read()
    try:
        ast.parse(src, filename=student_file)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {student_file} at line {e.lineno}: {e.msg}")


# Helper function (using Pathlib) - Modified slightly from previous example
def load_student_module(path_to_file: Path):
    """Dynamically loads a Python file as a module, handling import/syntax errors."""
    path_str = str(path_to_file)
    module_name = path_to_file.stem
    try:
        spec = spec_from_file_location(module_name, path_str)
        if spec is None: return None
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (SyntaxError, IndentationError, ImportError) as e:
        pytest.fail(f"Student submission '{path_to_file.name}' has a Syntax or Import Error: {type(e).__name__}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during import of '{path_to_file.name}': {type(e).__name__}: {e}")

    return None

@pytest.fixture(scope="session")
def student_module(request):
    """Import the student's MyList.py file as a module."""
    # Assuming the student submission directory contains MyList.py
    name = request.config.getoption("--name")
    uvid = request.config.getoption("--UVID")

    file_path = Path('./graded_submissions') / f'{uvid}_MyList.py'

    if not file_path.exists():
        pytest.fail(f"Required file '{uvid}_MyList.py' not found in: {str(file_path.parent)}")

    return load_student_module(file_path)

@pytest.fixture(scope="session")
def MyList_class(student_module):
    """Provides the MyList class from the student's module."""
    if not hasattr(student_module, 'MyList'):
        pytest.fail("Student file is missing the required class 'MyList'.")
    return getattr(student_module, 'MyList')

@pytest.fixture
def empty_list(MyList_class):
    """Provides a fresh MyList instance initialized with the default size (4)."""
    try:
        return MyList_class()
    except Exception as e:
        pytest.fail(f"Could not instantiate MyList() with default size. Check __init__: {e}")