from pathlib import Path
import csv


DATA_DIR = Path(__file__).resolve().parent


def save_sample_data(filename: str = "sample_usdjpy.csv") -> Path:
    """TESTAの動作確認用にサンプル価格データを保存する。"""
    output_path = DATA_DIR / filename

    rows = [
        ["time", "open", "high", "low", "close", "volume"],
        ["2026-08-15 09:00", 147.10, 147.20, 147.00, 147.10, 100],
        ["2026-08-15 09:15", 147.10, 147.30, 147.05, 147.25, 110],
        ["2026-08-15 09:30", 147.25, 147.40, 147.15, 147.35, 120],
        ["2026-08-15 09:45", 147.35, 147.45, 147.25, 147.40, 130],
        ["2026-08-15 10:00", 147.40, 147.50, 147.30, 147.45, 125],
        ["2026-08-15 10:15", 147.45, 147.40, 147.20, 147.25, 140],
        ["2026-08-15 10:30", 147.25, 147.20, 147.00, 147.05, 150],
        ["2026-08-15 10:45", 147.05, 147.00, 146.80, 146.90, 155],
        ["2026-08-15 11:00", 146.90, 146.95, 146.70, 146.80, 160],
        ["2026-08-15 11:15", 146.80, 147.00, 146.75, 146.95, 150],
        ["2026-08-15 11:30", 146.95, 147.15, 146.90, 147.10, 145],
        ["2026-08-15 11:45", 147.10, 147.25, 147.00, 147.20, 140],
        ["2026-08-15 12:00", 147.20, 147.35, 147.10, 147.30, 135],
        ["2026-08-15 12:15", 147.30, 147.20, 147.00, 147.05, 130],
        ["2026-08-15 12:30", 147.05, 146.95, 146.80, 146.85, 125],
        ["2026-08-15 12:45", 146.85, 146.75, 146.60, 146.70, 120],
        ["2026-08-15 13:00", 146.70, 146.90, 146.65, 146.85, 115],
        ["2026-08-15 13:15", 146.85, 147.05, 146.80, 147.00, 110],
        ["2026-08-15 13:30", 147.00, 147.20, 146.95, 147.15, 105],
        ["2026-08-15 13:45", 147.15, 147.30, 147.05, 147.25, 100],
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return output_path


def load_csv_data(filename: str = "sample_usdjpy.csv") -> list[dict]:
    """CSVデータを読み込む。"""
    input_path = DATA_DIR / filename

    with input_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def convert_price_data(data: list[dict]) -> list[dict]:
    """価格データのOHLCVを数値に変換する。"""
    numeric_columns = ["open", "high", "low", "close", "volume"]

    converted = []

    for row in data:
        new_row = row.copy()

        for column in numeric_columns:
            new_row[column] = float(row[column])

        new_row["volume"] = int(float(row["volume"]))

        converted.append(new_row)

    return converted


def calculate_sma(data: list[dict], period: int = 3) -> list[dict]:
    """終値から単純移動平均（SMA）を計算する。"""
    if period <= 0:
        raise ValueError("period must be greater than 0")

    result = []

    for index, row in enumerate(data):
        new_row = row.copy()

        if index + 1 >= period:
            closes = [
                item["close"]
                for item in data[index + 1 - period:index + 1]
            ]
            new_row["sma"] = sum(closes) / period
        else:
            new_row["sma"] = None

        result.append(new_row)

    return result