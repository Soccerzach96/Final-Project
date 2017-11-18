## SI 206 2017
## Final Project

## Zachary Strong


## IMPORTS:
import json
import sqlite3

## APIs to Be Used:
##		- Facebook
##		- GitHub
##		- Instagram
##		- Gmail
##		- YouTube

## Visualization Tools to Be Used:
##		- Pandas
##		- Google Maps


## Caching Setup:
##		- 100 interactions needed (posts, emails, commits, likes, etc.)

CACHE_FNAME = "206_APIsAndDBs_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}

# Define your function get_user_tweets here:
def get_user_tweets(user):
	if user in CACHE_DICTION:
		print("Data was in the cache")
		return CACHE_DICTION[user]
	else:
		print("Making a request for new data...")
		results = api.user_timeline(user)
		CACHE_DICTION[user] = results
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return CACHE_DICTION[user]

## Function to Find Days Interactions Took Place (Sunday - Monday):

## Write Data to Database:

## REPORT:
##		- Screen display, file output, etc.
##		- Shows how active you are on each day on the site