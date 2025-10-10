import ast
import csv
import importlib.util
import json
import os
import pathlib
import sys
import builtins
import textwrap
from itertools import chain

import pytest
import uuid
import time
from loguru import logger

#
#
# logger.remove()  # Remove the default handler.
# logger.add(
#     sys.stdout, level="INFO"
# )  # Log only messages with level "WARNING" or higher.

# Path for grade report
GRADE_FILE = pathlib.Path("grades.csv")


# ----------------------------------------------------
# Fixture to load a student's module dynamically
# ----------------------------------------------------
@pytest.fixture
def student_module(request):
    """
    Import the student's Python file as a module.
    """
    path = request.config.getoption("--input")
    if not path:
        pytest.skip("No --student-file provided. Use: pytest --student-file=path/to/submission.py")
    if not os.path.exists(path):
        pytest.skip(f"Student file not found: {path}")
    return load_student_module(path)

"""
file_path = pathlib.Path("student.py")
if not file_path.exists():
    pytest.fail("student.py not found in working directory")

spec = importlib.util.spec_from_file_location("student", file_path)
module = importlib.util.module_from_spec(spec)
sys.modules["student"] = module
spec.loader.exec_module(module)
return module
"""
# ----------------------------------------------------
# Fixture to monkeypatch input() with predefined values
# ----------------------------------------------------
@pytest.fixture
def fake_inputs(monkeypatch):
    """
    Feed predefined inputs to student's code that calls input().
    Usage: fake_inputs(["1","2","3"])
    """
    def _feed(inputs):
        it = iter(inputs)
        monkeypatch.setattr(
            builtins, "input",
            lambda prompt=None: next(it)
        )
    return _feed


def load_student_module(path):
    """Load student's .py into a uniquely named module to avoid caching issues."""
    # try:
    test_syntax(path)
    # except SyntaxError:
    #     logger.error(f"Syntax error for {path.stem!r}")


    spec = importlib.util.spec_from_file_location(f"student_{uuid.uuid4().hex}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

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



def parse_error_msg(error: str):
    """
    Parse the AssertionError on test case fails and return only the part about Expected and Actual Outputs
    """
    end_ix_act = error.find('assert')
    line = error[: end_ix_act].strip()
    indentation = '  '
    return textwrap.indent(line, indentation)

# Hook: collect results after each test module (i.e., per student)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    results = {}
    g = config._grading
    name = config.getoption("--name")
    uvid = config.getoption("--UVID")


    # Write per-student summary
    if 'passed' not in terminalreporter.stats:
        terminalreporter.stats['passed'] = []
    if 'failed' not in terminalreporter.stats:
        terminalreporter.stats['failed'] = []
    if 'error' not in terminalreporter.stats:
        terminalreporter.stats['error'] = []
    total_tests = len(terminalreporter.stats["passed"]) + len(
        terminalreporter.stats["failed"]) + len(terminalreporter.stats["error"])

    tests_passed = len(terminalreporter.stats["passed"])
    total_score = sum(
        t.keywords["points"]
        for t in chain(
            terminalreporter.stats["passed"], terminalreporter.stats["failed"], terminalreporter.stats["error"]
        )
    )
    earned_score = sum(
        t.keywords["points"]
        for t in terminalreporter.stats["passed"]
    )

    tests_failed = total_tests - tests_passed

    terminalreporter.write_sep(
        "=", f"Name: {name!r} UVID: {uvid!r} Score: {earned_score}/{total_score}  Tests passed: {tests_passed}/{total_tests}"
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
        f'Coding score: {payload["earned"]}/{payload["total"]}',
    ]  # list of lines of feedback

    for test_case in g['details']:
        if test_case['passed']:
            continue
        feedback_list.extend([
            f'* Failed {test_case["nodeid"].split("::")[-1]!r} (-{test_case["points"]:.1g} point)',
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

    parser.addoption(
        "--input",
        action="store",
        default=None,
        help="Path to student's submission (.py).",
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

def test_syntax(student_file):
    src = open(student_file).read()
    try:
        ast.parse(src, filename=student_file)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {student_file} at line {e.lineno}: {e.msg}")