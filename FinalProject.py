## SI 206 2017
## Final Project

## Zachary Strong


## IMPORTS:
import json
import sqlite3

## Connect to Coinbase API
import coinbase_info
from coinbase.wallet.client import Client


## Create Client Connection to Coinbase API
client = Client(coinbase_info.api_key, coinbase_info.api_secret)

price = client.get_buy_price(currency_pair = 'BTC-USD')

print(price)