#statistical learning
#Y = f(x) + E
#response from a set of features, and statistical learning is to predict
#the best function where the features and response are correlated 

#prediction is to predict response Y from the predictor X
#poor estimate is called reducible error, irreducible error is the E term

#inference is to get best form of function f

#focusing on predictive statistcal learning: creating an estimate f^ for f

#set of tuples (Xi, Yi) for each predictor as the training data

#parametric models: assume a form for function f, such as OLS (ordinary least squares)
#non parametric models: needs more data, but more flexible

#supervised model: for every Xi there is a Yi

#1) Regression: linear regression with ordinary least squares: ex) price data over last few days
#is the predictor, and response is the following day value of the SNP500

#2) Classification: ordinals (ordered) groups such as low, medium, high used in quant - 
#used for getting direction of future, not for exact time series value: log reg, SVM, ANNs

#3) Time series: ARIMA models and ARCH models
#ARIMA: model variations in absolute value of time series
#ARCH: variance (volatility) of time series over time
#Use continuous time series models: geometric brownian motion, heston stochastic volatility, 
#and Ornstein-Uhlenbeck models

#TIME SERIES ANALYSIS:

#Mean reversion: statistical tests to decide if pattern is different from a random walk
#Random walk has no memory of where it's been: random time series, while mean reverting
#has a predictable time series

#Use Ornstein-Uhlenbeck stochastic differential for this:
#states that change in price series during next time period is proportional to 
#difference of mean and current price, as well as Gaussian noise addition (brownian motion

#1) AUGMENTED DICKEY FULLER TEST 

from datetime import datetime
import pandas_datareader as web
import statsmodels.tsa.stattools as ts
import yfinance as yf

#download sample amazon data

aapl = yf.download("AAPL", datetime(2022,2,1), datetime(2023,8,1))
#datareader data from 2000 to 2015 for amazon 

print(ts.adfuller(aapl['Adj Close'], 1))
#ADF test on amazon, lag order of 1

#ADF test from statsmodels results in the test statistic (DF) and the distribution
#of the critical values at the 1,5,10 percent confidence intervals
#The statistic is larger than any of the critical values, and so we CANNOT REJECT THE NULL
#and this is a random walk: if we can reject the null, then it has mean reverting behavior


#2) STATIONARITY 

#Calculate Hurst exponent: variance of log price series compared to GBM
#In Geometric Brownian Motion (random walk), the log price variance is proportional to
#the log price itself: so this is when the Hurst exponent H = 0.5

#H < 0.5: mean reverting, H > 0.5: trending, H = 0.5: GBM

from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

def hurst(ts):
    lags = range(2,100)

    #array of variances for each lag in time series
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    #linear fit
    poly = polyfit(log(lags), log(tau), 1)

    return poly[0] * 2.0 #this is hurst exponent

#GBM, mean reverting, trending series created

gbm = log(cumsum(randn(100000))+1000)
mr = log(randn(100000)+1000)
tr = log(cumsum(randn(100000)+1)+1000)

print("Hurst(GBM):  %s" % hurst(gbm))
print("Hurst(Mean Reversion):  %s" % hurst(mr))
print("Hurst(Trending):  %s" % hurst(tr))

print("Hurst(AMZN):  %s" % hurst(aapl['Adj Close']))

#running hurst on GBM, MR, TR, and amazon adj close
#Hurst on GBM shud be .5, MR shud be 0, TR shud be 1
#How close AMZN is will tell us what is happening