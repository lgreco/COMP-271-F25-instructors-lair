import ast
import csv
import json
import pathlib
import textwrap

import pytest
import time
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
#
#
# logger.remove()  # Remove the default handler.
# logger.add(
#     sys.stdout, level="INFO"
# )  # Log only messages with level "WARNING" or higher.

# Path for grade report
GRADE_FILE = pathlib.Path("grades.csv")

#
# # ----------------------------------------------------
# # Fixture to load a student's module dynamically
# # ----------------------------------------------------
# @pytest.fixture
# def student_module(request):
#     """
#     Import the student's Python file as a module.
#     """
#     path = request.config.getoption("--input")
#     if not path:
#         pytest.skip("No --student-file provided. Use: pytest --student-file=path/to/submission.py")
#     if not os.path.exists(path):
#         pytest.skip(f"Student file not found: {path}")
#     return load_student_module(path)
#
# """
# file_path = pathlib.Path("student.py")
# if not file_path.exists():
#     pytest.fail("student.py not found in working directory")
#
# spec = importlib.util.spec_from_file_location("student", file_path)
# module = importlib.util.module_from_spec(spec)
# sys.modules["student"] = module
# spec.loader.exec_module(module)
# return module
# """
#
# def load_student_module(path):
#     """Load student's .py into a uniquely named module to avoid caching issues."""
#     # try:
#     test_syntax(path)
#     # except SyntaxError:
#     #     logger.error(f"Syntax error for {path.stem!r}")
#
#
#     spec = importlib.util.spec_from_file_location(f"student_{uuid.uuid4().hex}", path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#
#     return module

# --- Helper Function (Pathlib-compatible load_student_module) ---
def load_student_module(path_to_file: Path):
    """
    Dynamically loads a Python file as a module.
    Returns the module object on success, or None on Syntax/Import Error.
    """
    path_str = str(path_to_file)
    module_name = path_to_file.stem

    try:
        spec = spec_from_file_location(module_name, path_str)
        if spec is None:
            # Should not happen if file exists, but good practice
            return None

        module = module_from_spec(spec)

        # Crucial step: execution of the module's code happens here
        spec.loader.exec_module(module)

        return module

    # Catching common import errors like SyntaxError and IndentationError
    except (SyntaxError, IndentationError, ImportError) as e:
        # Log the error, but return None to prevent crashing the fixture
        print(
            f"\n--- Autograder Import Error ---\n"
            f"Submission file '{path_to_file.name}' could not be imported due to a syntax error.\n"
            f"Error Details: {type(e).__name__}: {e}"
        )
        return None
    except Exception as e:
        # Catch any other unexpected errors during import/execution
        print(
            f"\n--- Autograder Unexpected Error ---\n"
            f"An unexpected error occurred while importing '{path_to_file.name}'.\n"
            f"Error Details: {type(e).__name__}: {e}"
        )
        return None


# ---------------------------------------------------------------

# ---------------------------------------------------------------


REQUIRED_FILES = ["arya.py", "tyrion.py", "oberyn.py", "brienne.py"]

#
# @pytest.fixture
# def student_modules(request):
#     """
#     Checks for the required submission files using pathlib and imports them as modules.
#     Returns a dictionary of {filename_without_ext: module}.
#     """
#     # 1. Get the submission path and convert it to a Path object
#     submission_dir = Path('./graded_submissions')
#     uvid = request.config.getoption("--UVID")
#     if not submission_dir.is_dir():
#         pytest.skip(f"Submission path is not a directory: {submission_dir}")
#
#     missing_files = []
#     found_modules = {}
#
#     # 2. Check for all required files and load them
#     for filename in REQUIRED_FILES:
#         full_path: Path = submission_dir / f'{uvid}_Inherit_{filename}'  # Clean Path joining
#
#         if not full_path.exists():
#             missing_files.append(filename)
#             continue
#
#         try:
#             # Load the file as a module
#             module = load_student_module(full_path)
#
#             # Store it in the dictionary using the filename stem (e.g., 'Arya')
#             mod_name = full_path.stem.split('_')[-1]
#             found_modules[mod_name] = module
#
#         except Exception as e:
#             pytest.fail(f"Could not load '{filename}'. Check for syntax errors: {e}")
#
#     # 3. Handle missing files
#     if missing_files:
#         missing_list = ", ".join(missing_files)
#         pytest.skip(
#             f"Missing required submission file(s) in '{uvid}': {missing_list}"
#         )
#
#     return found_modules

