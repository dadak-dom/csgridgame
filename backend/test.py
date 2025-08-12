import pandas as pd
import json
import jq

with open("crawl-data.json") as f:
    data = json.load(f)

df = pd.json_normalize(data, sep='_')

result = df[(df["weapon"] == "AK-47") & (df["prices_StatTrak Factory New"] > 200)]
print(result[["weapon", "name", "prices_StatTrak Factory New"]])

print(df[(df["id"] == 10) ])#& (df["prices_StatTrak Factory New"] > 200)])

query = '.[] | select(.id == 1) | .prices'
result = jq.compile(query).input(data).all()

print(result)
