# Autograder setup
1. Go to Sakai COMP 271 F25 => Assignments => "Chapter 12A Assignment 1: Triangle with Inheritance" => "Grade".
2. Download student submissions by clicking on "Download All" => **Check** the box for " Student submission attachment(s)".
3. Unzip the archive and copy into the "Ch12A-Triangle" directory in the repo. 
4. Rename the Sakai assignments directory to something short (optional) 
5. Run `runner_triangle.py`, set the `sakai_submissions_dir` variable to the directory of Sakai submissions
6. Open the `graded_submissions` directory and view the following files:
   * `grades_summary_sorted.csv` for a sorted list of grades
   * Each student with UVID will have two files inside:
     * `UVID_Triangle.py`: their source code
     * `UVID_results.json`: JSON with the test case results. Lists what test cases passed, and what failed. Use this to write your feedback.
7. Start grading the assignment on Sakai. _Do not_ use the new Sakai grader. 
8. Put the points and feedback for all students.
9. Do not forget to check the `Late Pass 1` and `Late Pass 2` assignments on Sakai to see if students turned in their work with a late pass.

## Important notes
* Check the `grades_summary_sorted.csv` for any scores of 0. These programs likely failed to compile.
* Some students don't put their code in a function. The autograder will likely complain. You would need to manually edit their code inside the `graded_submissions` directory and re-run the autograder.
