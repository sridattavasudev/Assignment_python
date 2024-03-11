import matplotlib.pyplot as plt


def visualize_trading_data(df):
    plt.figure(figsize=(12, 6))

    # Plotting candlestick chart
    plt.subplot(2, 1, 1)
    plt.title("Stock Price")
    plt.plot(df["date"], df["close"], label="Close", color="black")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    # Highlighting entry and exit points
    plt.subplot(2, 1, 2)
    plt.title("Trading Signals")
    plt.plot(df["date"], df["close"], label="Close", color="black")
    plt.scatter(
        df[df["buy_signal"] == True]["date"],
        df[df["buy_signal"] == True]["close"],
        label="Buy",
        color="green",
        marker="^",
        alpha=0.7,
    )
    plt.scatter(
        df[df["sell_signal"] == True]["date"],
        df[df["sell_signal"] == True]["close"],
        label="Sell",
        color="red",
        marker="v",
        alpha=0.7,
    )
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    plt.tight_layout()
    plt.show()
