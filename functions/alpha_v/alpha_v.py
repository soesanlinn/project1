import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

api_key = '2ZCROLNJAADOE1V7'
class UT_03_av:
    def lastclose(ticker):
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_daily(symbol=ticker, outputsize= 'full')
        return data['4. close'][0]