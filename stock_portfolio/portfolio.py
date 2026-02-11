import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import random
import sqlite3
from datetime import datetime

# Define NIFTY Stock List

nifty_stocks = [
    "TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS",
    "ICICIBANK.NS", "SBIN.NS", "ITC.NS", "LT.NS",
    "BHARTIARTL.NS", "KOTAKBANK.NS", "AXISBANK.NS",
    "WIPRO.NS", "HCLTECH.NS", "TATAMOTORS.NS",
    "MARUTI.NS", "SUNPHARMA.NS", "DRREDDY.NS",
    "ONGC.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS"
]

# Create Portfolio

portfolio_data = []

for stock in nifty_stocks:
    portfolio_data.append({
        "Stock": stock,
        "Quantity": random.randint(5, 30),
        "Buy_Price": random.uniform(800, 2500)
    })

df = pd.DataFrame(portfolio_data)

# Fetch REAL-TIME Current Price

def fetch_realtime_prices(stock_list):

    realtime_prices = {}

    for stock in stock_list:
        try:
            ticker = yf.Ticker(stock)
            realtime_prices[stock] = ticker.fast_info["lastPrice"]
        except:
            realtime_prices[stock] = None

    return realtime_prices


current_prices = fetch_realtime_prices(df["Stock"].tolist())
df["Current_Price"] = df["Stock"].map(current_prices)

df.dropna(inplace=True)


# Financial Calculations

df["Investment"] = df["Quantity"] * df["Buy_Price"]
df["Current_Value"] = df["Quantity"] * df["Current_Price"]
df["Profit_Loss"] = df["Current_Value"] - df["Investment"]
df["Return_%"] = (df["Profit_Loss"] / df["Investment"]) * 100


# Portfolio Summary

total_investment = df["Investment"].sum()
total_current_value = df["Current_Value"].sum()
total_profit = df["Profit_Loss"].sum()
weighted_return = (total_profit / total_investment) * 100

print("\n📊 REAL-TIME PORTFOLIO REPORT")
print(df)

print("\n📈 LIVE PORTFOLIO SUMMARY")
print("Total Investment:", round(total_investment, 2))
print("Current Value:", round(total_current_value, 2))
print("Live Profit/Loss:", round(total_profit, 2))
print("Live Weighted Return: {:.2f}%".format(weighted_return))


# SQLITE DATABASE SECTION

def create_database():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            stock TEXT,
            quantity INTEGER,
            buy_price REAL,
            current_price REAL,
            investment REAL,
            current_value REAL,
            profit_loss REAL,
            return_percent REAL
        )
    """)

    conn.commit()
    conn.close()


def save_to_database(df):

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO portfolio (
                timestamp, stock, quantity, buy_price,
                current_price, investment, current_value,
                profit_loss, return_percent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            row["Stock"],
            int(row["Quantity"]),
            float(row["Buy_Price"]),
            float(row["Current_Price"]),
            float(row["Investment"]),
            float(row["Current_Value"]),
            float(row["Profit_Loss"]),
            float(row["Return_%"])
        ))

    conn.commit()
    conn.close()


# Create table and store data
create_database()
save_to_database(df)

print("\n✅ Portfolio snapshot saved to SQLite database (portfolio.db)")


# Visualization

colors = ["green" if x >= 0 else "red" for x in df["Return_%"]]

plt.figure(figsize=(12,6))
plt.bar(df["Stock"], df["Return_%"], color=colors)
plt.axhline(0)
plt.xticks(rotation=90)
plt.xlabel("Stock")
plt.ylabel("Live Return (%)")
plt.title("Real-Time Portfolio Performance")
plt.tight_layout()
plt.show()
