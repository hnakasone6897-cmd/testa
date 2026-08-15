def generate_signal(data: list[dict]) -> list[dict]:
    """終値とSMAを比較して売買シグナルを作る。"""
    result = []

    for row in data:
        new_row = row.copy()

        if new_row["sma"] is None:
            new_row["signal"] = "HOLD"
        elif new_row["close"] > new_row["sma"]:
            new_row["signal"] = "BUY"
        elif new_row["close"] < new_row["sma"]:
            new_row["signal"] = "SELL"
        else:
            new_row["signal"] = "HOLD"

        result.append(new_row)

    return result