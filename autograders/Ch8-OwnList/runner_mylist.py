import re
from pathlib import Path
import subprocess
import json
import pytest
import csv
from loguru import logger
import sys
import time

logger.remove()  # Remove the default handler.
logger.add(
    sys.stdout, level="INFO"
)  # Log only messages with level "WARNING" or higher.
#
ASSIGNNMENT_NAME = "MyList"


def parse_student_info_from_path(path: Path):
    """Given a path like .../<Assignment Name>/First Last (uvid)/submission.py
    return (uvid, "First Last")"""
    parts = path.parts
    if len(parts) < 2:
        raise ValueError(f"Path {path} is too short to parse student info")
    student_dir = parts[-2]  # "First Last (uvid)"
    if "(" not in student_dir or ")" not in student_dir:
        raise ValueError(f"Cannot find UVID in directory name: {student_dir}")
    name_part, uvid_part = student_dir.rsplit("(", 1)
    name = name_part.strip()
    uvid = uvid_part.strip(" )")
    return uvid, name


def rename_submission(path: Path, dest_dir: Path):
    """Rename the only .py file in path to <uvid>_Triangle.py and copy to dest_dir"""
    uvid, name = parse_student_info_from_path(path)
    py_files = list(path.glob("*.py"))
    if len(py_files) == 0:
        raise ValueError(f"No .py files found in {path}")
    if len(py_files) > 1:
        raise ValueError(f"Multiple .py files found in {path}: {py_files}")
    src_file = py_files[0]
    dest_file = dest_dir / f"{uvid}_{ASSIGNNMENT_NAME}.py"

    if not dest_file.exists():
        with open(src_file, "r") as fsrc, open(dest_file, "w") as fdst:
            orig_code = fsrc.read()
            lines = orig_code.strip().split('\n')
            if lines[-1].startswith('main()'):
                # orig_code = orig_code.replace('main()', '# main()  ## disabled main()')
                lines[-1] = '## main() # commented main()'
            fdst.write('\n'.join(lines))
    return uvid, name, dest_file


def prepare_submissions(
    sakai_basedir: Path | str, graded_submissions_dir: Path
) -> dict:
    """
    Rename and copy all submissions to submissions/ directory
    """
    basepath = Path("./")
    if isinstance(sakai_basedir, str):
        sakai_basedir = Path(sakai_basedir)
    # sakai_basedir = basepath / 'Sakai-RectangleOOP'

    uvid2name_map = {}
    # loop thru all directories in sakai_basedir
    for i, student_dir in enumerate(sorted(sakai_basedir.iterdir())):
        logger.info(f"Processing {student_dir}")
        if student_dir.is_dir():
            try:
                dest_dir = graded_submissions_dir
                dest_dir.mkdir(exist_ok=True)
                py_path = student_dir / "Submission attachment(s)"
                uvid, name, new_file = rename_submission(py_path, dest_dir)
                uvid2name_map[uvid] = name
                if new_file.exists():
                    continue
                logger.debug(f"Copied and renamed submission to {new_file}")
            except Exception as e:
                logger.error(f"Error processing {student_dir}: {e}")
    return uvid2name_map


def grade_single_submission(name, uvid):
    pytest.main(
        [
            "-q",
            "-v",
            "--name",
            name,
            "--UVID",
            uvid,
        ],
    )
    return

def grade_submissions(submission_dir: Path, uvid2name_map: dict):
    """
    Run pytest on each submission in submission_dir
    """
    results = []
    for py_file in sorted(submission_dir.glob("*_MyList.py")):
        uvid = py_file.stem.split("_")[0]
        name = uvid2name_map.get(uvid, "Unknown")
        logger.info(f"Grading {uvid} from {py_file}")
        result_json = submission_dir / f"{uvid}_results.json"

        grade_single_submission(name=name, uvid=uvid)

        if result_json.exists():
            with open(result_json, "r") as f:
                data = json.load(f)
                total = data.get("total", 0)
                earned = data.get("earned", 0)
                results.append((time.ctime(), uvid, name, earned, total))
                logger.debug(f"Result for {uvid}: {earned}/{total}")
        else:
            logger.error(f"No result JSON found for {uvid}")
            results.append((time.ctime(), uvid, name, 0, 0))
        # break

    # Write summary CSV
    summary_csv = submission_dir / "grades_summary.csv"
    with open(summary_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "UVID", "Name", "Earned", "Total"])
        for row in results:
            writer.writerow(row)
    logger.info(f"Wrote summary to {summary_csv}")

    ## sort the CSV by last name
    sorted_csv = submission_dir / "grades_summary_sorted.csv"
    with open(summary_csv, "r") as infile, open(sorted_csv, "w", newline="") as outfile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
        # sort by last name (assuming name is in "Last, First" format)
        rows.sort(key=lambda r: r[1].split(",")[0].strip().lower())
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)
    return


def main():
    # sakai_submissions_dir = Path('./Sakai-MyList')  ## example
    sakai_submissions_dir = None

    assert sakai_submissions_dir is not None, (
        f"Set the `sakai_submissions_dir` variable to the name of the directory with student submissions"
    )

    # grade_single_submission(name=name, uvid=uvid)
    graded_submission_dir = Path("./graded_submissions")
    graded_submission_dir.mkdir(exist_ok=True)

    uvid2name_map = prepare_submissions(
        graded_submissions_dir=graded_submission_dir,
        sakai_basedir=sakai_submissions_dir,
    )
    grade_submissions(graded_submission_dir, uvid2name_map)
    return


if __name__ == "__main__":
    main()
    # grade_single_submission(name='Ashley', uvid='dgallay')

