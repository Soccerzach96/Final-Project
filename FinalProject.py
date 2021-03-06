## SI 206 2017
## Final Project
## Zachary Strong

import json
import sqlite3
import datetime
import requests

## Import Coinbase API
import coinbase_info
from coinbase.wallet.client import Client
from coinbase.wallet.client import APIObject
## Create Client Connection to Coinbase API
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

## Import Quandl
import quandl

## Import Zillow
import zillow
import zillow_info
zillow_key = zillow_info.api_key
api = zillow.ValuationApi()

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
		return CACHE_DICTION['BTC-USD']
	else:
		## Request Historic Bitcoin Prices from past 100 days
		results = gdax_client.get_product_historic_rates('BTC-USD', granularity = 60*60*24)
		results = results[:100]
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
		return CACHE_DICTION['ETH-USD']
	else:
		## Request Historic Ethereum Prices from past 100 days
		results = gdax_client.get_product_historic_rates('ETH-USD', granularity = 60*60*24)
		results = results[:100]
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
		return CACHE_DICTION['LTC-USD']
	else:
		## Request Historic Litecoin Prices from past 100 days
		results = gdax_client.get_product_historic_rates('LTC-USD', granularity = 60*60*24)
		results = results[:100]
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

## Function to obtain Coinbase Portfolio Accounts (Coinbase)
def get_coinbase_accounts():
	if 'Coinbase_Accounts' in CACHE_DICTION:
		return CACHE_DICTION['Coinbase_Accounts']
	else:
		## Obtain Dictionary of USD, BTC, ETH, and LTC Accounts
		accounts = coinbase_client.get_accounts()
		accounts = accounts.data
		CACHE_DICTION['Coinbase_Accounts'] = accounts
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['Coinbase_Accounts']

## Function to obtain Coinbase Account Transactions (Coinbase)
def get_coinbase_transactions():
	if 'Coinbase_Transactions' in CACHE_DICTION:
		return CACHE_DICTION['Coinbase_Transactions']
	else:
		## Obtain Dictionary of USD, BTC, ETH, and LTC Accounts
		accounts = coinbase_client.get_accounts()
		transactions = list()
		## Iterate through each account and append the transactions to new list
		for account in accounts.data:
			transaction = account.get_transactions()
			transactions.append(transaction.data)
		CACHE_DICTION['Coinbase_Transactions'] = transactions
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['Coinbase_Transactions']

## Function to obtain Historic Gold Prices (Quandl)
## Dates variable used to match prices of all investments by specific dates
def get_gold_prices(dates):
	if 'Gold' in CACHE_DICTION:
		return CACHE_DICTION['Gold']
	else:
		## Connect to Gold Panda Dataset in Quandl API
		api_url = 'https://www.quandl.com/api/v1/datasets/LBMA/GOLD.json'
		## Convert Panda Dataset into JSON File
		session = requests.Session()
		raw_data = session.get(api_url)
		gold_data = raw_data.json()
		gold_data = dict(gold_data)
		historic_prices = list()
		## Create list of prices for specific dates
		for data in gold_data['data']:
			for date in dates:
				if data[0] == date:
					historic_prices.append(data)
		CACHE_DICTION['Gold'] = historic_prices
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION['Gold']

## Function to obtain Historic Stock Prices (Quandl)
## Dates variable used to match prices of all investments by specific dates
## Ticker variable from user input to determine which stock to pull data for
def get_stock_prices(dates, ticker):
	if ticker in CACHE_DICTION:
		return CACHE_DICTION[ticker]
	else:
		## Connect to Stock Panda Dataset in Quandl API
		api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % ticker
		## Convert Panda Dataset into JSON File
		session = requests.Session()
		raw_data = session.get(api_url)
		stock_data = raw_data.json()
		stock_data = dict(stock_data['dataset'])
		historic_prices = list()
		## Create list of prices for specific dates
		for data in stock_data['data']:
			for date in dates:
				if data[0] == date:
					historic_prices.append(data)
		CACHE_DICTION[ticker] = historic_prices
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION[ticker]

##
def get_property_comps(address, zipcode):
	if address in CACHE_DICTION:
		return CACHE_DICTION[address]
	else:
		data = api.GetSearchResults(zillow_key, address, zipcode)
		comps = api.GetComps(count = 25, zws_id = zillow_key, zpid = data.zpid)
		property_info_list = list()
		for comp in comps['comps']:
			individual_property = list()
			individual_property.append(comp.full_address.street)
			individual_property.append(comp.full_address.zipcode)
			individual_property.append(comp.full_address.city)
			individual_property.append(comp.full_address.state)
			individual_property.append(comp.zestiamte.amount)
			individual_property.append(comp.zestiamte.valuation_range_low)
			individual_property.append(comp.zestiamte.valuation_range_high)
			property_info_list.append(individual_property)
		CACHE_DICTION[address] = property_info_list
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION[address]



####################################################
################ FUNCTION CALLS ####################
####################################################

## Returning List of Historic Cryptocurrency Prices:
historic_Bitcoin = get_bitcoin_historic_prices()
historic_Ethereum = get_ethereum_historic_prices()
historic_Litecoin = get_litecoin_historic_prices()

## Returning List of Coinbase Transactions
coinbase_transactions = get_coinbase_transactions()

