from config.settings import (
    PROJECT_NAME,
    SYMBOL,
    TIMEFRAME,
    LIVE_TRADING,
)

from data.data_loader import (
    save_sample_data,
    load_csv_data,
    convert_price_data,
    calculate_sma,
)

from strategy.sma_strategy import generate_signal


def main():
    print(f"{PROJECT_NAME} AI START")
    print(f"Symbol: {SYMBOL}")
    print(f"Timeframe: {TIMEFRAME}")
    print(f"Live trading: {LIVE_TRADING}")

    save_sample_data()

    data = load_csv_data()
    data = convert_price_data(data)
    data = calculate_sma(data, period=3)
    data = generate_signal(data)

    latest = data[-1]

    print(f"Latest close: {latest['close']}")
    print(f"Latest SMA: {latest['sma']}")
    print(f"Latest signal: {latest['signal']}")


if __name__ == "__main__":
    main()