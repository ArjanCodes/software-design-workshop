import datetime

import pandas as pd

s = datetime.datetime(2025, 1, 1)

d = pd.read_csv("orders.csv")
d["date"] = pd.to_datetime(d["date"])

x = []
for i in range(len(d)):
    if d.iloc[i]["date"] >= s:
        x.append(d.iloc[i])

r = 0
for row in x:
    r += row["quantity"] * row["price"]

print("Total recent revenue: €" + str(round(r, 2)))
