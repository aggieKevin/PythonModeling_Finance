# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 12:32:53 2018

@author: kevin he
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
df = sm.datasets.macrodata.load_pandas().data
df.head()
index = pd.Index(sm.tsa.datetools.dates_from_range('1959Q1', '2009Q3'))
df.index = index
df['realgdp'].plot()
plt.ylabel("REAL GDP")

# get he cycle and trend of a cycle
gdp_cycle, gdp_trend = sm.tsa.filters.hpfilter(df.realgdp)
df["trend"] = gdp_trend
gdp_cycle.plot()
gdp_trend.plot()
