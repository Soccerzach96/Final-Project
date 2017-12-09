## SI 206 2017
## Final Project
## Zachary Strong

import json
import sqlite3
import datetime

## Import Coinbase API
import coinbase_info
from coinbase.wallet.client import Client
from coinbase.wallet.client import APIObject
## Creat Client Connection to Coinbase API
coinbase_client = Client(coinbase_info.api_key, coinbase_info.api_secret)

## Import GDAX API (Bitcoin, Ethereum, Litecoin)
import gdax
## Create Client Connection to GDAX API
gdax_client = gdax.PublicClient()


## Setup Investments Cache
CACHE_FNAME = "investments_cache.json"
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}



####################################################
################### FUNCTIONS ######################
####################################################

## Function to obtain historic Bitcoin prices (GDAX)
def get_bitcoin_historic_prices():
	if 'BTC-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['BTC-USD']
	else:
		print("Making a request for new data...")
		## Request Historic Bitcoin Prices in intervals of 30 days
		results = gdax_client.get_product_historic_rates('BTC-USD', granularity = 60*60*24*30)
		for b in results:
			## Convert Given Unixtime into Datetime
			unixTime = b[0]
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:10]
			b[0] = convert_unixTime
		CACHE_DICTION['BTC-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['BTC-USD']

## Function to obtain historic Ethereum prices (GDAX)
def get_ethereum_historic_prices():
	if 'ETH-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['ETH-USD']
	else:
		print("Making a request for new data...")
		## Request Historic Ethereum Prices in intervals of 30 days
		results = gdax_client.get_product_historic_rates('ETH-USD', granularity = 60*60*24*30)
		for b in results:
			## Convert Given Unixtime into Datetime
			unixTime = b[0]
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:10]
			b[0] = convert_unixTime
		CACHE_DICTION['ETH-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['ETH-USD']

## Function to obtain historic Litecoin prices (GDAX)
def get_litecoin_historic_prices():
	if 'LTC-USD' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['LTC-USD']
	else:
		print("Making a request for new data...")
		## Request Historic Litecoin Prices in intervals of 30 days
		results = gdax_client.get_product_historic_rates('LTC-USD', granularity = 60*60*24*30)
		for b in results:
			## Convert Given Unixtime into Datetime
			unixTime = int(b[0])
			convert_unixTime = datetime.datetime.utcfromtimestamp(unixTime)
			convert_unixTime = str(convert_unixTime)
			convert_unixTime = convert_unixTime[:10]
			b[0] = convert_unixTime
		CACHE_DICTION['LTC-USD'] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['LTC-USD']

## Function to obtain Coinbase Portfolio Accounts
def get_coinbase_accounts():
	if 'Coinbase_Accounts' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['Coinbase_Accounts']
	else:
		print("Making a request for new data...")
		accounts = coinbase_client.get_accounts()
		accounts = accounts.data
		CACHE_DICTION['Coinbase_Accounts'] = accounts
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['Coinbase_Accounts']

def get_coinbase_transactions():
	if 'Coinbase_Transactions' in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION['Coinbase_Transactions']
	else:
		print("Making a request for new data...")
		accounts = coinbase_client.get_accounts()
		transactions = list()
		for account in accounts.data:
			transaction = account.get_transactions()
			transactions.append(transaction.data)
		CACHE_DICTION['Coinbase_Transactions'] = transactions
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['Coinbase_Transactions']



####################################################
################ FUNCTION CALLS ####################
####################################################

## Returning List of Cryptocurrency Prices:
historic_Bitcoin = get_bitcoin_historic_prices()
historic_Ethereum = get_ethereum_historic_prices()
historic_Litecoin = get_litecoin_historic_prices()

## Returning Current Cryptocurrency Prices:
current_bitcoin_price = gdax_client.get_product_historic_rates('BTC-USD')[0][3]
current_ethereum_price = gdax_client.get_product_historic_rates('ETH-USD')[0][3]
current_litecoin_price = gdax_client.get_product_historic_rates('LTC-USD')[0][3]

## Returning List of Coinbase Accounts
coinbase_portfolio = get_coinbase_accounts()
for account in coinbase_portfolio:
	print(account['name'])
	print('Balance: ' + account['balance']['amount'], account['balance']['currency'])
	print('Worth: ' + account['native_balance']['amount'], account['native_balance']['currency'] + '\n')

## Returning List of Coinbase Transactions
coinbase_transactions = get_coinbase_transactions()

# exchange_rates = coinbase_client.get_exchange_rates()


# print(current_bitcoin_price, current_ethereum_price, current_litecoin_price)

# accounts = coinbase_client.get_accounts()
# for account in accounts.data:
# 	balance = account.balance
# 	print(account.name, balance.amount, balance.currency)
# 	print(account.get_transactions())

# for account in coinbase_portfolio:
# 	print(account[1])




####################################################
############## SQL DATABASE SETUP ##################
####################################################

## Creating Investments SQLite3 Datanase
conn = sqlite3.connect('Investments.sqlite')
cur = conn.cursor()

## Creating Coinbase Accounts Table
cur.execute('DROP TABLE IF EXISTS Coinbase_Accounts')
cur.execute('CREATE TABLE Coinbase_Accounts (Account_Name TEXT, Account_Balance INT, Account_Value INT)')
for account in coinbase_portfolio:
	tup = account['name'], account['balance']['amount'], account['native_balance']['amount']
	cur.execute('INSERT OR IGNORE INTO Coinbase_Accounts (Account_Name, Account_Balance, Account_Value) VALUES (?, ?, ?)', tup)
conn.commit()

## Creating Coinbase Transactions Table
# cur.execute('DROP TABLE IF EXISTS Coinbase_Transactions')
# cur.execute('CREATE TABLE Coinbase_Transactions (Account_Name TEXT, Account_Balance INT, Account_Value INT)')
# for account in coinbase_portfolio:
# 	tup = account['name'], account['balance']['amount'], account['native_balance']['amount']
# 	cur.execute('INSERT OR IGNORE INTO Coinbase_Transactions (Account_Name, Account_Balance, Account_Value) VALUES (?, ?, ?)', tup)
# conn.commit()

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














# import python_forex_quotes
# import forge_info

# client_1forge = python_forex_quotes.ForexDataClient(forge_info.api_key)
# conversion = client_1forge.convert('EUR', 'USD', 100)
# print(conversion)

# historic_Stock = quandl.get_table('WIKI/PRICES', ticker = 'FB')
# print(historic_Stock)

# ## Function to obtain Quandl Information
# def get_stock_historic_prices(stock):
# 	if stock in CACHE_DICTION:
# 		print("Data was in the cache")
# 		return CACHE_DICTION[stock]
# 	else:
# 		print("Making a request for new data...")
# 		results = quandl.get_table('WIKI/PRICES', ticker = stock)
# 		CACHE_DICTION[stock] = results.to_json()
# 		f = open(CACHE_FNAME, "w")
# 		f.write(json.dumps(CACHE_DICTION))
# 		f.close()
# 		return CACHE_DICTION[stock]

## Function to obtain Quandl Information
# def get_stock_historic_prices(stock):
# 	if stock in CACHE_DICTION:
# 		print("Data was in the cache")
# 		return CACHE_DICTION[stock]
# 	else:
# 		print("Making a request for new data...")
# 		results = quandl.get_table('WIKI/PRICES', ticker = stock)
# 		CACHE_DICTION[stock] = str(results)
# 		f = open(CACHE_FNAME, "w")
# 		f.write(json.dumps(CACHE_DICTION))
# 		f.close()
# 		return CACHE_DICTION[stock]

# results = quandl.get_table('WIKI/PRICES', ticker = 'AAPL')
# s = results.to_json()
# print(type(s))



## Quandl
# current_CrudeOil = quandl.get("EIA/PET_RWTC_D")
# stock_price = quandl.Dataset('WIKI/AAPL').data()
# print(stock_price)
# test = quandl.get_table('WIKI/PRICES', ticker = 'AAPL')
# print(test)

# results = quandl.get_table('WIKI/PRICES', ticker = 'AAPL')
# s = results.to_json()
# print(type(s))
# s = json.loads(results.T.to_json()).values()
# ss = dict(s)
# print(ss.keys)

# historic_Stock = get_stock_historical_prices('APPL')
# print(historic_Stock)