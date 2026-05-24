import requests
import pandas as pd
from datetime import datetime
from database.db_config import engine

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
data = response.json()

records = []

for coin in data:
    records.append({
        "coin_name": coin["name"],
        "symbol": coin["symbol"],
        "current_price": coin["current_price"],
        "market_cap": coin["market_cap"],
        "total_volume": coin["total_volume"],
        "price_change_24h": coin["price_change_percentage_24h"],
        "timestamp": datetime.now()
    })

df = pd.DataFrame(records)

df.to_sql(
    "crypto_prices",
    engine,
    if_exists="append",
    index=False
)

print("Data inserted successfully")