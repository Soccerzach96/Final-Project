## SI 206 2017
## Final Project

## Zachary Strong


## IMPORTS:
import json
import sqlite3

## Connect to Coinbase API
import coinbase_info
from coinbase.wallet.client import Client
from coinbase.wallet.client import APIObject

## Connect to GDAX
import gdax


## Create Client Connection to Coinbase API
client = Client(coinbase_info.api_key, coinbase_info.api_secret)

price = client.get_buy_price(currency_pair = 'BTC-USD')

# print(price.amount)


historic_Ethereum_Prices = client._make_api_object(client._get('v2', 'prices', 'ETH-USD', 'historic'), APIObject)

# print(historic_Ethereum_Prices)

## Create Client Connection to GDAX API
client = gdax.PublicClient()
for product in client.get_products():
	print(product)
# currencies = client.get_products()
# print(currencies)



# Returns the Price of Bitcoin every 30 days (Reverse from today's date)
ether = client.get_product_historic_rates('ETH-USD', granularity = 60*60*24*30, start = '2015-01-05T00:00:00+00:00')
# ether = client.getProductHistoricRates('BTC-USD', {'start': "2015-01-05T00:00:00+00:00"}, {'granularity': 60*60*24*30})
for e in ether:
	print(e[3])