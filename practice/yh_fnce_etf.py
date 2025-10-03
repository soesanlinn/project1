import yfinance as yf
from datetime import date
import workdays
today = date.today()
ticker = "GLE.PA"
df = yf.Ticker(ticker).history(period="max").tail(1)['Close']
#df = df[df['Date']=='2025-10-02 00:00:00+01:00']

#df.columns = df.columns.droplevel(1) # Drop the multi-index
test = yf.download(ticker,
                   start=workdays.workday(today,0 ),
                   end=today,
                   progress=False)["Close"]#.iloc[-1].iloc[-1]
#print(df)
print(yf.Ticker('TSLA').history(period="max").tail(1)['Close'])