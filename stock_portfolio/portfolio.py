import pandas as pd
import matplotlib.pyplot as plt

#Sample Data

data = [
    {"Stock": "TCS", "Quantity": 10, "Buy_Price": 3000, "Current_Price": 3500},
    {"Stock": "INFY", "Quantity": 15, "Buy_Price": 1400, "Current_Price": 1350},
    {"Stock": "HDFCBANK", "Quantity": 20, "Buy_Price": 1500, "Current_Price": 1650},
    {"Stock": "RELIANCE", "Quantity": 8, "Buy_Price": 2500, "Current_Price": 2400},
]

df = pd.DataFrame(data)

# Financial Calculations

df["Investment"] = df["Quantity"] * df["Buy_Price"]
df["Current_Value"] = df["Quantity"] * df["Current_Price"]
df["Profit_Loss"] = df["Current_Value"] - df["Investment"]
df["Return_%"] = (df["Profit_Loss"] / df["Investment"]) * 100

# ------------------------------
# Portfolio Summary
# ------------------------------

total_investment = df["Investment"].sum()
total_current_value = df["Current_Value"].sum()
total_profit = df["Profit_Loss"].sum()
weighted_return = (total_profit / total_investment) * 100

print("\n📊 STOCK PORTFOLIO REPORT")
print(df)

print("\n📈 PORTFOLIO SUMMARY")
print("Total Investment:", total_investment)
print("Current Value:", total_current_value)
print("Total Profit/Loss:", total_profit)
print("Weighted Return: {:.2f}%".format(weighted_return))


# Underperformers

underperformers = df[df["Return_%"] < 0]
print("\n Underperforming Stocks:")
print(underperformers[["Stock", "Return_%"]])

# Visualization
# ------------------------------

plt.figure()
plt.bar(df["Stock"], df["Return_%"])
plt.xlabel("Stock")
plt.ylabel("Return (%)")
plt.title("Stock Return Comparison")
plt.show()

