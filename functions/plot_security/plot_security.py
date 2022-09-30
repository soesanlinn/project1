import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.techindicators import TechIndicators
import matplotlib.dates as mdates
from datetime import datetime
import pytz


def getdata(input_sec_code, input_day_range, ti_param={}):
    # INITIAL SET UP________________________________________________________________________________________________
    tz_HK = pytz.timezone('Asia/Hong_Kong')
    rng_to_numdays = {
        '1D': 1,
        '5D': 5,
        '1M': 30,
        '3M': 90,
        '6M': 180,
        '1Y': 365,
        '5Y': 1825,
        '10Y': 3650, }
    if input_sec_code[:3] == "FX:":
        sec_type = "FX"
        sec_code = input_sec_code[3:]
    else:
        sec_type = "Stock"
        sec_code = input_sec_code
    # Alpha-vantage API key
    api_key = '2ZCROLNJAADOE1V7'
    api_key2 = '2ZV21LNT5TK8AWBS'
    # MACD info
    if ti_param == {}:
        ti_param = {
            'shortema_days': 12,
            'longema_days': 26,
            'signal_days': 9,
            'bb_proxrng': 10,
            'weight_macd': 33,
            'weight_rsi': 33,
            'weight_bb': 33,
            'buysell_threshold': 50,
        }
    num_days = int(rng_to_numdays[input_day_range])
    shortema_days = ti_param['shortema_days']
    longema_days = ti_param['longema_days']
    signal_days = ti_param['signal_days']
    bb_proxrng = 0.01 * ti_param['bb_proxrng']
    weight_macd = 0.01 * ti_param['weight_macd']
    weight_rsi = 0.01 * ti_param['weight_rsi']
    weight_bb = 0.01 * ti_param['weight_bb']
    buysell_threshold = 0.01 * ti_param['buysell_threshold']

    # API USAGE________________________________________________________________________________________________
    def reset_apiusage():  # Set API usage first time.
        now = datetime.now(tz_HK).strftime('%H:%M')
        apiusage = pd.DataFrame({'API Key': [api_key, api_key2],
                                'Time Period': [now, now],
                                'Number of Use': [0, 0]})
        apiusage = apiusage.set_index('API Key')
        return apiusage
    def update_apiusage(apikey, apiusage):  # Update the usage frequency of an API key.
        now = datetime.now(tz_HK).strftime('%H:%M')
        if now != apiusage['Time Period'][0]:  # If the minute changes, reset the apiusage table.
            apiusage = reset_apiusage()
            apiusage['Number of Use'][apikey] += 1
        return apiusage
    def less_used_api_key(apiusage):
        apikey = list(apiusage[apiusage['Number of Use'] == apiusage['Number of Use'].min()].index)[0]
        return apikey

    # SECURITY DATA________________________________________________________________________________________________
    apiusage = reset_apiusage()
    apikey = less_used_api_key(apiusage)
    if sec_type == 'FX':
        fx = ForeignExchange(key=apikey, output_format='pandas')
        data_ts, meta_data_ts = fx.get_currency_exchange_daily(from_symbol=sec_code[:3],
                                                               to_symbol=sec_code[3:],
                                                               outputsize='full')
    else:
        ts = TimeSeries(key=apikey, output_format='pandas')
        data_ts, meta_data_ts = ts.get_daily(symbol=sec_code, outputsize='full')
    apiusage = update_apiusage(apikey, apiusage)
    df = data_ts.sort_values(by=['date'], ascending=True)
    df = df[-num_days:]

    # TECH INDICATORS________________________________________________________________________________________________
    # MACD
    apikey = less_used_api_key(apiusage)
    ti = TechIndicators(key=apikey, output_format='pandas')
    apiusage = update_apiusage(apikey, apiusage)
    data_macd, meta_data_macd = ti.get_macd(symbol=sec_code, interval='daily', series_type='close',
                                            slowperiod=longema_days, fastperiod=shortema_days, signalperiod=signal_days)
    data_macd = data_macd.sort_values(by=['date'], ascending=True)
    data_macd = data_macd[-num_days:]
    df[['MACD','MACD_Signal','MACD_Hist']] = data_macd[['MACD','MACD_Signal','MACD_Hist']]
    def macd_buy_sell(df):  # MACD buy/ sell decision function
        move = []
        lastflag = ''
        for i in range(0, len(df)):
            # If the sign changes in histo data, there is a crossover of MACD and signal.
            if i > 0 and (df['MACD_Hist'][i] / abs(df['MACD_Hist'][i])) != (
                    df['MACD_Hist'][i - 1] / abs(df['MACD_Hist'][i - 1])):
                if df['MACD_Hist'][i] > 0 and lastflag != 'Buy':
                    move.append('Buy')
                    lastflag = 'Buy'
                elif df['MACD_Hist'][i] < 0 and lastflag != 'Sell':
                    move.append('Sell')
                    lastflag = 'Sell'
                else:
                    move.append(np.nan)
            else:
                move.append(np.nan)  # No crossover means no move but hold
        return move
    df['MACD_Buy_Sell'] = macd_buy_sell(df)
    # RSI
    apikey = less_used_api_key(apiusage)
    ti = TechIndicators(key=apikey, output_format='pandas')
    apiusage = update_apiusage(apikey, apiusage)
    data_rsi, metadata_rsi = ti.get_rsi(symbol=sec_code, interval='daily', series_type='close')
    data_rsi = data_rsi.sort_values(by=['date'], ascending=True)
    data_rsi = data_rsi[-num_days:]
    df['RSI'] = data_rsi['RSI']
    df['RSI_Buy_Sell'] = df['RSI'].apply(lambda x: 'Buy' if x < 30 else 'Sell' if x > 70 else np.nan)
    # Bollinger Band
    apikey = less_used_api_key(apiusage)
    ti = TechIndicators(key=apikey, output_format='pandas')
    apiusage = update_apiusage(apikey, apiusage)
    data_bb, metadata_bb = ti.get_bbands(symbol=sec_code, interval='daily', series_type='close')
    data_bb = data_bb.sort_values(by=['date'], ascending=True)
    data_bb = data_bb[-num_days:]
    df[['BB_Lower', 'BB_Middle', 'BB_Upper']] = data_bb[['Real Lower Band', 'Real Middle Band', 'Real Upper Band']]
    '''
    If closeprice within 10% of upper band-> overbought   -> sell when high.  -> decision value = 'Sell'
    If closeprice within 10% of lower band -> oversold     -> buy when low.    -> decision value = 'Buy'
    Otherwise   -> no recommendation                -> decision value = blank
    '''
    def bb_buy_sell(df):
        move = []
        for i in range(0, len(df)):
            bbwidth = df['BB_Upper'][i] - df['BB_Lower'][i]
            bbtriggerrng = bb_proxrng * bbwidth
            if df['4. close'][i] > df['BB_Upper'][i] - bbtriggerrng:
                move.append('Sell')
            elif df['4. close'][i] < df['BB_Lower'][i] + bbtriggerrng:
                move.append('Buy')
            else:
                move.append(np.nan)
        return move
    df['BB_Buy_Sell'] = bb_buy_sell(df)
    # FINAL DECISION________________________________________________________________________________________________
    # Convert decisions into numerals: Buy = 1, Sell = -1, Hold or np.nan = 0
    num_decision_dict = {'Buy': 1, 'Sell': -1, np.nan: 0}
    macd_decision_index = df['MACD_Buy_Sell'].apply(lambda x: num_decision_dict[x])
    rsi_decision_index = df['RSI_Buy_Sell'].apply(lambda x: num_decision_dict[x])
    bb_decision_index = df['BB_Buy_Sell'].apply(lambda x: num_decision_dict[x])
    # Average the decision numerals to draw an equally-weighted final decision on each entry.
    final_decision = (macd_decision_index * weight_macd) + (rsi_decision_index * weight_rsi) + (
                        bb_decision_index * weight_bb)
    noise_dayrng = int(round(num_days * 0.10, 0))  # Take percent of total number of days in scope as a day range to detect noise = x days.
    for i in range(len(final_decision) - noise_dayrng):  # The latest x number of days cannot be used due to a moving range nature
        if abs(final_decision[i]) > buysell_threshold:  # If the weight average value triggers buy/ sell decision
            noise_rng = final_decision[i + 1: i + noise_dayrng]  # Set a new moving noise range.
            if max(noise_rng.max(),
                   abs(noise_rng.min())) > buysell_threshold:  # If there is another buy/ sell decision in the next x days, the current datapoint at i is a noise and set the value to 0 to remove it.
                final_decision[i] = 0
    final_decision = final_decision.apply(lambda x: 'Buy' if x > buysell_threshold else 'Sell' if type(x) == float
                                                    and x < - buysell_threshold else np.nan)
    df['Final_Decision'] = final_decision
    return df


