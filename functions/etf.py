from functions.op_pyxl.op_pyxl import op_pyxl as xl
import openpyxl
import pandas as pd
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',2000)
pd.set_option('display.width', 2000)
path = '/Users/ssl/Dropbox/My Files/Excels/ETF Screener/Data/'
source_xl = path + 'ETF Screener 3.1.xlsm'
df = None
df_basket = pd.read_excel(source_xl,'HOME', usecols="A:G")
df_exclusion = pd.read_excel(source_xl,'HOME', usecols='L').dropna()
wt_return = dict(pd.read_excel(source_xl,'HOME', usecols="O:P").dropna().values)
wt_avg_rng_min = dict(pd.read_excel(source_xl,'HOME', usecols="R:S").dropna().values)
# Read each tab named by 'SUB-CATEGORY' values and append into a master table called DATA.
for index, row in df_basket.iterrows():
    df_temp = pd.read_excel(source_xl,row['SUB-CATEGORY'])
    df_temp.insert(loc=0,column='CATEGORY',value=row['CATEGORY'])
    df_temp.insert(loc=1,column='SUB-CATEGORY',value=row['SUB-CATEGORY'])
    if df is not None:
        df = pd.concat([df, df_temp], ignore_index=True, axis=0)
    else:
        df = df_temp
# Remove excluded tickers, rename the fields and format zero values.
df.drop(df[df['Ticker'].isin(df_exclusion['EXCLUSION LIST'])].index, inplace=True)
df.rename({'1-Month Total Return':'1M',
           '3-Month Total Return':'3M',
           '1-Year Total Return':'1Y',
           '3-Year Total Return':'3Y',
           '5-Year Total Return':'5Y',
           '10-Year Total Return':'10Y'}
          ,axis=1,inplace= True)
df[['1M','3M','1Y','3Y','5Y','10Y','Dividend Yield','Expense Ratio']]=df[['1M','3M','1Y','3Y','5Y','10Y','Dividend Yield','Expense Ratio']].replace(to_replace='--',value=0,regex=True)
# Weigh the returns -> weighted average returns.
df_wt_avg = (df['1M'] * wt_return['1M']) +\
            (df['3M'] * wt_return['3M']) +\
            (df['1Y'] * wt_return['1Y']) +\
            (df['3Y'] * wt_return['3Y']) +\
            (df['5Y'] * wt_return['5Y']) +\
            (df['10Y'] * wt_return['10Y'])
df = df.assign(wt_avg = df_wt_avg)
df_min = df[['1M','3M','1Y','3Y','5Y','10Y']].min(axis=1)
df_range = df[['1M','3M','1Y','3Y','5Y','10Y']].max(axis=1) - df_min

# Get the overall rank by weighing among return average, minimum and range (i.e. a spread between max and min).
return_rank = ((df_wt_avg + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['wt_avg']) +\
                ((df_min + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['min']) +\
                ((df_range + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['range'])
df.insert(loc=0,column='return_rank',value=return_rank)
df = df.sort_values(by=['CATEGORY','SUB-CATEGORY','return_rank'],ascending=[True,True,False])\
    [['return_rank','CATEGORY','SUB-CATEGORY','Ticker','Fund Name','5Y','10Y','wt_avg','Dividend Yield','Expense Ratio']]
#left join like in access db - very useful
df_result = df.groupby('SUB-CATEGORY',as_index=False).max('return_rank')[['SUB-CATEGORY','return_rank']]
df_result = df_result.merge(df[['Ticker','CATEGORY','SUB-CATEGORY','return_rank']], how='left', on=['SUB-CATEGORY','return_rank'])
# print(df_result)
# df.set_index('Ticker',inplace=True)
# df = df.style.hide_index()
print(df.iloc[0:3])
# # remove previous data.
# wb =  openpyxl.load_workbook(filename=source_xl,read_only=False, data_only=False,
#                             keep_vba=True, keep_links=True)
# sheet = wb['RESULT']
# sheet.delete_rows(1, sheet.max_row)
# wb.save(source_xl)
#
# # update 'DATA' tab.
# mywb = xl(source_xl)
# mywb.update_rng_val('RESULT',df)
