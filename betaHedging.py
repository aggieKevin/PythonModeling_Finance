# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 11:36:35 2018

@author: hejia
"""

import numpy as np
from statsmodels import regression
import fix_yahoo_finance as yf
import datetime
import matplotlib.pyplot as plt
#import  mysql_object

#mysql=mysql_object.mysqlOperation()

start=datetime.date(2018,6,1)
stock='AMZN'
index='SPY'

asset=yf.download(stock,start)['Close']
bench=yf.download(index,start)['Close']
asset_return = asset.pct_change()[1:]
bench_return = bench.pct_change()[1:]

plt.figure()
asset_return.plot(figsize=(12,7),label=stock)
bench_return.plot(label=index)
plt.ylabel('Daily return')
plt.legend()

# regression
x=bench_return.values
y=asset_return.values
pl=np.polyfit(x,y,1)
beta,alpha=[round(i,4) for i in pl]
print('alpha is: {0}, beta is: {1}'.format(alpha,beta))

plt.figure(figsize=(12,7))
x2=np.linspace(x.min(),x.max(),100)
y_regression=np.polyval(pl,x2)
plt.scatter(x,y,alpha=0.5)
plt.plot(x2,y_regression,'r')
plt.legend()

# hedgeing by short bench
plt.figure(figsize=(12,7))
portfolio=-1* beta*bench_return+ asset_return
portfolio.name='Tsla hedge with bench'
portfolio.plot(alpha=1,label=portfolio.name,color='r')
asset_return.plot(alpha=0.5,label=stock,color='b')
bench_return.plot(alpha=0.5,label=index,color='y')
plt.legend()

# alpha, beta after hedge
y2=portfolio.values
pl2=np.polyfit(x,y2,1)
beta2,alpha2=[round(i,4) for i in pl2]
print('alpha2 is: {0}, beta2 is: {1}'.format(alpha2,beta2))

