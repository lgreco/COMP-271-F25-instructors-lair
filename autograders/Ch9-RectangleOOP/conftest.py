# conftest.py
import importlib.util
import os
import uuid
import json
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--student-file",
        action="store",
        default=None,
        help="Path to student's submission (.py)."
    )
    print(f'Reading student file from command line argument: {parser}')
    parser.addoption(
        "--output",
        action="store",
        default=None,
        help="Path to write JSON/CSV grade output (optional)."
    )
    parser.addoption(
        "--name",
        action="store",
        type=str,
        default=None,
        help="Student name",
    )
    
    parser.addoption(
        "--uvid",
        action="store",
        type=str,
        default=None,
        help="Student UVID",
    )
    return 

def pytest_configure(config):
    # store running totals and details on config so plugin is stateless across tests
    if not hasattr(config, "_grading"):
        config._grading = {"total": 0, "earned": 0, "details": []}

def load_student_module(path):
    """Load student's .py into a uniquely named module to avoid caching issues."""
    spec = importlib.util.spec_from_file_location(f"student_{uuid.uuid4().hex}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def student_module(request):
    path = request.config.getoption("--student-file")
    if not path:
        pytest.skip("No --student-file provided. Use: pytest --student-file=path/to/submission.py")
    if not os.path.exists(path):
        pytest.skip(f"Student file not found: {path}")
    return load_student_module(path)

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
    
    cfg._grading["details"].append({
        "nodeid": item.nodeid,
        # "name": item.name,
        "points": pts,
        "passed": passed,
        "error": None if passed else str(call.excinfo)
    })

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    g = config._grading
    terminalreporter.write_sep("=", f"Score: {g['earned']} / {g['total']}")

    out = config.getoption("--output")
    if out:
        # student identifier
        student_file = config.getoption("--student-file") or ""
        # student = os.path.splitext(os.path.basename(student_file))[0]
        student_name = config.getoption("--name")
        uvid = config.getoption("--uvid")
        if not uvid:
            uvid = "NA"   
        if not student_name:
            student_file = config.getoption("--student-file") or ""
            student_name = os.path.splitext(os.path.basename(student_file))[0]

        payload = {
            "name": student_name,
            "UVID": uvid,
            "earned": g["earned"],
            "total": g["total"],
            "details": g["details"],
        }

        # write JSON
        if out.lower().endswith(".json"):
            with open(out, "w") as f:
                json.dump(payload, f, indent=2)
        # write CSV (one row per test)
        elif out.lower().endswith(".csv"):
            import csv
            with open(out, "w", newline='') as f:
                w = csv.writer(f)
                w.writerow(["student", "earned", "total", "nodeid", "test_name", "points", "passed", "error"])
                for d in g["details"]:
                    w.writerow([student_name, g["earned"], g["total"], d["nodeid"], d["name"], d["points"], d["passed"], d["error"]])
        else:
            # default to JSON if extension unknown
            with open(out, "w") as f:
                json.dump(payload, f, indent=2)
