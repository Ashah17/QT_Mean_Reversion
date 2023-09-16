#Idea: identify mean reverting stocks during period of last 5 years (after COVID drop)
#in an economy that seems to be in recovery.
#1) Pull the SnP 500 ticker symbols from the symbol database: use 75 random
#2) Using yfinance perform ADF tests to get a list of stocks where null hypothesis can be reject
#which are the stocks whose time series are not acting as a random walk
#3) Calculate the Herst exponent and compare the mean reverting stocks to the results of the ADF test

import pandas as pd
import numpy as np
import pymysql as pymy
import yfinance as yf #yahoo data
import statsmodels.tsa.stattools as tsa #time series
from datetime import datetime
import random

db_host = "localhost"
db_user = "root"
db_pass = "hopkinton"
db_name = "securities_master"

con = pymy.connect(
    host = db_host,
    user = db_user,
    password = db_pass,
    db = db_name
)

def ticker_list():
    cur = con.cursor()
    cur.execute (
        """SELECT ticker FROM symbol
        """
    )
    tickers = cur.fetchall()
    return tickers

#selected tickers from SQL database with code above, now format it correctly

list_of_tickers = [] #add to this list

for ticker in ticker_list():
    ticker = str(ticker[0]) #taking first from tuple, so just ticker name not the comma
    list_of_tickers.append(ticker) #added to list

#stock data for last 5 years for all tickers
#list_of_tickers = random.sample(list_of_tickers, 50)

list_of_tickers = random.sample(list_of_tickers, 75)

good_list = []

for ticker in list_of_tickers:
    curr_data = yf.download(ticker, datetime(2019, 1, 1), datetime(2023, 1, 1))
    ts = tsa.adfuller(curr_data["Adj Close"], 1)

    #ts[0] is the statistic
    #ts[4] is the dictionary with confidence interval t values
    stat = ts[0]
    onePercent = ts[4].get('1%')
    fivePercent = ts[4].get('5%')
    tenPercent = ts[4].get('10%')

    if(stat < onePercent):
        decision = "Reject on 1 percent confidence interval"
    elif(stat < fivePercent):
        decision = "Reject on 5 percent confidence interval"
    elif(stat < tenPercent):
        decision = "Reject on 10 percent confidence interval"
    else:
        decision = "Random Walk"

    if(decision != "Random Walk"):
        good_list.append(ticker) #add ticker if it is not a random walk

#do with these 3 for now

print(good_list) 

#ADF tests successful, run Herst exponent
