# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:55:49 2018

@author: kevin he
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:44:45 2018

@author: kevin he
"""
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
from collections import OrderedDict,defaultdict
import sys
sys.path.append('E:/python/StocksAnalysis/functions')
from functions import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# set how to present data 
default_setting() # from module funcitons

# step1, get the data
CODE='TSLA'
start_date=datetime.datetime(2017,6,1)
STOCK=yf.download(CODE,start_date)
#date_range=400
#start_date=datetime.datetime.today()-datetime.timedelta(date_range)

# step 2, std and mean
STOCK['MA10']=STOCK['Close'].rolling(10).mean()
STOCK['MA50']=STOCK['Close'].rolling(50).mean()
STOCK['MA200']=STOCK['Close'].rolling(200).mean()
STOCK_data=STOCK['Close']
STOCK_std=np.std(STOCK_data.dropna())
STOCK_mean=np.mean(STOCK_data)
N=2 
plotStds(STOCK_data,STOCK_mean,STOCK_std,N)

# step 3: based on std and mean, set trading range
# set a conservative aggressive factor 0-1,the smaller the less
lowest,highest=np.min(STOCK['Close']),np.max(STOCK['Close'])


low_price,high_price=250,320
most_shares,least_shares=12,2
pl=np.polyfit([low_price,high_price],[most_shares,least_shares],1)

price_range=np.array([round(i,2) for i in np.linspace(low_price,high_price,3)])
shares_range=np.array([int(round(i)) for i in np.polyval(pl,price_range)])
price_shares=list(zip(price_range,shares_range))

# find the current stock price's location in the price_range list

# show an example [10,20,30,40,50]
def currentPriceInList(currentPrice,price_range): # lst is sorted increasing
    if currentPrice<price_range[0]:
        return 0
    elif currentPrice>price_range[-1]:
        return len(price_range)-1
    else:
        for i in range(len(price_range)-1):
            
            if currentPrice >=price_range[i] and currentPrice<price_range[i+1]:
                return i
def currentSharesInList(currentShares,shares_range):
    for i in range(len(shares_range)):
        if currentShares==shares_range[i]:
            return i 


current_shares=1
location=1
cash_account=100
trading_record=defaultdict(list)
# judge , operate 
def evenTrading(current_price):
    global location,current_shares,cash_account
    buy_allowance,sell_allowance=True,True
    if current_shares==most_shares: # cannot buy any more
        buy_allowance=False
    if current_shares==least_shares:# cannot sell any more
        sell_allowance=False
    # 1. can do both buy and sell    
    if sell_allowance==True and buy_allowance==True: 
        upper_price,upper_shares=price_range[location+1],shares_range[location+1]
        lower_price,lower_shares=price_range[location-1],shares_range[location-1]
        print('------------------------------------------------')
        print('you should do the following setting:')
        print('buy {1} shares at {0} '.format(lower_price,lower_shares-current_shares ))
        print('sell {1} shares at {0} \n'.format(upper_price,current_shares-upper_shares))   
        print('before trading: location is {0}, whole shares is {1}'.format(location,current_shares))
        print('current price is {}'.format(current_price))
        #  check the current stock price
        if current_price>=upper_price:
            action='Sell'
            print('current price {0},sold {1} shares at {2}'.format(current_price,current_shares-upper_shares,upper_price)) 
            cash_account+=upper_price*(current_shares-upper_shares)
            location+=1
            trading_record[upper_price].append(action)
            print('after trade: current location is {0}, and current shares is {1}\n'.format(location,shares_range[location]))
        if current_price<=lower_price:
            action='BUY'
            print('current price {0},bought {1} shares {2}'.format(current_price,lower_shares-current_shares,lower_price))
            cash_account-=lower_price*(lower_shares-current_shares )
            location-=1
            trading_record[lower_price].append(action)
            print('after trade: current location is {0}, and current shares is {1}\n'.format(location,shares_range[location]))
         
    # 2. can sell but not buy because of most shares already
    if sell_allowance==True and buy_allowance==False:
        upper_price,upper_shares=price_range[location+1],shares_range[location+1]
        print('------------------------------------------------')
        print('you used all the money, and you should do the following setting:')
        print('sell {1} shares at {0} \n'.format(upper_price,current_shares-upper_shares))
        print('before trading: location is {0}, whole shares is {1}'.format(location,current_shares))
        print('current price is {}'.format(current_price))
        # check the current stock price
        if current_price>=upper_price:
            action='SELL'
            print('current price {0},sold {1} shares at {2}'.format(current_price,current_shares-upper_shares,upper_price)) 
            cash_account+=upper_price*(current_shares-upper_shares)
            location+=1 
            trading_record[upper_price].append(action)
            print('after trade: current location is {0}, and current shares is {1}\n'.format(location,shares_range[location]))
     # 3. can buy but not sell because of least shares already       
    elif sell_allowance==False and buy_allowance==True:
        lower_price,lower_shares=price_range[location-1],shares_range[location-1]
        print('------------------------------------------------')
        print('you almost sold all stocks, so you should do the following setting:')
        print('buy {1} shares at {0} '.format(lower_price,lower_shares-current_shares ))  
        print('before trading: location is {0}, whole shares is {1}'.format(location,current_shares))
        print('current price is {}'.format(current_price))
        if current_price<=lower_price:
            action='BUY'
            print('current price is {0},bought {1} shares at {2}'.format(current_price,lower_shares-current_shares,lower_price))
            cash_account-=lower_price*(lower_shares-current_shares )
            location-=1
            trading_record[lower_price].append(action)
            print('after trading: current location is {0}, and current shares is {1}\n'.format(location,shares_range[location]))
    current_shares=shares_range[location]


price_record_collection=[]
names=[]

# test 1, use prices list
price_record1=[10,50,100,200,250,300,350,300,200,150,100,50,10]
price_record_collection.append(price_record1)
# test 2, use STOCK['Close']

price_record2=STOCK['Close']
price_record_collection.append(price_record2)
#test 3, use random
priceChange=np.concatenate((np.random.normal(0.003,0.03,150),np.random.normal(-0.005,0.05,80)))
price_record3=[19]
for i in range(len(priceChange)):
    price_record3.append(round(price_record3[i]*(1+priceChange[i]),2))
price_record_collection.append(price_record3)
for price in price_record3:
    evenTrading(price)

# test four, use high and low
price_record4=[x for z in zip(STOCK['High'],STOCK['Low']) for x in z]
price_record_collection.append(price_record4)



account_record_collection=[]
trading_record_collection=[]
for i in range(len(price_record_collection)):
    # 1. initialize
    cash_account=5000
    current_price=price_record_collection[i][0]
    location=currentPriceInList(current_price,price_range)
    current_shares=shares_range[location]
    cash_account=cash_account-current_shares*current_price
    trading_record=defaultdict(list)
    # 2. trading
    for price in price_record_collection[i]:        
        evenTrading(price)
    # 3. record results
    stock_account=current_shares*current_price
    total_account=stock_account+cash_account
    cash_account,stock_account,total_account=map(lambda x:round(x,2),[cash_account,stock_account,total_account])
    account_record_collection.append([total_account,stock_account,cash_account])
    trading_record_collection.append(trading_record)
print('****************************************')
# compare finial result
for i in range(len(account_record_collection)):
    total_account,stock_account,cash_account=account_record_collection[i]
    print('total_acount:{0}, stock_account:{1}, cash_account:{2}'.format(total_account,stock_account,cash_account))
for i in    trading_record_collection:
    print(i)

    
    
    
