# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:57:22 2018

@author: kevin he
"""
from collections import defaultdict
class Stock(object):
    def __init__(self,buyList,sellList,initialPrice):
        self.buyList=buyList# [[pricelist],[shareList]]
        self.sellList=sellList# [[pricelist],[shareList]]
        self.positionBuy=0
        self.positionSell=0
        self.currentShares=0
        self.buyAllow=True
        self.sellAllow=True
        self.totalMoneyBuy=0
        self.totalMoneySell=0
        self.tradingRecord=defaultdict(list)
        self.initialize(initialPrice)
#        self.currentStatus={}
#        self.currentStatus['buyAllow']=True
#        self.currentStatus['sellAllow']=True
#        self.currentStatus['currentShares']=0
#        self.currentStatus['positionBuy']=0
#        self.currentStatus['positionSell']=0
        

    def initialize(self,currentPrice): #set positionBuy, positionSell, currentShare
        print('beginning of initialization')
        if currentPrice<self.buyList[0][0]:
            self.positionBuy=0
            self.positionSell=0
        elif currentPrice>self.buyList[0][-1]:
            self.positionBuy= len(self.buyList[0])-1
            self.positionSell=len(self.sellList[0])-1
        else:
            for i in range(len(self.buyList[0])-1):
                if self.buyList[0][i]<= currentPrice<self.buyList[0][i+1]:
                    self.positionBuy=i+1
                    break
        self.currentShares=self.buyList[1][self.positionBuy]
        self.totalMoneyBuy=self.currentShares*currentPrice
        self.tradingRecord[currentPrice].append(('Buy',self.currentShares))
        for i in range(len(self.sellList[1])-1):
            if self.currentShares==self.sellList[1][i]:
                self.positionSell=i
                break
        self.checkAllow()
        print('current shares: ', self.currentShares)
        print('initial price: ',currentPrice)
        print('buy list: ',self.buyList)
        print('sell list: ',self.sellList)
        print('end of enitialization')
        self.setOrder()
        
        

    def updatePositionBuy(self):
        for i in range(len(self.buyList[1])-1):
            if self.buyList[1][i+1]<=self.currentShares<self.buyList[1][i]:
                self.positionBuy=i+1
                break
                
    def updatePositionSell(self):
        for i in range(len(self.sellList[1])-1):
            if self.sellList[1][i+1]<self.currentShares<=self.sellList[1][i]:
                self.positionSell=i
                break
    def getProfit(self,currentPrice):
        return round(self.currentShares*currentPrice+self.totalMoneySell-self.totalMoneyBuy,2)
    def setBuyList(self,newBuyList):
        self.buyList=newBuyList
    def setSellList(self,newSellList):
        self.sellList=newSellList
    def getBuyList(self):
        return self.buyList
    def getSellList(self):
        return self.sellList
    def checkAllow(self):
        most_shares=self.sellList[1][0]
        least_shares=self.sellList[1][-1]
        self.buyAllow=False if self.currentShares>=most_shares else True    
        self.sellAllow=False if self.currentShares<=least_shares else True

    def setOrder(self):
        if self.sellAllow==True: # set how to sell
            upperPrice,upperShares=self.sellList[0][self.positionSell+1],self.sellList[1][self.positionSell+1]
            print('sell setting:')
            print('sell {1} shares at {0}'.format(upperPrice,self.currentShares-upperShares))
        if self.buyAllow==True:
            lowerPrice,lowerShares=self.buyList[0][self.positionBuy-1],self.buyList[1][self.positionBuy-1]
            print('buy setting:')
            print('buy {1} shares at {0} '.format(lowerPrice,lowerShares-self.currentShares ))
        print('\n')
            
    def tradeStock(self,currentPrice):        
        # buy
        # update locationInBuyList and sell list
        if self.buyAllow==True:
            lowerPrice,lowerShares=self.buyList[0][self.positionBuy-1],self.buyList[1][self.positionBuy-1]
            if currentPrice<=lowerPrice:
                action='Buy'
                print('current price is ',currentPrice)
                print('before trade, current shares: {}'.format(self.currentShares))
                print('now price {0},bought {1} shares at {2}'.format(currentPrice,lowerShares-self.currentShares,lowerPrice))
                # update 
                self.tradingRecord[lowerPrice].append((action,lowerShares-self.currentShares))
                self.totalMoneyBuy+=lowerPrice*(lowerShares-self.currentShares)
                self.currentShares=lowerShares
                self.positionBuy-=1              
                self.updatePositionSell()
                self.checkAllow()
                print('after trade, current shares: {}'.format(self.currentShares))
                print('profit: ',self.getProfit(currentPrice))
                print('****************************************************')               
                self.setOrder()
        if self.sellAllow==True:
            upperPrice,upperShares=self.sellList[0][self.positionSell+1],self.sellList[1][self.positionSell+1]
            if currentPrice>=upperPrice:
                action='Sell'
                print('current price is ',currentPrice)
                print('before trade, current shares: {}'.format(self.currentShares))
                print('now price {0},sold {1} shares at {2}'.format(currentPrice,self.currentShares-upperShares,upperPrice))
                #update
                self.tradingRecord[upperPrice].append((action,self.currentShares-upperShares))
                self.totalMoneySell+=upperPrice*(self.currentShares-upperShares)
                self.currentShares=upperShares
                self.positionSell+=1
                self.updatePositionBuy()
                self.checkAllow()
                print('after trade, current shares: {}'.format(self.currentShares))
                print('profit: ',self.getProfit(currentPrice))
                print('****************************************************')
                self.setOrder()

if __name__=="__main__":                
    buyList= [[10, 30, 50, 70], [80, 60, 40, 20]]
    sellList=[ [10., 20., 30., 40., 50., 60., 70.],[80., 70., 60., 50., 40., 30., 20.]]
    price=[20.0, 5,10,12,18,20,25.56, 31.11, 36.67, 42.22, 47.78, 53.33, 58.89, 64.44, 70.0,80,70,60,66,55,45,38,22,22,13]
    currentPrice=price[0]
    m=Stock(buyList,sellList,currentPrice)
    for i in price:
        m.tradeStock(i)
    
    



