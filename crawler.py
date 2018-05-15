#cryptonews crawler using the NEWS API
#this py file is used as a module for bot.py

import time
import json
import requests
import datetime
from secrets import NEWSAPIKEY
from bs4 import BeautifulSoup

def getOldestDate():
	"""
	function that determine the date limit from the current date
	"""
	oldestYear = time.localtime().tm_year
	oldestMonth = time.localtime().tm_mon
	oldestDay = time.localtime().tm_mday

	if oldestDay - 2 <= 0:
		oldestMonth = oldestMonth - 1
		oldestDay = 28
	else:
		oldestDay -= 2
	if oldestMonth == 0:
		oldestMonth = 12
		oldestYear = oldestYear - 1

	return datetime.date(oldestYear, oldestMonth, oldestDay) 



def getNews(keyword, 
	currDate = datetime.date(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday), 
	limitDate = getOldestDate()):
	"""
	request the news given the parameter keyword and return it in a json format
	keyword is obtained by the tweet
	currDate is the current date
	limitDate is the date a week ago from currDate

	both currDate and limitDate can be used to limit the search	
	"""
	r = requests.get('https://newsapi.org/v2/everything?q={}&from={}&to={}&sortBy=popularity&apiKey={}'.format(keyword, limitDate, currDate, NEWSAPIKEY)).json()
	return json.loads(json.dumps(r))

















