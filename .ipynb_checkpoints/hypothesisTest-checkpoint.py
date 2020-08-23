# -*- coding: utf-8 -*-
"""
@author: kevin he
"""
# use this case to test the mean return of stock TSLA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import fix_yahoo_finance as yf
import scipy.stats

# initialize the setting
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

start_date=datetime.date(2017,1,1)
end_date=datetime.date(2018,6,30)
STOCK_NAME='TSLA'
stock=yf.download(STOCK_NAME,start_date,end_date) # download the data 


stock_return=stock['Close'].pct_change()[1:]
plt.figure(figsize=(12,8))
plt.plot(stock_return,label='daily return of Tesla')
plt.ylabel('return')
plt.legend(loc='best')
# draw the shape of normal distribution
x=np.linspace(-5,5,100)
y=scipy.stats.norm(0,1).pdf(x) # because sample size is very large, use normal distribution
plt.figure(figsize=(12,8))
plt.plot(x,y)
plt.fill_between(x,0,y,where=x>1.96,color='blue' )
plt.fill_between(x,0,y,where=x<-1.96,color='blue' )
plt.title('95% confidence')
plt.xlabel('x')
plt.ylabel('P(x)')
plt.legend('normal distribution')
plt.legend(loc='best')

# test statistic. H0 hypothesis:  mean of return is equl to 0
l=len(stock_return)
test=(stock_return.mean()-0)/(stock_return.std()/np.sqrt(l))
print('t test: ', test)
p_value=(1-scipy.stats.norm(0,1).cdf(test)) * 2
print('p-value is: {:.4f}'.format(p_value))
plt.axvline(x=p_value,color='r',label='p_value:{:.4f}'.format(p_value))
plt.legend(loc='center')

# Conclusion: 
# p_value is 0.2355, much larger than 0.05, so we cannot reject the hypothesis. 

