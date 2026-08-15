from data.data_loader import (
    save_sample_data,
    load_csv_data,
    convert_price_data,
    calculate_sma,
)

from strategy.sma_strategy import generate_signal


def run_backtest(data: list[dict], initial_balance: float = 100000) -> dict:
    """SMA戦略の簡易バックテストを行う。"""
    balance = initial_balance
    position = None
    entry_price = None
    trades = []

    for row in data:
        signal = row["signal"]
        close = row["close"]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = close

        elif signal == "SELL" and position == "LONG":
            profit = close - entry_price
            balance += profit
            trades.append(
                {
                    "entry": entry_price,
                    "exit": close,
                    "profit": profit,
                }
            )

            position = None
            entry_price = None

    return {
        "initial_balance": initial_balance,
        "final_balance": balance,
        "trades": trades,
    }


def main():
    save_sample_data()

    data = load_csv_data()
    data = convert_price_data(data)
    data = calculate_sma(data, period=3)
    data = generate_signal(data)

    result = run_backtest(data)

    print(f"Initial balance: {result['initial_balance']}")
    print(f"Final balance: {result['final_balance']}")
    print(f"Trades: {len(result['trades'])}")


if __name__ == "__main__":
    main()