# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 23:19:07 2018

@author: kevin he
"""
code='^IXIC'

# import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import datetime

# read data
#
def default_setting():
    pd.set_option('display.max_rows',100)
    pd.set_option('display.max_columns',10)
    pd.set_option('display.max_colwidth',100)
    pd.set_option('display.width',None)
def get_std(data):
    return np.std(data)

def get_mean(data):
    return 

def plotStds(data,data_mean,data_std,N): #n mean how many std    
    data.plot(figsize=(12,8))           
    plt.axhline(data_mean,color='y',linestyle='-',label='mean '+str(round(data_mean,2)))
    plt.axhline(data_mean+N*data_std,color='r',linestyle='-',label=str(N)+'+std '+str(round(data_mean+N*data_std,2)))
    plt.axhline(data_mean-N*data_std,color='g',linestyle='-',label=str(N)+'-std '+str(round(data_mean-N*data_std,2)))
    plt.legend(bbox_to_anchor=(1,1))
    print('buy the stock at {:.2f}'.format(data_mean-N*data_std))
    print('sell the stock at {:.2f}'.format(data_mean+N*data_std))
    
stock_list=['TSLA','PDD']
start_date=datetime.datetime(2017,6,1)
    
def stocksCurrent(stock_list,start_date):
    l=[]
    for CODE in stock_list:
        STOCK=yf.download(CODE,start_date)
        lowest,highest=round(np.min(STOCK['Close']),2),round(np.max(STOCK['Close']),2)
        current=STOCK['Close'][-1]
        crt_lowest_growth=round(current/lowest-1,4)
        crt_highest_drop=round(current/highest-1,4)
        volatility=((STOCK['High']-STOCK['Low'])/STOCK['Close']).mean()
        l.append([lowest,highest,current,crt_lowest_growth,crt_highest_drop,volatility])
    names='lowest highest current crt_lowest_growth crt_highest_drop volatility'.split()
    df=pd.DataFrame(l,index=stock_list,columns=names)
    return df
    
        


