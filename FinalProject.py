## SI 206 2017
## Final Project

## Zachary Strong


## IMPORTS:
import json
import sqlite3

## Connect to Coinbase API
import coinbase_info
from coinbase.wallet.client import client



## Create Client Connection to Coinbase API
client = Client(coinbase_info.api_key, coinbase_info.api_secret)