@pytest.fixture
def student_modules(request):
    """
    Checks for the required submission files and imports them as modules.
    Returns a dictionary of {filename_without_ext: module or FailureReason}.
    """
    # ... (submission_dir setup code) ...
    # 1. Get the submission path and convert it to a Path object
    submission_dir = Path('./graded_submissions')
    uvid = request.config.getoption("--UVID")
    if not submission_dir.is_dir():
        pytest.skip(f"Submission path is not a directory: {submission_dir}")

    missing_files = []
    found_modules = {}

    # 2. Check for all required files and load them
    for filename in REQUIRED_FILES:
        full_path: Path = submission_dir / f'{uvid}_Inherit_{filename}'  # Clean Path joining
        module_name = full_path.stem.split("_")[-1]

        if not full_path.exists():
            missing_files.append(filename)
            # Store a placeholder to indicate the file was missing
            found_modules[module_name] = "FILE_MISSING"
            continue

        module = load_student_module(full_path)

        if module is None:
            # Module load failed due to syntax or other import error
            found_modules[module_name] = "LOAD_FAILED"
        else:
            found_modules[module_name] = module

    # 3. Handle missing files (as before)
    if missing_files:
        missing_list = ", ".join(missing_files)
        # We can still skip if the submission is fundamentally incomplete
        # or handle this in the test functions themselves (recommended).
        # For now, let's keep the skip for fundamental file absence.
        pytest.skip(f"Missing required submission file(s): {missing_list}")

    return found_modules


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
    line = 'Expected: '
    start_ix_exp = error.find('Expected Output:') + len('Expected Output:')
    end_ix_exp = error.find('Actual Output:')
    line = line + error[start_ix_exp: end_ix_exp]
    start_ix_act = error.find('Actual Output:') + len('Actual Output:')
    end_ix_act = error.find('assert')
    line = line + f'\nActual: {error[start_ix_act: end_ix_act]}'
    indentation = ' '
    return textwrap.indent(line, indentation)

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
            f'* Failed {test_case["nodeid"].split("::")[-1]!r} (-{test_case["points"]} points)',
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


# IMPORTANT: Adjusting the character names to match the expected class names
# The file names are 'Arya', 'Tyrion', etc., but the class *inside* is likely 'arya', 'tyrion'.
# We will use the capitalized name for the module/file lookup and the lowercase name for the class lookup.

@pytest.fixture(scope="session", params=['arya', 'tyrion', 'oberyn', 'brienne'])
def character_file_name(request):
    """Fixture to parametrize tests across all four character files (e.g., 'Arya')."""
    return request.param

@pytest.fixture
def character_name(character_file_name):
    """Returns the expected class name (lowercase, e.g., 'arya')."""
    return character_file_name.title()
#
# @pytest.fixture
# def character_class(student_modules, character_file_name, character_name):
#     """Dynamically get the main class (e.g., arya, tyrion) from the module."""
#     # The module is imported using the file name (e.g., 'Arya')
#     student_module = student_modules[character_file_name]
#
#     # Check if the class itself exists in the module (using the lowercase name)
#     if not hasattr(student_module, character_name):
#         pytest.fail(f"Could not find the class '{character_name}' in {character_file_name}.py. Ensure the class name is lowercase.")
#
#     return getattr(student_module, character_name)


@pytest.fixture
def character_class(student_modules, character_file_name, character_name):
    """Dynamically get the main class, skipping if the module failed to load."""

    # 1. Check if the module load failed (due to Syntax/Import Error)
    module_status = student_modules[character_file_name]

    if module_status == "LOAD_FAILED":
        pytest.skip(
            f"Submission file {character_file_name}.py has a syntax or import error. Skipping tests for this file."
        )
    if module_status == "FILE_MISSING":
        pytest.skip(
            f"Submission file {character_file_name}.py is missing. Skipping tests."
        )

    student_module = module_status  # It's the actual module now

    # 2. Check if the class exists
    if not hasattr(student_module, character_name):
        pytest.fail(
            f"Could not find the class '{character_name}' in {character_file_name}.py. Failing structural tests."
        )

    return getattr(student_module, character_name)


# character_instance remains the same, as it depends on the now-error-checking character_class.


@pytest.fixture
def character_instance(character_class):
    """Instantiate the character class for method testing."""
    try:
        # Assuming the class takes no arguments for simple instantiation
        return character_class()
    except Exception as e:
        pytest.fail(f"Failed to instantiate class {character_class.__name__}. Check the __init__ method. Error: {e}")