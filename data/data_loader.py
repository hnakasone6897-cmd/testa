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


if __name__ == "__main__":
    path = save_sample_data()
    print(f"Sample data saved: {path}")

    data = load_csv_data()
    print(f"Rows loaded: {len(data)}")

    converted_data = convert_price_data(data)

    print(f"Latest close: {converted_data[-1]['close']}")
    print(f"Close type: {type(converted_data[-1]['close']).__name__}")

    analyzed_data = calculate_sma(converted_data, period=3)

    print(f"Latest SMA: {analyzed_data[-1]['sma']}")