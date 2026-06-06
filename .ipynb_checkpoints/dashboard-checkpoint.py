import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# connect database
conn = sqlite3.connect("nepse.db")

# load data
df = pd.read_sql_query("SELECT * FROM market_leaders", conn)

print("Total rows:", len(df))
print(df.head())

# ---- TOP GAINERS ----
gainers = df[df["category"] == "gainer"].head(10)

plt.figure()
plt.bar(gainers["symbol"], gainers["rank"])
plt.title("Top Gainers (Rank)")
plt.xticks(rotation=45)
plt.show()

# ---- TOP LOSERS ----
losers = df[df["category"] == "loser"].head(10)

plt.figure()
plt.bar(losers["symbol"], losers["rank"])
plt.title("Top Losers (Rank)")
plt.xticks(rotation=45)
plt.show()

# ---- TURNOVER ----
turnover = df[df["category"] == "turnover"].head(10)

plt.figure()
plt.bar(turnover["symbol"], turnover["rank"])
plt.title("Top Turnover (Rank)")
plt.xticks(rotation=45)
plt.show()