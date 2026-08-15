from data.data_loader import (
    save_sample_data,
    load_csv_data,
    convert_price_data,
    calculate_sma,
)

from strategy.sma_strategy import generate_signal


def run_backtest(
    data: list[dict],
    initial_balance: float = 100000,
) -> dict:
    """SMA戦略の簡易バックテストを行う。"""
    balance = initial_balance
    position = None
    entry_price = None
    trades = []

    peak_balance = initial_balance
    max_drawdown = 0.0

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

        if balance > peak_balance:
            peak_balance = balance

        drawdown = peak_balance - balance

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    total_profit = balance - initial_balance

    winning_trades = [
        trade for trade in trades
        if trade["profit"] > 0
    ]

    losing_trades = [
        trade for trade in trades
        if trade["profit"] < 0
    ]

    trade_count = len(trades)

    if trade_count > 0:
        win_rate = len(winning_trades) / trade_count * 100
    else:
        win_rate = 0.0

    return {
        "initial_balance": initial_balance,
        "final_balance": balance,
        "total_profit": total_profit,
        "trades": trades,
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "win_rate": win_rate,
        "max_drawdown": max_drawdown,
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
    print(f"Total profit: {result['total_profit']:.2f}")
    print(f"Trades: {len(result['trades'])}")
    print(f"Winning trades: {result['winning_trades']}")
    print(f"Losing trades: {result['losing_trades']}")
    print(f"Win rate: {result['win_rate']:.2f}%")
    print(f"Max drawdown: {result['max_drawdown']:.2f}")


if __name__ == "__main__":
    main()