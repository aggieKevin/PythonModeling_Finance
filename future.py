# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 21:46:19 2019

@author: hejia
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl
import datetime

# K is the delivery price agreed upon in the contract
K=50
S_T=np.linspace(0,100,200)
long_payoff=S_T-K
short_payoff=K-S_T

plt.plot(S_T, long_payoff)
plt.axhline(0, color='black', alpha=0.3)
plt.axvline(0, color='black', alpha=0.3)
plt.xlim(0, 100)
plt.ylim(-100, 100)
plt.axvline(K, linestyle='dashed', color='r', label='K')
plt.ylabel('Payoff')
plt.xlabel('$S_T$')
plt.title('Payoff of a Long Forward Contract')
plt.legend();

plt.plot(S_T, short_payoff);
plt.axhline(0, color='black', alpha=0.3)
plt.axvline(0, color='black', alpha=0.3)
plt.xlim(0, 100)
plt.ylim(-100, 100)
plt.axvline(K, linestyle='dashed', color='r', label='K')
plt.ylabel('Payoff')
plt.xlabel('$S_T$')
plt.title('Payoff of a Short Forward Contract')
plt.legend()

start_date=datetime.datetime(2017,1,19)
end_date=datetime.datetime(2017,2,15)
futures_position_value=quandl.get('CHRIS/CME_CNH1',start_date=start_date,end_date=end_date)['Settle']
