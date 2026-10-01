#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")

MIN_SYSTOLIC = 60
MAX_SYSTOLIC = 250
CUTOFF = 140
REASON = "140 mmHg is the AHA stage 2 hypertension threshold, so calls go to patients most likely to need treatment changes."


def read_encounters(data_path):
    """Read the CSV and keep usable encounters.

    A usable encounter is a dict with patient_id, visit_date, and an integer
    systolic reading from 60 to 250 mmHg. Returns (encounters, skipped).
    """
    with open(data_path) as f:
        lines = f.read().splitlines()

    encounters = []
    skipped = 0

    for line in lines[1:]:
        if line.strip() == "":
            print("Skipping a blank row.")
            skipped += 1
            continue

        fields = line.split(",")
        if len(fields) != 3:
            print(f"Skipping (wrong number of fields): {line}")
            skipped += 1
            continue

        patient_id, visit_date, systolic_text = fields
        try:
            systolic = int(systolic_text)
        except ValueError:
            print(f"Skipping (not a number): {line}")
            skipped += 1
            continue

        if systolic < MIN_SYSTOLIC or systolic > MAX_SYSTOLIC:
            print(f"Skipping (out of range): {line}")
            skipped += 1
            continue

        encounters.append(
            {"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic}
        )

    return encounters, skipped


def main():
    """Write output/vitals_report.txt and output/followup_list.txt."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_path = OUTPUT_DIR / "vitals_report.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines) + "\n")

    with open(report_path) as f:
        print(f.read())

    followup_lines = [f"Cutoff: {CUTOFF} mmHg", f"Reason: {REASON}"]
    followup_lines += patients_at_or_above(encounters, CUTOFF)
    followup_path = OUTPUT_DIR / "followup_list.txt"
    with open(followup_path, "w") as f:
        f.write("\n".join(followup_lines) + "\n")

    with open(followup_path) as f:
        print(f.read())


if __name__ == "__main__":
    main()
