from pathlib import Path

import pandas as pd


TASK_SEGMENTS = {
    "baseline": ("relax_start", "relax_end"),
    "squat": ("squat_test_start", "squat_test_end"),
    "video1": ("video1_start", "video1_end"),
    "video2": ("video2_start", "video2_end"),
}


def normalize_subject_id(subject_id):
    subject_str = str(subject_id)
    if subject_str.isdigit():
        return f"S{int(subject_str):02d}"
    return subject_str


def subject_sort_key(subject_id):
    subject_str = str(subject_id)
    normalized = normalize_subject_id(subject_str)
    if normalized.startswith("S") and normalized[1:].isdigit():
        return (0, int(normalized[1:]))
    return (1, normalized)


def list_subject_ids(data_dir):
    data_dir = Path(data_dir)
    eda_subjects = {path.stem for path in (data_dir / "eda").glob("*.csv")}
    ppg_subjects = {path.stem for path in (data_dir / "ppg").glob("*.csv")}
    stamp_subjects = {path.stem for path in (data_dir / "stamps").glob("*.txt")}
    return sorted(eda_subjects & ppg_subjects & stamp_subjects, key=subject_sort_key)


def load_signal(path, signal_col):
    path = Path(path)
    df = pd.read_csv(path)

    if "Timestamp" not in df.columns:
        if "LocalTimestamp" not in df.columns:
            raise KeyError(f"{path} no contiene ni 'Timestamp' ni 'LocalTimestamp'.")
        df = df.rename(columns={"LocalTimestamp": "Timestamp"})

    required_columns = ["Timestamp", signal_col]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise KeyError(f"{path} no contiene las columnas requeridas: {missing_columns}")

    df = df[required_columns].copy()
    df["Timestamp"] = df["Timestamp"].astype(float)
    df[signal_col] = df[signal_col].astype(float)
    return df.sort_values("Timestamp").reset_index(drop=True)


def load_subject_signal(data_dir, modality, subject_id, signal_col):
    return load_signal(Path(data_dir) / modality / f"{subject_id}.csv", signal_col)


def load_stamps(path):
    stamps = {}
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            key, value = line.split(",", maxsplit=1)
            stamps[key] = float(value)
    return stamps


def load_subject_stamps(data_dir, subject_id):
    return load_stamps(Path(data_dir) / "stamps" / f"{subject_id}.txt")


def crop_signal(df, start_ts, end_ts):
    cropped_df = df[(df["Timestamp"] >= float(start_ts)) & (df["Timestamp"] <= float(end_ts))].copy()
    return cropped_df.sort_values("Timestamp").reset_index(drop=True)


def segment_signal(df, stamps, label_name):
    if label_name not in TASK_SEGMENTS:
        raise KeyError(f"Tarea desconocida: {label_name}")
    start_key, end_key = TASK_SEGMENTS[label_name]
    return crop_signal(df, stamps[start_key], stamps[end_key])
