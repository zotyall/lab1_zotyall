# lab1_zotyall
# Grade Evaluator — ALU Python Lab

This project is a Python based grade evaluation tool built for the ALU Introduction to Python Programming and Databases lab. It reads student grades from a CSV file, validates them, calculates the final grade and GPA, and determines whether the student passed or failed.

## How to Run the Python Script

Make sure grades.csv is in the same folder as grade-evaluator.py, then open your terminal and run:

python3 grade-evaluator.py

It will ask you for the filename. Just type grades.csv and hit Enter. The script will then display a full grade report showing each assignment, the formative and summative category scores, the final grade, GPA out of 5.0, and whether the student passed or failed.

## How to Run the Shell Script

The organizer.sh script archives your grades.csv file by moving it into an archive folder with a timestamp, creates a fresh empty grades.csv, and logs everything into organizer.log.

To run it, first make it executable by typing this in the terminal:

chmod +x organizer.sh

Then run it:

./organizer.sh

## Pass or Fail

A student only passes if they score 50% or above in both the Formative and Summative categories. Scoring well overall but failing one category still results in a fail.

## GPA

GPA is calculated as: (Final Grade / 100) x 5.0
