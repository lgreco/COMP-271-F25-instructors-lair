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
        writer.writerow(["timestamp", "name", "UVID", 'num_tests', 'tests_failed', 'score', 'total'])


def pytest_sessionfinish(session, exitstatus):
    print(f"\nGrades written to {GRADE_FILE.resolve()}")


def parse_error_msg(error: str):
    """
    Parse the AssertionError on test case fails and return only the part about Expected and Actual Outputs
    """
    if not error:
        return ""
    ix = error.find('assert')
    if ix != -1:
        line = error[:ix]
    else:
        line = error

    indentation = '  '
    return textwrap.indent(line.strip(), indentation)


# Hook: collect results after each test module (i.e., per student)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    g = config._grading
    name = config.getoption("--name")
    uvid = config.getoption("--UVID")

    # Primary logic using our custom grading hook
    if g['details']:
        total_tests = len(g['details'])
        tests_passed = len([1 for testcase in g['details'] if testcase['passed']])
        earned_score = g["earned"]
        total_score = g["total"]
    # Fallback logic for when no tests ran (e.g., collection error)
    else:
        # Robustly count total tests by summing all outcomes from the stats object
        total_tests = sum(len(v) for v in terminalreporter.stats.values() if isinstance(v, list))
        tests_passed = 0
        if 'passed' in terminalreporter.stats:
            tests_passed = len(terminalreporter.stats['passed'])

        # If no tests ran, score is 0. Avoids complex and potentially incorrect calculations.
        earned_score = 0
        total_score = 0 # Cannot determine total score if tests did not run to populate g['total']

    tests_failed = total_tests - tests_passed

    terminalreporter.write_sep(
        "=", f"Name: {name!r} UVID: {uvid!r} Score: {earned_score:.3g}/{total_score:.2g}  Tests passed: {tests_passed}/{total_tests}"
    )

    payload = {
        "name": name,
        "UVID": uvid,
        "earned": earned_score,
        "total": total_score,
        "details": g["details"],
    }

    # Ensure the output directory exists
    output_dir = Path("./graded_submissions")
    output_dir.mkdir(exist_ok=True)

    # write JSON
    json_path = output_dir / f'{uvid}_results.json'
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    # write feedback based on failed test cases
    feedback_path = output_dir / f"{uvid}_feedback.txt"
    feedback_list = [
        f'Coding score: {payload["earned"]:.3g}/{payload["total"]:.3g}',
    ]

    if not g['details'] and total_tests == 0:
        feedback_list.append("\nNo tests were run. This may be due to a syntax error in the submission file or an issue with the test setup.")
    else:
        failed_tests = [tc for tc in g['details'] if not tc['passed']]
        if failed_tests:
            feedback_list.append('Deductions:')
            for test_case in failed_tests:
                feedback_list.extend([
                    f'* Failed {test_case["nodeid"].split("::")[-1]!r} (-{test_case["points"]:.3g} points)',
                    parse_error_msg(test_case["error"]),
                ])
        else:
            feedback_list.append('Well done! All tests passed.')

    with open(feedback_path, "w") as f:
        f.write('\n'.join(feedback_list))

    with GRADE_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.ctime(), name, uvid, total_tests, tests_failed, earned_score, total_score])


# This function is not standard in conftest and may not be picked up by pytest.
# It's better to check syntax inside the fixture that loads the module.
# def test_syntax(student_file):
#     src = open(student_file).read()
#     try:
#         ast.parse(src, filename=student_file)
#     except SyntaxError as e:
#         pytest.fail(f"Syntax error in {student_file} at line {e.lineno}: {e.msg}")


# Helper function to load student code
def load_student_module(path_to_file: Path):
    """Dynamically loads a Python file as a module, handling import/syntax errors."""
    if not path_to_file.exists():
        pytest.fail(f"Required file not found: {path_to_file}")

    module_name = path_to_file.stem
    try:
        # Check for syntax errors before trying to import
        with open(path_to_file, 'r') as f:
            ast.parse(f.read(), filename=str(path_to_file))

        spec = spec_from_file_location(module_name, str(path_to_file))
        if spec is None:
            pytest.fail(f"Could not create module spec for {path_to_file}")
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (SyntaxError, IndentationError) as e:
        pytest.fail(f"Student submission '{path_to_file.name}' has a Syntax Error: {type(e).__name__}: {e.msg} at line {e.lineno}")
    except ImportError as e:
        pytest.fail(f"Student submission '{path_to_file.name}' has an Import Error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during import of '{path_to_file.name}': {type(e).__name__}: {e}")
    return None


# In conftest.py


@pytest.fixture(scope="session")
def student_module(request):
    """Import the student's midterm.py file as a module."""
    uvid = request.config.getoption("--UVID")
    if not uvid:
        pytest.fail("A student --UVID must be provided to run the grading script.")

    file_path = Path("./graded_submissions") / f"{uvid}_Midterm.py"

    # <<< SET YOUR BREAKPOINT ON THE LINE BELOW
    return load_student_module(file_path)


@pytest.fixture(scope="session")
def My2DQueue_class(student_module):
    """Provides the TwoDimensionalQ class from the student's module."""
    if not hasattr(student_module, 'TwoDimensionalQ'):
        pytest.fail("Student file is missing the required class 'TwoDimensionalQ'.")
    return getattr(student_module, 'TwoDimensionalQ')


@pytest.fixture
def empty_q_2x2(My2DQueue_class): # Corrected fixture name used here
    """Provides an empty 2x2 queue."""
    return My2DQueue_class(n=2)