## Returning List of Coinbase Accounts
coinbase_portfolio = get_coinbase_accounts()
print('###################################')
print('#### Personal Coinbase Account ####')
print('###################################', '\n')
total_worth = 0
for account in coinbase_portfolio:
	print(account['name'])
	print('Balance: ' + account['balance']['amount'], account['balance']['currency'])
	print('Worth: ' + account['native_balance']['amount'], account['native_balance']['currency'] + '\n')
	total_worth += float(account['native_balance']['amount'])
print('Total Coinbase Worth: ', total_worth, '\n')

## Returning Current Cryptocurrency Prices:
print('###################################')
print('## Current Cryptocurrency Prices ##')
print('###################################', '\n')
current_date = gdax_client.get_time()
current_date = current_date['iso'][:10]
print('Date: ', current_date)

current_bitcoin_price = gdax_client.get_product_historic_rates('BTC-USD')[0][3]
print('Current Bitcoin Price: ', current_bitcoin_price)

current_ethereum_price = gdax_client.get_product_historic_rates('ETH-USD')[0][3]
print('Current Ethereum Price: ', current_ethereum_price)

current_litecoin_price = gdax_client.get_product_historic_rates('LTC-USD')[0][3]
print('Current Litecoin Price: ', current_litecoin_price, '\n')

## Returning List of Range of Dates for Gold Prices
dates = list()
for date in historic_Bitcoin:
	dates.append(date[0])

## Returning List of Gold Prices
historic_Gold = get_gold_prices(dates)
print('###################################')
print('###### Current Price of Gold ######')
print('###################################', '\n')
print('Current Price of Gold: ', historic_Gold[0][1], '\n')

## Returning List of Stock Prices
print('###################################')
print('###### Current Price of Stock #####')
print('###################################', '\n')
stock_name = input('Ticker of Stock: ')
stock_info = get_stock_prices(dates, stock_name)
print('Current Price of', stock_name, ':', stock_info[0][1], '\n')

## Returning Comps of Desired Property
print('###################################')
print('######## Comps of Property ########')
print('###################################', '\n')
print('Format of User Input: 1523 Maryland Blvd, Birmingham, MI')
zillow_address = input('Property Address: ')
zillow_zipcode = input('Property Zipcode: ')
property_info = get_property_comps(zillow_address, zillow_zipcode)

data = api.GetSearchResults(zillow_key, zillow_address, zillow_zipcode)
zestimate = api.GetZEstimate(zws_id = zillow_key, zpid = data.zpid)
property_valuation = zestimate.zestiamte.amount
print('\n')
print("Valuation of Property: $", property_valuation)
print("Look at SQLite3 Table for Addresses and Valuations of Comps", '\n')



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

## Creating Gold Table
cur.execute('DROP TABLE IF EXISTS Gold')
cur.execute('CREATE TABLE Gold (Date TEXT, USD_Price INT)')
for gold in historic_Gold:
	tup = gold[0], gold[1]
	cur.execute('INSERT OR IGNORE INTO Gold (Date, USD_Price) VALUES (?, ?)', tup)
conn.commit()

## Creating Stock Table
cur.execute('DROP TABLE IF EXISTS Stock')
cur.execute('CREATE TABLE Stock (Date TEXT, Trading_Price INT)')
for stock in stock_info:
	tup = stock[0], stock[1]
	cur.execute('INSERT OR IGNORE INTO Stock (Date, Trading_Price) VALUES (?, ?)', tup)
conn.commit()

## Creating Property Table
cur.execute('DROP TABLE IF EXISTS Property')
cur.execute('CREATE TABLE Property (Street TEXT, Zipcode TEXT, City TEXT, State TEXT, ZEstimate INT, Valuation_Range_Low INT, Valuation_Range_High INT)')
for comp in property_info:
	tup = comp[0], comp[1], comp[2], comp[3], comp[4], comp[5], comp[6]
	cur.execute('INSERT OR IGNORE INTO Property (Street, Zipcode, City, State, ZEstimate, Valuation_Range_Low, Valuation_Range_High) VALUES (?, ?, ?, ?, ?, ?, ?)', tup)
conn.commit()



####################################################
############## Data Visualization ##################
####################################################

############# Coinbase Portfolio Pie Chart #########

## Pull Coinbase Account Names and Values
cur.execute("SELECT Account_Name FROM Coinbase_Accounts")
portfolio_accounts = cur.fetchall()

cur.execute("SELECT Account_Value FROM Coinbase_Accounts")
portfolio_value = cur.fetchall()

## Setup Portfolio Distribution Pie Chart
trace = go.Pie(labels = portfolio_accounts, values = portfolio_value)
py.iplot([trace], filename = 'coinbase_portfolio_piechart')


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

## Pull Litecoin Trades and Calculate Single Litecoin Price at Time of Trade
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

## Pull Historic Gold Prices
cur.execute("SELECT Date FROM Gold")
g_dates = cur.fetchall()
cur.execute("SELECT USD_Price FROM Gold")
g_prices = cur.fetchall()

trace6 = go.Scatter(x = g_dates, y = g_prices, mode = 'lines', name = 'Gold Prices')

## Pull Historic Stock Prices
cur.execute("SELECT Date FROM Stock")
stock_dates = cur.fetchall()
cur.execute("SELECT Trading_Price FROM Stock")
stock_prices = cur.fetchall()

trace7 = go.Scatter(x = stock_dates, y = stock_prices, mode = 'lines', name = stock_name + ' Prices')

data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7]

layout = dict(title = 'Investment Prices and Portfolio', yaxis = dict(title = 'PRICE'), xaxis = dict(title = 'DATE'))
fig = dict(data = data, layout = layout)
py.iplot(fig, filename = 'Investment_Graph')




cur.close()