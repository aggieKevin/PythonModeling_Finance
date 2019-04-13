# -*- coding: utf-8 -*-
"""
@author: kevin he
"""
#------Use CAMP to find the optimum Portofolio
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import fix_yahoo_finance as fix

start=datetime.date(2017,1,1)

# create portfolio
AAPL=fix.download('AAPL',start)
CISCO=fix.download('CSCO',start)
IBM=fix.download('IBM',start)
AMZN=fix.download('AMZN',start)

#normalize price
for stock_df in (AAPL,CISCO,IBM,AMZN):
    stock_df['Normed Return']=stock_df['Adj Close']/stock_df.iloc[0]['Adj Close']
AAPL.head()

for stock_df,allo in zip([AAPL,CISCO,IBM,AMZN],[0.3,0.2,0.4,0.1]):
    stock_df['Allocation']=stock_df['Normed Return']*allo
    
# Initialize investment, with origial value at 10,000
investment=10000
for stock_df in (AAPL,CISCO,IBM,AMZN):
    stock_df['Position Values']=stock_df['Allocation']*investment

portfolio=pd.concat([AAPL['Position Values'],CISCO['Position Values'],\
                     IBM['Position Values'],AMZN['Position Values']],axis=1)
portfolio.columns=['AAPL','CISCO','IBM','AMZN']
portfolio['Total']=portfolio.sum(axis=1)
portfolio.plot(figsize=(10,8))

# daily return
portfolio['Daily Return']=portfolio['Total'].pct_change(1)
portfolio['Daily Return'].mean()
portfolio['Daily Return'].std()

# porftfolio optimization
stocks=pd.concat([AAPL['Adj Close'],CISCO['Adj Close'],IBM['Adj Close'],\
                  AMZN['Adj Close']],axis=1)
stocks.columns=['AAPL','CISCO','IBM','AMZN']
daily_change=stocks.pct_change(1)
daily_change.corr()

# Mento Carlo simulation:  thousands of possible allocations
stock_normed=stocks/stocks.iloc[0]
stock_normed.plot()

# log return vs arithmetic returns
log_ret=np.log(stocks/stocks.shift(1))
log_ret.head()
log_ret.hist(bins=100,figsize=(12,6))
plt.tight_layout()
log_ret.describe().transpose()
log_ret.mean()*252
log_ret.cov()

# ******singel run from some random allocation
np.random.seed(101)
print('stocks')
print(stocks.columns)

# funcitons
def assignWeight(NumOfStocks):
    weights=np.array(np.random.random(NumOfStocks))
    weights=weights/np.sum(weights)
    return weights

def portMeanAndVar(stocks,weights):
    log_ret=np.log(stocks/stocks.shift(1))
    exp_ret=np.sum((log_ret.mean()*weights)*252)
    # how to caculate portfolio covariance
    #  σ2p=ω C ω⊺ ,C is the cov matrix
    exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    SR=exp_ret/exp_vol
    return exp_ret,exp_vol,SR

def simulation(times,stocks):    
    # initialize 
    NumOfStocks=len(stocks.columns)
    all_weights=np.zeros((times,NumOfStocks))
    ret_arr=np.zeros(times)
    vol_arr=np.zeros(times)
    sharpe_arr=np.zeros(times)
    for i in range(times):
        weights=assignWeight(NumOfStocks)
        all_weights[i,:]=weights
        ret_arr[i],vol_arr[i],sharpe_arr[i]=portMeanAndVar(stocks,weights)
    return ret_arr,vol_arr,sharpe_arr

# simulation main part     
weights=assignWeight(4)
result=portMeanAndVar(stocks,weights)
ret_arr,vol_arr,sharpe_arr=simulation(5000,stocks)  
sharpe_arr.max()
maxLocation=sharpe_arr.argmax()
max_sr_ret=ret_arr[maxLocation]
max_sr_vol=vol_arr[maxLocation]
     
plt.figure(figsize=(12,8))
plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.scatter(max_sr_vol,max_sr_ret,c='red',s=50,edgecolors='black')        
    
    










