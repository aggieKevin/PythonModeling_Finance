# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 18:56:36 2018

@author: hejia
"""

import fix_yahoo_finance as yf
import numpy as np
import datetime 

def caculateBelta(index,stock,start_date):
    indexRecord=(yf.download(index,start_date))['Close'].pct_change(1)[1:]
    stockRecord=yf.download(stock,start_date)['Close'].pct_change(1)[1:]
    belta=np.cov([indexRecord,stockRecord])[0,1]/np.var(indexRecord)
    return round(belta,2)

nasdaq='^IXIC'
sp500='SPX'
marriott='MAR'
years=[2010,2011,2012,2013,2014,2015,2016,2017]
belta_against_nasdaq={}
for year in years:
    start_date=datetime.date(year,1,1)
    belta_against_nasdaq['since '+str(year)]=caculateBelta(nasdaq,marriott,start_date)
    


    
    
