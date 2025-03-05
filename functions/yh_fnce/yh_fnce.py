import pandas as pd
from datetime import date
import workdays

# Yahoo Finance
import yfinance as yf

class yh_fnce:

    #Steven's codes
    def lastclose(ticker):
        today = date.today()
        #1. determine the last business day.
        '''
        if float(date.weekday(today)) > 4:
            lastBD = workdays.workday(today, -1)
        else:
            lastBD = today
        return yf.download(ticker,
                      start=lastBD,
                      end=lastBD,
                      progress=False)["Close"][0]
        '''
        return yf.download(ticker,
                      start=workdays.workday(today,-1),
                      end=today,
                      progress=False)["Close"].iloc[-1].iloc[-1]
    #get data on this ticker
    def tickerData(ticker):
        return yf.Ticker(ticker)

    #get the historical prices for this ticker
    def tickerHP(self):
        return self.tickerData().history(period='1d', start= self.startdate, end= self.enddate)

'''
    #info on the company
    tickerData.info

    #see your data
    tickerDf

    #upcoming earning event
    tickerData.calendar

    #get recommendation data for ticker
    tickerData.recommendations

    ticker = yf.Ticker('TSLA')
    
    tsla_df = ticker.history(period="max")
    
    tsla_df['Close'].plot(title="TSLA's stock price")


    # from yahoofinancials
    from yahoofinancials import YahooFinancials
    yahoo_financials = YahooFinancials('HKD=X')

    data = yahoo_financials.get_historical_price_data(start_date='2000-01-01',
                                                      end_date='2019-12-31',
                                                      time_interval='weekly')

    tsla_df = pd.DataFrame(data['HKD=X']['prices'])
    tsla_df = tsla_df.drop('date', axis=1).set_index('formatted_date')
    print(tsla_df.head())
'''





