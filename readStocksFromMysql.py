# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 11:22:51 2018

@author: hejia
"""

import pandas as pd
import sqlalchemy
import fix_yahoo_finance as yf
import datetime
from myList import *

engine=sqlalchemy.create_engine('mysql+pymysql://root:hejia123@127.0.0.1:3306/stocks')
stock='TSLA'
sql='select * from '+ stock
TSLA=pd.read_sql(sql,engine,index_col='Date')
#.data=pd.read_sql_table(stock,engine,index_col='Date') 
