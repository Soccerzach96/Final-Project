## SI 206 2017
## Final Project

## Zachary Strong


## IMPORTS:
import json
import sqlite3
import datetime

## Import Coinbase API
import coinbase_info
from coinbase.wallet.client import Client
from coinbase.wallet.client import APIObject

## Import GDAX API
import gdax

### COINBASE API
## Create Client Connection to Coinbase API
client = Client(coinbase_info.api_key, coinbase_info.api_secret)

price = client.get_buy_price(currency_pair = 'BTC-USD')

# print(price.amount)


historic_Ethereum_Prices = client._make_api_object(client._get('v2', 'prices', 'ETH-USD', 'historic'), APIObject)

# print(historic_Ethereum_Prices)




### GDAX API
## Create Client Connection to GDAX API
client = gdax.PublicClient()

## Setup Crytocurrency Prices Cache
CACHE_FNAME = "historic_cryptocurrency_prices_cache.json"
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}



## Function to obtain historic Bitcoin prices
def get_bitcoin_historic_prices():
	if 'BTC-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['BTC-USD']
	else:
		print("Making a request for new data...")
		results = client.get_product_historic_rates('BTC-USD', granularity = 60*60*24*30)
		for b in results:
			unixTime = b[0]
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:11]
			b[0] = convert_unixTime
		CACHE_DICTION['BTC-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['BTC-USD']

## Function to obtain historic Ethereum prices
def get_ethereum_historic_prices():
	if 'ETH-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['ETH-USD']
	else:
		print("Making a request for new data...")
		results = client.get_product_historic_rates('ETH-USD', granularity = 60*60*24*30)
		for b in results:
			unixTime = b[0]
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:11]
			b[0] = convert_unixTime
		CACHE_DICTION['ETH-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['ETH-USD']

## Function to obtain historic Litecoin prices
def get_litecoin_historic_prices():
	if 'LTC-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['LTC-USD']
	else:
		print("Making a request for new data...")
		results = client.get_product_historic_rates('LTC-USD', granularity = 60*60*24*30)
		for b in results:
			unixTime = b[0]
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:11]
			b[0] = convert_unixTime
		CACHE_DICTION['LTC-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['LTC-USD']



## Returning Cryptocurrency Prices:
historic_Bitcoin = get_bitcoin_historic_prices()
historic_Ethereum = get_ethereum_historic_prices()
historic_Litecoin = get_litecoin_historic_prices()



## Creating Investments SQLite3 Datanase
conn = sqlite3.connect('Investments.sqlite')
cur = conn.cursor()

## Creating Bitcoin Table
cur.execute('DROP TABLE IF EXISTS Bitcoin')
cur.execute('CREATE TABLE Bitcoin (Date TEXT, Initial_Price TEXT, End_Price TEXT, Price_High TEXT, Price_Low TEXT, Volume TEXT)')
for coin in historic_Bitcoin:
	tup = coin[0], coin[3], coin[4], coin[2], coin[1], coin[5]
	cur.execute('INSERT OR IGNORE INTO Bitcoin (Date, Initial_Price, End_Price, Price_High, Price_Low, Volume) VALUES (?, ?, ?, ?, ?, ?)', tup)
conn.commit()

## Creating Ethereum Table
cur.execute('DROP TABLE IF EXISTS Ethereum')
cur.execute('CREATE TABLE Ethereum (Date TEXT, Initial_Price TEXT, End_Price TEXT, Price_High TEXT, Price_Low TEXT, Volume TEXT)')
for coin in historic_Ethereum:
	tup = coin[0], coin[3], coin[4], coin[2], coin[1], coin[5]
	cur.execute('INSERT OR IGNORE INTO Ethereum (Date, Initial_Price, End_Price, Price_High, Price_Low, Volume) VALUES (?, ?, ?, ?, ?, ?)', tup)
conn.commit()

## Creating Litecoin Table
cur.execute('DROP TABLE IF EXISTS Litecoin')
cur.execute('CREATE TABLE Litecoin (Date TEXT, Initial_Price TEXT, End_Price TEXT, Price_High TEXT, Price_Low TEXT, Volume TEXT)')
for coin in historic_Litecoin:
	tup = coin[0], coin[3], coin[4], coin[2], coin[1], coin[5]
	cur.execute('INSERT OR IGNORE INTO Litecoin (Date, Initial_Price, End_Price, Price_High, Price_Low, Volume) VALUES (?, ?, ?, ?, ?, ?)', tup)
conn.commit()





cur.close()

