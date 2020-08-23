# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 22:09:50 2018

@author: kevin he
"""
# import modules
#import numpy as np
import pandas as pd
#import pandas_datareader.data as web
import datetime
#import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
#import scipy.stats as sts
import matplotlib.pyplot as plt
# initialize setting
pd.set_option('display.max_columns',8)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# get data of PDD and JD
start=datetime.datetime(2018,7,26)
PDD=yf.download('PDD',start)
JD=yf.download('JD',start)

PDD_latestPrice=PDD['Close'][-1]
PDD_shareOutstanding=1.11 # Billion, ADS
PDD_marketCap=PDD_shareOutstanding*PDD['Close']


JD_latestPrice=JD['Close'][-1]
JD_shareOutstanding=1.45 # billion, ADS
JD_marketCap=JD_shareOutstanding*JD['Close']

# strategy:
rational_leverage_low=1.2
rational_leverage_high=1.5

 # how many times the market value of JD should be that of PDD
#print('assume rational_leverage should be:',rational_leverage)

actual_leverage=round(JD_marketCap/PDD_marketCap,2)

plt.figure(figsize=(12,7))
actual_leverage.plot() 
plt.axhline(y=1.5,color='r',linestyle='-',label='ratio=1.5')
plt.axhline(y=1.2,color='y',linestyle='-',label='ratio=1.2')
plt.legend()

if actual_leverage[-1]<rational_leverage_low:
    print('the actual_leverage is {0}, PDD is overvalued'.format(actual_leverage))   
elif actual_leverage[-1]>rational_leverage_high:
    print('the actual_leverage is {0}, JD is overvalued'.format(actual_leverage))



# JD market value be 1.5 of PDD