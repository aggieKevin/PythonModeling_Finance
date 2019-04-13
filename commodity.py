# -*- coding: utf-8 -*-
"""
@author: kevin he
"""
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import quandl


# 1. read data
start=datetime.datetime(2016,1,1)
OIL_CME_RB1=quandl.get("CHRIS/CME_RB1",start_date=start)
GAS_CME_NG1=quandl.get("CHRIS/CME_NG1",start_date=start)
GOLD_CME_GC1=quandl.get("CHRIS/CME_GC1",start_date=start)

# Index(['Open', 'High', 'Low', 'Last', 'Change', 'Settle', 'Volume','Previous Day Open Interest']

OIL_CME_RB1['Open'].plot(label='OIL_CME_RB1',figsize=(8,6),title='Open Price')
plt.legend()

OIL_CME_RB1['Volume'].plot(label='OIL_CME_RB1',figsize=(12,8),title='Volume Traded')
plt.legend()
OIL_CME_RB1['Volume'].argmax()

OIL_CME_RB1['Total Traded'] = OIL_CME_RB1['Open']*OIL_CME_RB1['Volume']
OIL_CME_RB1['Total Traded'].plot(label='OIL_CME_RB1',figsize=(12,8))
plt.legend()
plt.ylabel('Total Traded')

# 2. get average stock price, creat bollinger bands
OIL_CME_RB1['MA50'] = OIL_CME_RB1['Settle'].rolling(50).mean()
OIL_CME_RB1['upper']=OIL_CME_RB1['MA50']+3*OIL_CME_RB1['Settle'].rolling(50).std()
OIL_CME_RB1['lower']=OIL_CME_RB1['MA50']-3*OIL_CME_RB1['Settle'].rolling(50).std()
OIL_CME_RB1[['Settle','MA50','upper','lower']].plot(figsize=(10,7))

# 200 days MA and 50 days MA
OIL_CME_RB1['MA200'] = OIL_CME_RB1['Settle'].rolling(200).mean()# to find the trend
OIL_CME_RB1[['Open','MA50','MA200']].plot(label='OIL_CME_RB1',figsize=(8,4))


#3. different commodities comparision: GAS,OIL,GOLD
# GAS should have highER correlation with OIL than with GOLD
from pandas.plotting import scatter_matrix
GAS_CME_NG1=quandl.get("CHRIS/CME_NG1",start_date=start)
GOLD_CME_GC1=quandl.get("CHRIS/CME_GC1",start_date=start)

Commodity_comp = pd.concat([OIL_CME_RB1['Open'],GAS_CME_NG1['Open'],GOLD_CME_GC1['Open']],axis=1)
Commodity_comp.columns = ['OIL_CME_RB1 Open','GAS_CME_NG1 Open','GOLD_CME_GC1 Open']
scatter_matrix(Commodity_comp,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50});

OIL_CME_RB1['returns'] = (OIL_CME_RB1['Settle'] / OIL_CME_RB1['Settle'].shift(1) ) - 1
GOLD_CME_GC1['returns'] = GOLD_CME_GC1['Settle'].pct_change(1)
GAS_CME_NG1['returns'] = GAS_CME_NG1['Settle'].pct_change(1)

OIL_CME_RB1['returns'].hist(bins=100,label='OIL_CME_RB1',figsize=(10,8),alpha=0.5)
GAS_CME_NG1['returns'].hist(bins=100,label='GAS_CME_NG1',alpha=0.5)
GOLD_CME_GC1['returns'].hist(bins=100,label='GOLD_CME_GC1',alpha=0.5)
plt.legend()

# KED plot
OIL_CME_RB1['returns'].plot(kind='kde',label='OIL_CME_RB1',figsize=(12,6))
GAS_CME_NG1['returns'].plot(kind='kde',label='GAS_CME_NG1')
GOLD_CME_GC1['returns'].plot(kind='kde',label='GOLD_CME_GC1')
plt.legend()

# box plots
box_df = pd.concat([OIL_CME_RB1['returns'],GAS_CME_NG1['returns'],GOLD_CME_GC1['returns']],axis=1)
box_df.columns = ['OIL_CME_RB1 Returns',' GAS_CME_NG1 Returns','GOLD_CME_GC1 Returns']
box_df.plot(kind='box',figsize=(12,8),colormap='jet')


scatter_matrix(box_df,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50});
# compare GAS_CME_NG1 and GOLD_CME_GC1
box_df.plot(kind='scatter',x=' GAS_CME_NG1 Returns',y='OIL_CME_RB1 Returns',alpha=0.4,figsize=(10,6))
box_df.plot(kind='scatter',x=' GAS_CME_NG1 Returns',y='GOLD_CME_GC1 Returns',alpha=0.4,figsize=(10,6))

# cumulateive daily return
OIL_CME_RB1['Cumulative Return'] = (1 + OIL_CME_RB1['returns']).cumprod()
GOLD_CME_GC1['Cumulative Return'] = (1 + GOLD_CME_GC1['returns']).cumprod()
GAS_CME_NG1['Cumulative Return'] = (1 + GAS_CME_NG1['returns']).cumprod()

OIL_CME_RB1['Cumulative Return'].plot(label='OIL_CME_RB1',figsize=(16,8),title='Cumulative Return')
GOLD_CME_GC1['Cumulative Return'].plot(label='GOLD_CME_GC1')
GAS_CME_NG1['Cumulative Return'].plot(label='GAS_CME_NG1')
plt.legend()
