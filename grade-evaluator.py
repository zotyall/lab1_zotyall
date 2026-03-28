import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if not assignments:
        print("Error: The CSV file is empty or has no valid data rows.")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    Evaluates student grades based on loaded CSV data.
    """
    print("\n--- Processing Grades ---\n")

    # a) Grade Validation: all scores must be between 0 and 100
    invalid_scores = [d['assignment'] for d in data if not (0 <= d['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have scores outside the valid range (0-100):")
        for name in invalid_scores:
            print(f"  - {name}")
        sys.exit(1)
    print("✔ All scores are within valid range (0–100).")

    # b) Weight Validation
    formative_data = [d for d in data if d['group'] == 'Formative']
    summative_data = [d for d in data if d['group'] == 'Summative']

    total_weight     = sum(d['weight'] for d in data)
    formative_weight = sum(d['weight'] for d in formative_data)
    summative_weight = sum(d['weight'] for d in summative_data)

    weight_errors = []
    if total_weight != 100:
        weight_errors.append(f"  - Total weight is {total_weight}, expected 100.")
    if formative_weight != 60:
        weight_errors.append(f"  - Formative weight is {formative_weight}, expected 60.")
    if summative_weight != 40:
        weight_errors.append(f"  - Summative weight is {summative_weight}, expected 40.")

    if weight_errors:
        print("Error: Weight validation failed:")
        for err in weight_errors:
            print(err)
        sys.exit(1)
    print("✔ Weight validation passed (Total=100, Formative=60, Summative=40).\n")

    # c) GPA Calculation
    # Weighted grade within each group
    formative_grade = sum(d['score'] * d['weight'] for d in formative_data) / formative_weight
    summative_grade = sum(d['score'] * d['weight'] for d in summative_data) / summative_weight

    # Overall final grade (weighted across all assignments)
    final_grade = sum(d['score'] * d['weight'] for d in data) / total_weight
    gpa = (final_grade / 100) * 5.0

    # d) Pass/Fail — must score >= 50% in BOTH categories
    formative_pass = formative_grade >= 50
    summative_pass = summative_grade >= 50
    overall_status = "PASSED" if (formative_pass and summative_pass) else "FAILED"

    # e) Resubmission Logic
    # Find failed formative assignments (score < 50)
    failed_formative = [d for d in formative_data if d['score'] < 50]
    resubmit_candidates = []
    if failed_formative:
        max_failed_weight = max(d['weight'] for d in failed_formative)
        resubmit_candidates = [
            d['assignment'] for d in failed_formative
            if d['weight'] == max_failed_weight
        ]

    # f) Print Full Report
    print("=" * 50)
    print("         GRADE REPORT")
    print("=" * 50)

    print("\n[Assignment Breakdown]")
    print(f"{'Assignment':<40} {'Group':<12} {'Score':>6} {'Weight':>7}")
    print("-" * 68)
    for d in data:
        print(f"{d['assignment']:<40} {d['group']:<12} {d['score']:>6.1f} {d['weight']:>7.1f}")

    print("\n[Category Summary]")
    print(f"  Formative Grade : {formative_grade:.2f}%  ({'PASS' if formative_pass else 'FAIL'})")
    print(f"  Summative Grade : {summative_grade:.2f}%  ({'PASS' if summative_pass else 'FAIL'})")

    print("\n[Final Results]")
    print(f"  Final Grade     : {final_grade:.2f}%")
    print(f"  GPA             : {gpa:.2f} / 5.0")
    print(f"  Status          : {overall_status}")

    print("\n[Resubmission]")
    if not failed_formative:
        print("  No failed formative assignments. No resubmission required.")
    else:
        print("  Failed formative assignments:")
        for d in failed_formative:
            print(f"    - {d['assignment']} (Score: {d['score']:.1f}, Weight: {d['weight']:.1f})")
        print(f"\n  Eligible for resubmission (highest weight among failed formative):")
        for name in resubmit_candidates:
            print(f"    → {name}")

    print("\n" + "=" * 50)
    print(f"  FINAL DECISION: {overall_status}")
    print("=" * 50)


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
