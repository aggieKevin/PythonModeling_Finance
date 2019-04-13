# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 17:11:18 2018

@author: kevin he
"""

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import scipy.stats as sts

pd.set_option('display.max_columns',8)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def countPosAndNeg(df): 
    pos=0
    neg=0
    for i in df:
        if i >0:
            pos+=1
    for i in df:
        if i<=0:
            neg+=1
    return pos,neg

start=datetime.datetime(2016,1,1)
#end=
# 1. read data
PDD=yf.download('PDD',start)


PDD['Close'].plot()
(PDD['Volume']/pow(10,7)*5).plot()
plt.legend()
PDD[['Close','Volume']].corr()
sts.linregress(PDD['Close'],PDD['Volume'])
PDDS=PDD.shift(1) # one day late
#second day open - first day close
open2Close1=PDD['Open']-PDDS['Close']

# second day high - first day close
high2Close1=PDD['High']-PDDS['Close']

# second day low - first day close
low2Close1=PDD['Low']-PDDS['Close']
plt.plot(high2Close1)
plt.axhline(y=0,color='r',linestyle='-')

plt.plot(low2Close1)
plt.axhline(y=0,color='r',linestyle='-')
plt.plot(open2Close1)
plt.axhline(y=0,color='r',linestyle='-')
open2Close1.plot()
plt.figure()
open2Close1.hist()
pos=0
neg=0
open2Close1.dropna(inplace=True)
pos,neg=countPosAndNeg(open2Close1)
# day high - day open
HighMinusOpen=PDD['High']-PDD['Open']
sortedHighMinusOpen=sorted(HighMinusOpen)
plt.figure()
HighMinusOpen.hist(bins=100)
# day close - day open
CloseMinusOpen=PDD['Close']-PDD['Open']
sortedCloseMinusOpen=sorted(CloseMinusOpen)
CloseMinusOpen.hist(bins=50)
# day open - day low
OpenMinusLow=PDD['Open']-PDD['Low']
OpenMinusLow.hist(bins=50)

plt.figure()
plt.plot(HighMinusOpen)
plt.axhline(y=0,color='r',linestyle='-')
plt.plot(OpenMinusLow)
plt.axhline(y=0,color='r',linestyle='-')
countPosAndNeg(CloseMinusOpen)

