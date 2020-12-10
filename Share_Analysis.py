
"""
Created on Wed Dec  9 13:57:59 2020

STOCK_MARKET_ANALYSIS

@author: Kartikeya.Tiwari...

"""

import yfinance as yf                  
import pandas as pd                    
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

file = open("C:/Users/Dell/Downloads/Place_This_File_in_Download_Folder.txt","r")
print(file.read())
file.close()

def average_volume(data_frame):
    temp = data_frame
    temp = list(temp)
    temp = temp[-50:]
    average_vol = st.mean(temp)
    return average_vol

def moving_mean(data_frame,n):
    data_frame = list(data_frame)
    i = 0
    moving_average = []
    while i < (len(data_frame) - n + 1):
        temp = data_frame[i:i+n]
        temp_average = sum(temp)/n
        moving_average.append(temp_average)
        i = i + 1
    return moving_average

n = int(input("How many companies to compare?"))
for i in range(n):
        print("Enter ticker symbol of respective",i+1," company")
        ticker_symbol = input()                                         
        ticker_company = yf.Ticker(ticker_symbol) 
        company = ticker_company.history(period='2y', start= '2018-12-5' ,end = None)
        current_price = company['Close']
        current_price = current_price[-1]
        avg_volume = average_volume(company['Volume'])
        stats = ticker_company.info 
        info = {ticker_symbol:
                {'Currency:':stats['currency'],
                 'Current Price of stock:':current_price,
                 'Market cap:':stats['marketCap'],
                 'Dividend Rate:':stats['dividendRate'],
                 'Dividend Yield:':stats['dividendYield'],
                 'Beta:':stats['beta'],
                 'Earnings Quarterly Growth:':stats['earningsQuarterlyGrowth'],
                 'Fifty Day Average:':stats['fiftyDayAverage'],
                 'Standard_deviation:':np.std(company['Close']),
                 'Variance:':np.var(company['Close']),
                 'Volume of share traded(50 days average)':avg_volume,
                 'Price to book ratio:':stats['priceToBook']
                 }
                }
        print(pd.DataFrame(info))
        if stats['priceToBook'] is None:
            print("No data")
        else:    
            if stats['priceToBook'] < 1:
               print('Price to Book ratio : Undervalued')
            elif stats['priceToBook'] > 1 and stats['priceToBook'] < 5:
               print('Price to Book ratio : Fairvalued')
            else:
               print('Price to book ratio : Overvalued')
        rec = ticker_company.recommendations
        if rec is None:
            print('No recommendations!')
        else:
            df = pd.DataFrame(rec)
            last_element = df.iloc[-1]
            last_element = dict(last_element)
            print("Latest Recommendation:")
            for each in last_element:
              print(each,":->",last_element[each])
        company_legend = stats['longName'] 
        stock_market = yf.Ticker('^BSESN')         #enter respective stock market exchange, for ex.-> for AAPL , you have to enter(^IXIC) as it belong to NASDAQ stock market exchange
        data = stock_market.history(period='2y', start= '2018-12-5' ,end = None)
        plt.figure(0)
        plt.title(
                  label ="Co-relation graph w.r.t ^BSESN(cyan color)",
                  fontsize=15, 
                  color="orange"
                  )
        plt.plot(data['Close']/max(data['Close']),'cyan')
        plt.plot(company['Close']/max(company['Close']),label =  company_legend )
        plt.legend()
        plt.figure(1)
        plt.title(
                  label ="Last 2 years share graph",
                  fontsize=15, 
                  color="orange"  
                  )
        plt.plot(company['Close'],label =  company_legend)
        plt.xlabel('years')
        plt.ylabel('Cost of 1 share')
        plt.legend()
        
        lst = list(company['Close'])
        last = lst[-32:]
        predict = moving_mean(last,3)
        predict1 = predict
        std_dev = np.std(company['Close'])
        for i in range (30):
            predict1[i]=predict1[i]+std_dev         
        plt.figure(2)
        plt.title(
                  label ="Prediction of next 30 days",
                  fontsize=12, 
                  color="orange"
                 )
        plt.plot(predict1,label =  company_legend)
        plt.legend()
    