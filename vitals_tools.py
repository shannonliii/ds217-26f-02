"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list of the systolic reading (mmHg) from every encounter."""
    readings = []
    for encounter in encounters:
        readings.append(encounter['systolic'])
    return readings


def mean_systolic(readings):
    """Return the mean of the readings, or None if the list is empty."""
    if len(readings) == 0:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return how many distinct patient IDs appear in the encounters."""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter['patient_id'])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return the sorted distinct patient IDs with any reading >= cutoff."""
    flagged = set()
    for encounter in encounters:
        if encounter['systolic'] >= cutoff:
            flagged.add(encounter['patient_id'])
    return sorted(flagged)
