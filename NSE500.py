#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 07:37:21 2020

@author: hpareek1
"""
import datetime as dt
import matplotlib.pyplot as plt 
from matplotlib import style
import pandas as pd 
import pandas_datareader.data as web
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
# import os 
# import subprocess
from selenium import webdriver

start = dt.datetime(year=1990,month=1,day=1)
end = dt.date.today()


ax1 = plt.subplot2grid(((6,1)), (0,0), rowspan=5,colspan=1)
ax2 = plt.subplot2grid(((6,1)), (5,0), rowspan=1,colspan=1, sharex=ax1)

ax1.xaxis_date()

def getNSE500stockList():
    df_nse500 = pd.read_csv('/Users/hpareek1/Documents/finance/nse500/ind_nifty500list.csv',header=None,usecols=[2])
    df_nse500 =  df_nse500.drop(df_nse500.index[0])
    return df_nse500.values.tolist()


def printnse500():
    nse_500 = getNSE500stockList()
    for i in nse_500:
        print(i)
        
def getLTPStock(stockName):
    url = 'https://in.tradingview.com/symbols/NSE-'+stockName+'/'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options,executable_path='/usr/local/bin/chromedriver')
    driver.get(url)
    p_element = driver.find_element_by_class_name('tv-symbol-price-quote__value')
    print('LTP is : '+p_element.text)
    # print(var)
    
    
def getHistoricalData(period,symbolName):
    symbolName = symbolName + '.NS'
    df = web.DataReader(symbolName,'yahoo',start,end)
    df_ohlc = df['Adj Close'].resample(period).ohlc()
    df_volume = df['Volume'].resample(period).sum()
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    candlestick_ohlc(ax1, df_ohlc.values, width =2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values, 0, color='b')
    plt.show()


while True:
    try:
         print('Enter 1 for All Stock List \nEnter 2 to get LTP for Stock \nEnter 3 for Historical Data Feed to a file')
         choice = int(input('Enter your Choice '))
         # print(choice)
         if(choice==3):
             getHistoricalData(input('Enter the Period for Data: '), input('Enter the Symbol Name: '))
         if(choice==2):
             getLTPStock(input('Enter the Stock ID: '))
         if(choice==1):
             printnse500()
    except ValueError:
        print('Enter a correct Value')
   