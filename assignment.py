import psycopg2
import pandas as pd
from Virtualisation import visualize_trading_data


# Connect to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="NewDb",  # database name
            user="",  # dbusername
            password="",  # dbpassword
            host="localhost",
            port="5432",
        )
        print("Connected to database successfully!")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return None


# Retrieve stock data from the database
def retrieve_stock_data(conn, start_date, end_date):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM stock_data WHERE date >= %s AND date <= %s;"
        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        return df
    except psycopg2.Error as e:
        print("Error retrieving stock data:", e)
        return None


# Generate trading signals based on moving averages
def generate_trading_signals(df):
    df["50_day_ma"] = df["close"].rolling(window=50).mean()
    df["500_day_ma"] = df["close"].rolling(window=500).mean()
    df["20_day_ma"] = df["close"].rolling(window=20).mean()
    df["200_day_ma"] = df["close"].rolling(window=200).mean()
    df["10_day_ma"] = df["close"].rolling(window=10).mean()
    df["5_day_ma"] = df["close"].rolling(window=5).mean()

    df["buy_signal"] = (df["50_day_ma"] > df["500_day_ma"]) & (
        df["50_day_ma"].shift(1) <= df["500_day_ma"].shift(1)
    )
    df["sell_signal"] = (df["20_day_ma"] < df["200_day_ma"]) & (
        df["20_day_ma"].shift(1) >= df["200_day_ma"].shift(1)
    )
    df["close_buy_position"] = (df["10_day_ma"] < df["20_day_ma"]) & (
        df["10_day_ma"].shift(1) >= df["20_day_ma"].shift(1)
    )
    df["close_sell_position"] = (df["5_day_ma"] < df["10_day_ma"]) & (
        df["5_day_ma"].shift(1) >= df["10_day_ma"].shift(1)
    )

    return df


# Calculate profit and loss based on generated signals
def calculate_profit_loss(df):
    buy_price = None
    profit_loss = []
    for index, row in df.iterrows():
        if row["buy_signal"] and buy_price is None:
            buy_price = row["close"]
        elif row["sell_signal"] and buy_price is not None:
            profit_loss.append(row["close"] - buy_price)
            buy_price = None
        elif row["close_buy_position"] and buy_price is not None:
            profit_loss.append(row["close"] - buy_price)
            buy_price = None
        elif row["close_sell_position"] and buy_price is not None:
            profit_loss.append(row["close"] - buy_price)
            buy_price = None
    df["profit_loss"] = profit_loss
    return df


# Store results back into the database
def store_results(conn, df, stock_symbol):
    try:
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute(
                "INSERT INTO trading_results (symbol, date, buy_signal, sell_signal, close_buy_position, close_sell_position, profit_loss) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    stock_symbol,
                    row["date"],
                    row["buy_signal"],
                    row["sell_signal"],
                    row["close_buy_position"],
                    row["close_sell_position"],
                    row["profit_loss"],
                ),
            )
        conn.commit()
        cursor.close()
        print("Results for", stock_symbol, "stored in the database successfully!")
    except psycopg2.Error as e:
        print("Error storing results in the database:", e)


def main():
    # Connect to the database
    conn = connect_to_database()
    if conn is None:
        return

    # List of stock symbols
    stock_symbols = ["AAPL", "HDB", "INRX", "JIOFINNS", "MARA", "TATAMOTORSNS", "TSLA"]

    # Process each stock
    for stock_symbol in stock_symbols:
        # Retrieve stock data from the database for the entire dataset
        df = retrieve_stock_data(conn, start_date=None, end_date=None)
        if df is None:
            continue

        # Generate trading signals
        df = generate_trading_signals(df)

        # Calculate profit and loss
        df = calculate_profit_loss(df)

        # Store results back into the database
        store_results(conn, df, stock_symbol)
        # Visualize trading data
        visualize_trading_data(df)

    # Close the database connection
    conn.close()
    print("Database connection closed.")


# Call the main function directly
if __name__ == "__main__":
    main()
