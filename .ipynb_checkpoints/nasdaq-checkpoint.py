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
import sys
from collections import OrderedDict,defaultdict
sys.path.append('E:/python/StocksAnalysis/function_packages')
from function_packages import *
# set options
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# step1, get the data
start_date=datetime.datetime(2017,6,1)
try:
    TQQQ=yf.download('TQQQ',start_date)
except ValueError:
    pass

# step 2, std and mean
TQQQ['MA10']=TQQQ['Close'].rolling(10).mean()
TQQQ['MA50']=TQQQ['Close'].rolling(50).mean()
TQQQ['MA200']=TQQQ['Close'].rolling(200).mean()
# choose one column as the source to caculate the std and mean
N=2
TQQQ_data=TQQQ['MA50']
TQQQ_std=np.std(TQQQ_data.dropna())
TQQQ_mean=np.mean(TQQQ_data)
#plotStds(TQQQ_data,TQQQ_mean,TQQQ_std,N)

# based on std and mean, set trading range

low_price,high_price=30,70
most_shares,least_shares=100,10
pl=np.polyfit([low_price,high_price],[most_shares,least_shares],1)

price_range=np.array([round(i,2) for i in np.linspace(low_price,high_price,5)])
shares_range=np.array([int(round(i)) for i in np.polyval(pl,price_range)])
price_shares=list(zip(price_range,shares_range))

# find the current stock price's location in the price_range list
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

'''
1. initial investment
2. stock account, cash account
   (1) stock account=current_shares*current_price
   (2) cash account=initial account-cashout on buying+ cashin from selling
'''



price_record_collection=[]
names=[]
# test 1, use prices list
price_record1=[36,40,45,50,55,58,55,51,57,60,67,66,59,65,68,69,70]
price_record_collection.append(price_record1)
# test 2, use TQQQ['Close']

price_record2=TQQQ['Close']
price_record_collection.append(price_record2)
#test 3, use random
priceChange=np.concatenate((np.random.normal(0.003,0.03,150),np.random.normal(-0.005,0.05,80)))
price_record3=[40]
for i in range(len(priceChange)):
    price_record3.append(round(price_record3[i]*(1+priceChange[i]),2))
price_record_collection.append(price_record3)
for price in price_record3:
    evenTrading(price)

# test four, use high and low
price_record4=[x for z in zip(TQQQ['High'],TQQQ['Low']) for x in z]
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
    

    
    
    
