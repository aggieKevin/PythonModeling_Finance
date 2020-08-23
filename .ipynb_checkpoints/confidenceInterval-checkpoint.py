# -*- coding: utf-8 -*-
"""
@author: kevin he
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
background: we are use the sample to estimate the stock price. Assume that
based on the data from all population, the average stock price is 50, the standard
error is 5

'''
#
# step 1. create a sample based on the population. sample size is 100
#
np.random.seed(100)
population_mean=50
population_std=5
sample_size=100
sample=np.random.normal(population_mean,population_std,sample_size)
sample_mean=sample.mean()
sample_mean_std=sample.std()/np.sqrt(sample_size)

z_val=1.96 # 95% confidence level
lower95,upper95=sample_mean-z_val*sample_mean_std,sample_mean+z_val*sample_mean_std
confidenceIntervel95=(lower95,upper95)
print('95% confidence intervel is: ',confidenceIntervel95)
plt.figure(figsize=(12,6))
x=np.linspace(sample_mean-5,sample_mean+5,200)
y=stats.norm.pdf(x,sample_mean,sample_mean_std)
plt.plot(x,y,label='sample mean distribution with 0.95 confidence interval')
plt.xlabel('sample_mean')
plt.ylabel('sample_mean  pdf')
plt.fill_between(x,0,y,where=x>upper95,color='blue' )
plt.fill_between(x,0,y,where=x<lower95,color='blue')
plt.legend()


# step 2: use resampling to approach the analysis of confidence interval 
#  select one hundred data from the sample with repetition, doing it for n times
plt.figure(figsize=(12,6))
plt.xlabel('resample means distribution')
plt.axvline(x=lower95,color='orange')
plt.axvline(x=upper95,color='orange')
times=100
resample_size=100
means=[]
for i in range(times): 
    pick=np.random.randint(0,100,resample_size) # select 100 data from sample
    resample=[sample[i] for i in pick ]
    mean_i=np.mean(resample)
    means.append(mean_i)
    plt.plot(mean_i,i,'ro') # 95% confidence 
  
# the histgram distribution of means from 100 times of resample
plt.figure(figsize=(12,6))
plt.hist(means,label='resample means')
resample_mean=np.mean(means)
resample_mean_std=np.std(means)
plt.legend()

plt.figure(figsize=(12,6))
y1=stats.norm.pdf(x,sample_mean,sample_mean_std)
y2=stats.norm.pdf(x,resample_mean,resample_mean_std)
plt.plot(x,y1,label='sample',color='blue')
plt.plot(x,y2,label='resample with replacement',color='orange')
plt.legend()
# compare the distrution from     

# step 3: use different sizes to see the how distribution changes
sizes=[10,50,100,1000]
colors=['orange','red','blue','green']
plt.figure(figsize=(10,7))
plt.xlabel('sample_mean')
plt.ylabel('sample_mean  pdf')
for i in range(len(sizes)):
    sample_size=sizes[i]
    np.random.seed(100)
    sample_mean=sample.mean()
    sample_mean_std=sample.std()/np.sqrt(sample_size)
    print('sample size {0} has a sample_mean std at {1:.3f}'.format(sample_size,sample_mean_std))
    lower95,upper95=sample_mean-1.96*sample_mean_std,sample_mean+1.96*sample_mean_std
    x=np.linspace(sample_mean-5,sample_mean+5,200)
    y=stats.norm.pdf(x,sample_mean,sample_mean_std)
    plt.plot(x,y,label='sample size {}'.format(sample_size),color=colors[i])
    
    plt.fill_between(x,0,y,where=x>upper95,color=colors[i] )
    plt.fill_between(x,0,y,where=x<lower95,color=colors[i] )
    plt.legend()
# it's clear to see that when sample size increase, the confidence interval narrows down
 



