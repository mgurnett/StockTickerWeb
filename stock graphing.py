# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

#description: this program uses the dual moving average croissover to determine when to buy and sell stock

#Import the libraries 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si

plt.style.use('fivethirtyeight')

# or Amazon
amzn = si.get_live_price("amzn")
amzn_data = si.get_data('amzn' , start_date = '01/01/2010')
 
# or any other ticker
tsla = si.get_live_price("tsla")
tsla_data = si.get_data('tsla' , start_date = '01/01/2010')

APPL = si.get_live_price("aapl")
APPL_data = si.get_data('aapl' , start_date = '01/01/2010')

#Visualize the data
plt.figure(figsize=(12.5, 4.5))
plt.plot(APPL_data['adjclose'], label = 'Apple' )
plt.plot(tsla_data['adjclose'], label = 'Tesla' )
plt.plot(amzn_data['adjclose'], label = 'Amazon' )
plt.title('Adj. Close Price History')
plt.xlabel('Date')
plt.ylabel('Adj. Close Price (USD)')
plt.legend(loc='upper left')
plt.show()

#Create the simple moving average witha 30day window
SMA30 = pd.DataFrame()
SMA30['Adj Close Price'] = APPL_data['adjclose'].rolling(window= 30).mean()

#Create the simple moving average with a 100 day window
SMA100 = pd.DataFrame()
SMA100['Adj Close Price'] = APPL_data['adjclose'].rolling(window= 100).mean()

#Visualize the data
plt.figure(figsize=(16.5, 4.5))
plt.plot(APPL_data['adjclose'], label = 'AAPL' )
plt.plot(SMA30['Adj Close Price'])
#plt.plot(SMA30['Adj Close Price'], lable = '30 Day')
plt.plot(SMA100['Adj Close Price'])
plt.title('Apple Adj. Close Price History')
plt.xlabel('Date')
plt.ylabel('Adj. Close Price (USD)')
plt.legend(loc='upper left')
plt.show()

#creat new dataframe to store all the data
data = pd.DataFrame()
data['AAPL'] = APPL_data['adjclose']
data['SMA30'] = SMA30['Adj Close Price']
data['SMA100'] = SMA100['Adj Close Price']

#Creat a function to signal when to buy and sell the asset/stock
def buy_sell (data):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA30'][i] > data['SMA100'][i]:
      if flag != 1:
        sigPriceBuy.append(data['AAPL'][i])
        sigPriceSell.append(np.nan)
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA30'][i] < data['SMA100'][i]:
      if flag != 0:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(data['AAPL'][i])
        flag = 0
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan)
  return (sigPriceBuy, sigPriceSell)

#Store the buy and sell data into a variable
buy_sell = buy_sell (data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#Visualize the data and the stratigy
plt.figure(figsize=(16.5, 4.5))
plt.plot(data['AAPL'], label = 'AARP', alpha = 0.35)
plt.plot(data['SMA30'], label = 'SMA30', alpha = 0.35)
plt.plot(data['SMA100'], label = 'SMA100', alpha = 0.35)
plt.scatter(data.index, data['Buy_Signal_Price'], label = 'BUY', marker = '^', color = 'green')
plt.scatter(data.index, data['Sell_Signal_Price'], label = 'SELL', marker = 'v', color = 'red')
plt.title('Apple Adj. Close Price History with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Adj. Close Price (USD)')
plt.legend(loc='upper left')

plt.show()