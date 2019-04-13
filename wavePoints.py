# -*- coding: utf-8 -*-
"""
@author: hejia
"""
import mysql_object
import functions
import waveOperation
import numpy as np

# default setting, like the interface
functions.default_setting()
mysql=mysql_object.mysqlOperation()

def generateBuyAndSellList(stock,capital,factors):    
    # get data from database
    lowBoundary=factors[0]
    highBoundary=factors[1]
    sellBuyRatio=factors[2]
    gap=factors[3]
    
    stockDelta=mysql.readDelta(stock)
    lowest=(stockDelta.iloc[0]['minimum'])*lowBoundary
    highest=(stockDelta.iloc[0]['maximum'])*highBoundary
    averagePrice=(lowest+highest)/2
    gap=stockDelta.iloc[0]['vol_value_median']*gap
    
    maxShare=int(capital/averagePrice)
    minShare=10
    pl=np.polyfit([lowest,highest],[maxShare,minShare],1)
    
    buyPoints=max(int((highest-lowest)/gap/sellBuyRatio)+1,2)
    sellPoints=(buyPoints-1)*sellBuyRatio+1
    sellPriceRange=np.array([round(i,2) for i in np.linspace(lowest,highest,sellPoints)])
    buyPriceRange=np.array([round(i,2) for i in np.linspace(lowest,highest,buyPoints)])
    buyShareRange=np.array([int(round(i)) for i in np.polyval(pl,buyPriceRange)])
    sellShareRange=np.array([int(round(i)) for i in np.polyval(pl,sellPriceRange)])
    
    buyList=[buyPriceRange,buyShareRange]
    sellList=[sellPriceRange,sellShareRange]
    return buyList,sellList

def generateFactorArray(lowBoundary,highBoundary,sellBuyRatio,gap):
    combinations=[]
    for i1 in lowBoundary:
        for i2 in highBoundary:
            for i3 in sellBuyRatio:
                for i4 in gap:
                    combinations.append([i1,i2,i3,i4])
    return combinations

stock='PDD'
stockInfo=mysql.readStcokInfo(stock)
initialPrice=stockInfo.iloc[0]['Open']
capital=3000
price_record1=[x for z in zip(stockInfo['High'],stockInfo['Low']) for x in z]

lowBoundary=np.arange(0.8,1.2,0.1)
highBoundary=np.arange(0.8,1.2,0.1)
sellBuyRatio=[1,2]
gap=np.arange(0.5,1.5,0.2)
combinations=generateFactorArray(lowBoundary,highBoundary,sellBuyRatio,gap) 
profit=[]
record=[]
ex=[]
for factor_i in range(len(combinations)):
    try:
    
        buyList,sellList=generateBuyAndSellList(stock,capital,combinations[factor_i])
        stockWave=waveOperation.Stock(buyList,sellList,initialPrice)
        for price in price_record1:
            stockWave.tradeStock(round(price,2))
        profit.append(stockWave.getProfit(20.96))
        record.append(stockWave.tradingRecord)
        combinations[factor_i].append(stockWave.getProfit(20.96))
            #stockWave.tradingRecord
    except Exception as e:
        print(e)
        ex.append(factor_i)
        combinations[factor_i].append(0)

        
#x=sorted(combinations,key=lambda factor: factor[4],reverse=True)
#records=[]
#test_factor=[1.1, 0.8, 2, 1]
#buyList,sellList=generateBuyAndSellList(stock,capital,test_factor)
#stockWave=waveOperation.Stock(buyList,sellList,initialPrice)
#for price in price_record1:
#    stockWave.tradeStock(round(price,2))
#profit.append(stockWave.getProfit(20.96))
#combinations[factor_i].append(stockWave.getProfit(20.96))



         


















