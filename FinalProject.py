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

## Import Plot.ly
import plotly_info
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username = plotly_info.username, api_key = plotly_info.api_key)



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
		print(type(results))
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

## Returning List of Coinbase Transactions
coinbase_transactions = get_coinbase_transactions()

## Returning List of Coinbase Accounts
coinbase_portfolio = get_coinbase_accounts()
for account in coinbase_portfolio:
	print(account['name'])
	print('Balance: ' + account['balance']['amount'], account['balance']['currency'])
	print('Worth: ' + account['native_balance']['amount'], account['native_balance']['currency'] + '\n')

## Returning Current Cryptocurrency Prices:
current_date = gdax_client.get_time()
current_date = current_date['iso'][:10]
print('Date: ', current_date)

current_bitcoin_price = gdax_client.get_product_historic_rates('BTC-USD')[0][3]
print('Current Bitcoin Price: ', current_bitcoin_price)

current_ethereum_price = gdax_client.get_product_historic_rates('ETH-USD')[0][3]
print('Current Ethereum Price: ', current_ethereum_price)

current_litecoin_price = gdax_client.get_product_historic_rates('LTC-USD')[0][3]
print('Current Litecoin Price: ', current_litecoin_price)



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
cur.execute('DROP TABLE IF EXISTS Coinbase_Transactions')
cur.execute('CREATE TABLE Coinbase_Transactions (Date TEXT, Buy_or_Sell TEXT, Cryptocurrency TEXT, Cryptocurrency_Amount INT, USD_Amount INT)')
for account in coinbase_transactions:
	for transaction in account:
		tup = transaction['created_at'][:10], transaction['type'], transaction['amount']['currency'], transaction['amount']['amount'], transaction['native_amount']['amount']
		cur.execute('INSERT OR IGNORE INTO Coinbase_Transactions (Date, Buy_or_Sell, Cryptocurrency, Cryptocurrency_Amount, USD_Amount) VALUES (?, ?, ?, ?, ?)', tup)
conn.commit()

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



####################################################
############## Data Visualization ##################
####################################################

############# Coinbase Portfolio Pie Chart #########

## Pull Coinbase Account Names and Values
# cur.execute("SELECT Account_Name FROM Coinbase_Accounts")
# portfolio_accounts = cur.fetchall()
# print(portfolio_accounts)

# cur.execute("SELECT Account_Value FROM Coinbase_Accounts")
# portfolio_value = cur.fetchall()
# print(portfolio_value)

# ## Setup Portfolio Distribution Pie Chart
# trace = go.Pie(labels = portfolio_accounts, values = portfolio_value)
# py.iplot([trace], filename = 'coinbase_portfolio_piechart')


####### Coinbase Portfolio vs. GDAX Prices #########

## Pull Bitcoin Trades and Calculate Single Bitcoin Price at Time of Trade
cur.execute("SELECT Date, Cryptocurrency_Amount, USD_Amount FROM Coinbase_Transactions WHERE Cryptocurrency == 'BTC'")
b_trades = cur.fetchall()
b_trades = list(b_trades)
bitcoin_trades = list()
for trade in b_trades:
	trade = list(trade)
	trade.append(trade[2]/trade[1])
	bitcoin_trades.append(trade)
bitcoin_dates = list()
bitcoin_price = list()
for trade in bitcoin_trades:
	bitcoin_dates.append(trade[0])
	bitcoin_price.append(trade[3])

trace0 = go.Scatter(x = bitcoin_dates, y = bitcoin_price, mode = 'markers', name = 'Bitcoin Transactions')

cur.execute("SELECT Date, End_Price FROM Bitcoin")
historical_bitcoin = cur.fetchall()
h_bitcoin_dates = list()
h_bitcoin_prices = list()
h_bitcoin_dates.append(current_date)
h_bitcoin_prices.append(current_bitcoin_price)
for date in historical_bitcoin:
	h_bitcoin_dates.append(date[0])
	h_bitcoin_prices.append(date[1])

trace1 = go.Scatter(x = h_bitcoin_dates, y = h_bitcoin_prices, mode = 'lines', name = 'Bitcoin Prices')

## Pull Ethereum Trades and Calculate Single Ethereum Price at Time of Trade
cur.execute("SELECT Date, Cryptocurrency_Amount, USD_Amount FROM Coinbase_Transactions WHERE Cryptocurrency == 'ETH'")
e_trades = cur.fetchall()
e_trades = list(e_trades)
ethereum_trades = list()
for trade in e_trades:
	trade = list(trade)
	trade.append(trade[2]/trade[1])
	ethereum_trades.append(trade)
ethereum_dates = list()
ethereum_price = list()
for trade in ethereum_trades:
	ethereum_dates.append(trade[0])
	ethereum_price.append(trade[3])

trace2 = go.Scatter(x = ethereum_dates, y = ethereum_price, mode = 'markers', name = 'Ethereum Transactions')

cur.execute("SELECT Date, End_Price FROM Ethereum")
historical_ethereum = cur.fetchall()
h_ethereum_dates = list()
h_ethereum_prices = list()
h_ethereum_dates.append(current_date)
h_ethereum_prices.append(current_ethereum_price)
for date in historical_ethereum:
	h_ethereum_dates.append(date[0])
	h_ethereum_prices.append(date[1])

trace3 = go.Scatter(x = h_ethereum_dates, y = h_ethereum_prices, mode = 'lines', name = 'Ethereum Prices')

# ## Pull Litecoin Trades and Calculate Single Litecoin Price at Time of Trade
cur.execute("SELECT Date, Cryptocurrency_Amount, USD_Amount FROM Coinbase_Transactions WHERE Cryptocurrency == 'LTC'")
l_trades = cur.fetchall()
l_trades = list(l_trades)
litecoin_trades = list()
for trade in l_trades:
	trade = list(trade)
	trade.append(trade[2]/trade[1])
	litecoin_trades.append(trade)
litecoin_dates = list()
litecoin_price = list()
for trade in litecoin_trades:
	litecoin_dates.append(trade[0])
	litecoin_price.append(trade[3])

trace4 = go.Scatter(x = litecoin_dates, y = litecoin_price, mode = 'markers', name = 'Litecoin Transactions')

cur.execute("SELECT Date, End_Price FROM Litecoin")
historical_litecoin = cur.fetchall()
h_litecoin_dates = list()
h_litecoin_prices = list()
h_litecoin_dates.append(current_date)
h_litecoin_prices.append(current_litecoin_price)
for date in historical_litecoin:
	h_litecoin_dates.append(date[0])
	h_litecoin_prices.append(date[1])

trace5 = go.Scatter(x = h_litecoin_dates, y = h_litecoin_prices, mode = 'lines', name = 'Litecoin Prices')


data = [trace0, trace1, trace2, trace3, trace4, trace5]

layout = dict(title = 'Cryptocurrency Prices and Portfolio', yaxis = dict(zeroline = False), xaxis = dict(zeroline = False))
fig = dict(data = data, layout = layout)
py.iplot(fig, filename = 'Cryptocurrency_Graph')




cur.close()