def mplplot(df, sec_code):
    # Format the plots.
    plt.style.use('fivethirtyeight')
    mpl.rcParams['text.color'] = 'lightgrey'
    mpl.rcParams['axes.labelcolor'] = 'grey'
    mpl.rcParams['axes.edgecolor'] = 'dimgrey'
    mpl.rcParams['xtick.color'] = 'grey'
    mpl.rcParams['ytick.color'] = 'grey'
    mpl.rcParams['grid.color'] = 'grey'
    mpl.rcParams['grid.linestyle'] = 'dashed'
    mpl.rcParams['grid.linewidth'] = 0.8
    mpl.rcParams['grid.alpha'] = 0.7
    mpl.rcParams['figure.facecolor'] = 'black'
    mpl.rcParams['axes.facecolor'] = 'black'
    mpl.rcParams['legend.frameon'] = False
    mpl.rcParams['legend.facecolor'] = 'grey'
    mpl.rcParams['lines.markersize'] = 12
    mpl.rcParams['axes.linewidth'] = 1.3
    datefmt = mdates.DateFormatter('%d-%b')
    # Assign histo data to buy/ sell decisions to later plot it on the MACD chart.
    buy_macd = df.apply(lambda x: x['MACD'] if x['MACD_Buy_Sell'] == 'Buy' else np.nan, axis=1)
    sell_macd = df.apply(lambda x: x['MACD'] if x['MACD_Buy_Sell'] == 'Sell' else np.nan, axis=1)
    # Assign buy/ sell decisions to RSI to later plot it on the RSI chart.
    buy_rsi = df.apply(lambda x: x['RSI'] if x['RSI_Buy_Sell'] == 'Buy' else np.nan, axis=1)
    sell_rsi = df.apply(lambda x: x['RSI'] if x['RSI_Buy_Sell'] == 'Sell' else np.nan, axis=1)
    buyprices = df.apply(lambda x: x['4. close'] if x['Final_Decision'] == 'Buy' else np.nan, axis=1)
    sellprices = df.apply(lambda x: x['4. close'] if x['Final_Decision'] == 'Sell' else np.nan, axis=1)
    # PLOT________________________________________________________________________________________________
    # Visually show the stock buy and sell signals.
    fig = plt.figure(figsize=(20, 15))
    # Create an X-axis visual with 10 equally spaced dates.
    xlabels = np.linspace(df.index[0].value, df.index[-1].value,
                          10)  # convert timestamps into values before equally spacing them into 10.
    xlabels = pd.to_datetime(xlabels)  # reconvert the 10 values into respective timestamps
    # 1. Main graph
    # Close price
    ax1 = plt.subplot2grid((13, 4), (1, 0), rowspan=7, colspan=4)
    if buyprices.count() > 0:
        ax1.scatter(df.index, buyprices, label='Buy', color='green', marker='^', alpha=1)
    if sellprices.count() > 0:
        ax1.scatter(df.index, sellprices, label='Sell', color='red', marker='v', alpha=1)
    ax1.plot(df.index, df['4. close'], label='Close Price', color='teal', alpha=0.8, linewidth=2)
    # Bollinger Bands
    ax1.plot(df.index, df['BB_Lower'], color='orange', alpha=0.3, linewidth=1.8)
    ax1.plot(df.index, df['BB_Middle'], color='orange', alpha=0.2, linewidth=1.5)
    ax1.plot(df.index, df['BB_Upper'], color='orange', alpha=0.3, linewidth=1.8)
    ax1.xaxis.set_ticklabels([])
    plt.xticks(xlabels)
    ax1.legend(loc='upper left', ncol=10)
    plt.title(sec_code + ' Close Price, Buy and Sell Signals')
    # Split the histogram into two for coloring: green and red
    histo_p = pd.DataFrame(df['MACD_Hist'])
    histo_n = pd.DataFrame(df['MACD_Hist'])
    histo_p[histo_p < 0] = 0
    histo_n[histo_n > 0] = 0
    # 2. MACD graph
    ax2 = plt.subplot2grid((13, 4), (8, 0), rowspan=2, colspan=4)
    if buy_macd.count() > 0:
        ax2.scatter(df.index, buy_macd, label='Buy', color='green', marker='^', alpha=1)
    if sell_macd.count() > 0:
        ax2.scatter(df.index, sell_macd, label='Sell', color='red', marker='v', alpha=1)
    ax2.plot(df.index, df['MACD_Signal'], label='Signal', color='cadetblue', alpha=0.7, linewidth=1.3)
    ax2.plot(df.index, df['MACD'], label='MACD', color='tomato', alpha=0.7, linewidth=1.3)
    ax2.bar(df.index, histo_p['MACD_Hist'], label='Histogram', color='green', alpha=0.5)
    ax2.bar(df.index, histo_n['MACD_Hist'], color='red', alpha=0.5)
    ax2.xaxis.set_ticklabels([])
    plt.xticks(xlabels)
    ax2.legend(loc='lower right', ncol=10)
    # 3. RSI graph
    ax3 = plt.subplot2grid((13, 4), (10, 0), rowspan=2, colspan=4)
    if buy_rsi.count() > 0:
        ax3.scatter(df.index, buy_rsi, label='Buy', color='green', marker='^', alpha=1)
    if sell_rsi.count() > 0:
        ax3.scatter(df.index, sell_rsi, label='Sell', color='red', marker='v', alpha=1)
    ax3.plot(df.index, df['RSI'], label='RSI', color='tomato', alpha=0.7, linewidth=1.3)
    ax3.fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70), color='red', alpha=0.3)
    ax3.fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30), color='green', alpha=0.6)
    ax3.xaxis.set_major_formatter(datefmt)
    ax3.legend(loc='lower right', ncol=10)
    plt.xticks(xlabels)
    plt.yticks((0, 30, 50, 70, 100))
    plt.ylim(0, 100)
    plt.show()


if __name__ == '__main__':
    sec_code = 'VOO'  # GLE.PA FX:SGDHKD MCHI SPY FAS
    time_rng = '6M'
    df_result = getdata(sec_code, time_rng)
    mplplot(df_result, sec_code)
