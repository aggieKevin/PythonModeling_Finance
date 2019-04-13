# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 15:27:13 2019

@author: hejia
"""
# stationary: mean, variance, autocorrelation are all constant
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.tsa as tsa
import matplotlib.pyplot as plt

#X_t=b_0 + b_1 * x_t-1 + b_2 * x_t-2 + b_p * x_t-p + error
np.random.seed(100)
def AR(b,X,mu,sigma):
    length=min(len(b)-1,len(X))
    return b[0]+np.dot(b[1:length+1],X[-length:])+ np.random.normal(mu,sigma)

b=np.array([0,0.8,0.1,0.05])
X=np.array([1])

mu=0
sigma=1

for i in range(10000):
    X=np.append(X,AR(b,X,mu,sigma))
    
plt.figure(figsize=(8,4))
plt.plot(X)
plt.xlabel('Time')
plt.ylabel('AR')

# tail risk, AR tends to have more extreme values than data from a normal distribution.
#becasue the value will stay up and affect more values.
def compare_AR_normal(X):
    A=np.zeros((2,4))
    for k in range(4):
        A[0,k]=len(X[X>k+1])/float(len(X)) # estimate tails of X
        A[1,k]=1-stats.norm.cdf(k+1)
    print('extreme value in AR 1:{:.3f} ,2:{:.3f}, 3:{:.3f}, 4:{:.3f}'.format(*A[0]))
    print('extreme value in normal 1:{:.3f} ,2:{:.3f}, 3:{:.3f}, 4:{:.3f}'.format(*A[1]))
    return A

compare_AR_normal(X)



# check whether the mean of X is stationary
def compute_unajusted_interval(X): # 95% boundaries 
    mu=np.mean(X)
    sigma=np.std(X)
    lower=mu-1.96* sigma/np.sqrt(len(X))
    upper=mu+1.96* sigma/np.sqrt(len(X))
    return lower,upper

def check_coverage(X):
    lower,upper=compute_unajusted_interval(X)
    return True if 0<=upper and 0>=lower else False

def simulate_AR_process(b,T):
    X=np.array([1])
    mu=0
    sigma=1
    for i in range(T):
        X=np.append(X,AR(b,X,mu,sigma))
    return X

trials=1000
outcomes=np.zeros((trials,1))

for i in range(trials):
    Z=simulate_AR_process(np.array([0,0.8,0.1,0.05]),100)
    if check_coverage(Z):
        outcomes[i]=1
    else:
        outcomes[i]=0
np.sum(outcomes)/trials

# autocorrelation function and partial autocorrelation function
from statsmodels.tsa.stattools import acf,pacf
X=simulate_AR_process(np.array([0,0.8,0.1,0.05]),1000)
# choose 40 lags
nlags=40
X_acf=acf(X,nlags=nlags)
print('Autocorrelations: \n {}'.format(X_acf))

X_pacf=pacf(X,nlags=nlags)
print('Partial Autocorelations :\n {}'.format(X_pacf))

plt.figure()
plt.plot(X_acf,'ro')
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('ACF')   

plt.figure()
plt.plot(X_pacf,'ro')
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.title('PACF')   

# check confidence level for acf and pacf
X_acf, X_acf_confs=acf(X,nlags=nlags,alpha=0.05)
X_pacf,X_pacf_confs=pacf(X,nlags=nlags,alpha=0.05)

def plot_acf(X_acf, X_acf_confs, title='ACF'):
    # The confidence intervals are returned by the functions as (lower, upper)
    # The plotting function needs them in the form (x-lower, upper-x)
    errorbars = np.ndarray((2, len(X_acf)))
    errorbars[0, :] = X_acf - X_acf_confs[:,0]
    errorbars[1, :] = X_acf_confs[:,1] - X_acf

    plt.plot(X_acf, 'ro')
    plt.errorbar(range(len(X_acf)), X_acf, yerr=errorbars, fmt='none', ecolor='gray', capthick=2)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title(title);
plot_acf(X_acf, X_acf_confs)





