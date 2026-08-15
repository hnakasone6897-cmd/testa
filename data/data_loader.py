from pathlib import Path
import csv


DATA_DIR = Path(__file__).resolve().parent


def save_sample_data(filename: str = "sample_usdjpy.csv") -> Path:
    """TESTAの動作確認用にサンプル価格データを保存する。"""
    output_path = DATA_DIR / filename

    rows = [
        ["time", "open", "high", "low", "close", "volume"],
        ["2026-08-15 09:00", 147.10, 147.20, 147.00, 147.15, 100],
        ["2026-08-15 09:15", 147.15, 147.25, 147.05, 147.20, 120],
        ["2026-08-15 09:30", 147.20, 147.30, 147.10, 147.25, 110],
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return output_path


def load_csv_data(filename: str = "sample_usdjpy.csv") -> list[dict]:
    """保存したCSVデータを読み込む。"""
    input_path = DATA_DIR / filename

    with input_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


if __name__ == "__main__":
    path = save_sample_data()
    print(f"Sample data saved: {path}")

    data = load_csv_data()
    print(f"Rows loaded: {len(data)}")
    print(f"Latest close: {data[-1]['close']}")