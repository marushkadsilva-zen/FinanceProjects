import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

portfolio_data = [
    {"Stock": "TCS.NS", "Quantity": 10, "Buy_Price": 3000},
    {"Stock": "INFY.NS", "Quantity": 15, "Buy_Price": 1400},
    {"Stock": "HDFCBANK.NS", "Quantity": 20, "Buy_Price": 1500},
    {"Stock": "RELIANCE.NS", "Quantity": 8, "Buy_Price": 2500},
    {"Stock": "ICICIBANK.NS", "Quantity": 12, "Buy_Price": 900},
    {"Stock": "LT.NS", "Quantity": 5, "Buy_Price": 2000},
    {"Stock": "SBIN.NS", "Quantity": 25, "Buy_Price": 550},
    {"Stock": "ITC.NS", "Quantity": 30, "Buy_Price": 400},
]

df = pd.DataFrame(portfolio_data)

def fetch_live_prices(stock_list):
    prices = {}

    for stock in stock_list:
        ticker = yf.Ticker(stock)
        data = ticker.history(period="1d")

        if not data.empty:
            prices[stock] = data["Close"].iloc[-1]
        else:
            prices[stock] = None

    return prices

live_prices = fetch_live_prices(df["Stock"])
df["Current_Price"] = df["Stock"].map(live_prices)

df["Investment"] = df["Quantity"] * df["Buy_Price"]
df["Current_Value"] = df["Quantity"] * df["Current_Price"]
df["Profit_Loss"] = df["Current_Value"] - df["Investment"]
df["Return_%"] = (df["Profit_Loss"] / df["Investment"]) * 100

total_investment = df["Investment"].sum()
total_current_value = df["Current_Value"].sum()
total_profit = df["Profit_Loss"].sum()
weighted_return = (total_profit / total_investment) * 100

print("\n📊 LIVE STOCK PORTFOLIO REPORT")
print(df)

print("\n📈 PORTFOLIO SUMMARY")
print("Total Investment:", round(total_investment, 2))
print("Current Value:", round(total_current_value, 2))
print("Total Profit/Loss:", round(total_profit, 2))
print("Weighted Return: {:.2f}%".format(weighted_return))

colors = ["green" if x >= 0 else "red" for x in df["Return_%"]]

plt.figure(figsize=(10,5))
plt.bar(df["Stock"], df["Return_%"], color=colors)
plt.axhline(0)
plt.xticks(rotation=45)
plt.xlabel("Stock")
plt.ylabel("Return (%)")
plt.title("Live Portfolio Performance")
plt.tight_layout()
plt.show()