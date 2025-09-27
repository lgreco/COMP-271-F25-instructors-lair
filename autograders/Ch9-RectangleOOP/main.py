# prepare the submissions
# Parse python submissions from students
# Get their UVID and full name from the paths 
# Rename the only Py file as "<uvid>_Rectangle.py"
# Copy the file to the submissions directory  
# Run pytest with `--name=UVID`, separate out files for all students 
# Parse JSONs to get names, uvid, score, total

from pathlib import Path
import subprocess
import json
import csv
from loguru import logger
import sys
import time

logger.remove()  # Remove the default handler.
logger.add(sys.stdout, level='INFO')  # Log only messages with level "WARNING" or higher.

def parse_student_info_from_path(path: Path):
    """Given a path like .../Sakai-RectangleOOP/First Last (uvid)/submission.py
    return (uvid, "First Last")"""
    parts = path.parts
    if len(parts) < 2:
        raise ValueError(f"Path {path} is too short to parse student info")
    student_dir = parts[-2]  # "First Last (uvid)"
    if '(' not in student_dir or ')' not in student_dir:
        raise ValueError(f"Cannot find UVID in directory name: {student_dir}")
    name_part, uvid_part = student_dir.rsplit('(', 1)
    name = name_part.strip()
    uvid = uvid_part.strip(' )')
    return uvid, name

def rename_submission(path: Path, dest_dir: Path):
    """Rename the only .py file in path to <uvid>_Rectangle.py and copy to dest_dir"""
    uvid, name = parse_student_info_from_path(path)
    py_files = list(path.glob('*.py'))
    if len(py_files) == 0:
        raise ValueError(f"No .py files found in {path}")
    if len(py_files) > 1:
        raise ValueError(f"Multiple .py files found in {path}: {py_files}")
    src_file = py_files[0]
    dest_file = dest_dir / f"{uvid}_Rectangle.py"
    with open(src_file, 'r') as fsrc, open(dest_file, 'w') as fdst:
        fdst.write(fsrc.read())
    return uvid, name, dest_file


def prepare_submissions(sakai_basedir: Path|str) -> dict:
    """
    Rename and copy all submissions to submissions/ directory
    """
    basepath = Path('./')
    if isinstance(sakai_basedir, str):
        sakai_basedir = Path(sakai_basedir)
    # sakai_basedir = basepath / 'Sakai-RectangleOOP'
    
    uvid2name_map = {}
    # loop thru all directories in sakai_basedir
    for i, student_dir in enumerate(sorted(sakai_basedir.iterdir())):
        logger.info(f"Processing {student_dir}")
        if student_dir.is_dir():
            try:
                dest_dir = basepath / 'submissions'
                dest_dir.mkdir(exist_ok=True) 
                py_path = student_dir / 'Submission attachment(s)'
                uvid, name, new_file = rename_submission(py_path, dest_dir)
                uvid2name_map[uvid] = name
                if new_file.exists():
                    continue 
                logger.debug(f"Copied and renamed submission to {new_file}")
            except Exception as e:
                logger.error(f"Error processing {student_dir}: {e}")
    return uvid2name_map

def grade_submissions(submission_dir: Path, uvid2name_map: dict):
    """
    Run pytest on each submission in submission_dir
    """
    results = []
    for py_file in sorted(submission_dir.glob('*_Rectangle.py')):
        uvid = py_file.stem.split('_')[0]
        name = uvid2name_map.get(uvid, 'Unknown')
        logger.info(f"Grading {uvid} from {py_file}")
        result_json = submission_dir / f"{uvid}_results.json"

        cmd = [
            'pytest', 
            '--student-file', str(py_file), 
            '--name', name,
            '--uvid', uvid,
            '--output', str(result_json),
            '--tb=line',
            '-qq',
            '--disable-warnings',
            'tests/'
        ]
        try:
            subprocess.run(cmd, check=False)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error grading {uvid}: {e}")
            results.append((time.ctime(), uvid, 0, 0))

        if result_json.exists():
            with open(result_json, 'r') as f:
                data = json.load(f)
                total = data.get('total', 0)
                earned = data.get('earned', 0)
                results.append((time.ctime(), uvid, name, earned, total))
                logger.debug(f"Result for {uvid}: {earned}/{total}")
        else:
            logger.error(f"No result JSON found for {uvid}")
            results.append((time.ctime(), uvid, name, 0, 0))


    # Write summary CSV
    summary_csv = submission_dir / 'grades_summary.csv'
    with open(summary_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'UVID', 'Name', 'Earned', 'Total'])
        for row in results:
            writer.writerow(row)
    logger.info(f"Wrote summary to {summary_csv}")
    
    ## sort the CSV by last name   
    sorted_csv = submission_dir / 'grades_summary_sorted.csv'
    with open(summary_csv, 'r') as infile, open(sorted_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
        # sort by last name (assuming name is in "Last, First" format)
        rows.sort(key=lambda r: r[1].split(',')[0].strip().lower())  
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)
    return
    
    
def main():
    # sakai_submissions_dir = Path('./Sakai-RectangleOOP')  ## example
    sakai_submissions_dir = None
    assert sakai_submissions_dir is not None, f'Set the sakai_submissions_dir variable to the name of the directory with student submissions'

    submission_dir = Path("./submissions")
    submission_dir.mkdir(exist_ok=True)

    uvid2name_map = prepare_submissions(sakai_submissions_dir)

    grade_submissions(submission_dir, uvid2name_map=uvid2name_map)
    return 
    
if __name__ == '__main__':
    main()