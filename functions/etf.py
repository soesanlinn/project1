#from functions.op_pyxl.op_pyxl import op_pyxl as xl
import pandas as pd
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',2000)
pd.set_option('display.width', 2000)
path = '/Users/ssl/Dropbox/My Files/Excels/ETF Screener/Data/'
source_xl = path + 'ETF Screener 3.0.xlsx'
df = None
df_basket = pd.read_excel(source_xl,'PARAM', usecols="A:G")
df_exclusion = pd.read_excel(source_xl,'PARAM', usecols='I').dropna()
wt_return = dict(pd.read_excel(source_xl,'PARAM', usecols="L:M").dropna().values)
wt_avg_rng_min = dict(pd.read_excel(source_xl,'PARAM', usecols="O:P").dropna().values)
for index, row in df_basket.iterrows():
    df_temp = pd.read_excel(source_xl,row['SUB-CATEGORY'])
    df_temp.insert(loc=0,column='CATEGORY',value=row['CATEGORY'])
    df_temp.insert(loc=1,column='SUB-CATEGORY',value=row['SUB-CATEGORY'])
    if df is not None:
        df = pd.concat([df, df_temp], ignore_index=True, axis=0)
    else:
        df = df_temp
df.drop(df[df['Ticker'].isin(df_exclusion['EXCLUSION LIST'])].index, inplace=True)
df.rename({'1 Month Return':'1M',
           '3 Month Return':'3M',
           '1 Year Return':'1Y',
           '3 Year Return':'3Y',
           '5 Year Return':'5Y',
           '10 Year Return':'10Y'}
          ,axis=1,inplace= True)
df[['1M','3M','1Y','3Y','5Y','10Y','Dividend Yield']]=df[['1M','3M','1Y','3Y','5Y','10Y','Dividend Yield']].replace(to_replace='--',value=0,regex=True)
df_wt_avg = (df['1M'] * wt_return['1M']) +\
            (df['3M'] * wt_return['3M']) +\
            (df['1Y'] * wt_return['1Y']) +\
            (df['3Y'] * wt_return['3Y']) +\
            (df['5Y'] * wt_return['5Y']) +\
            (df['10Y'] * wt_return['10Y'])
df = df.assign(wt_avg = df_wt_avg)
df_min = df[['1M','3M','1Y','3Y','5Y','10Y']].min(axis=1)
df_range = df[['1M','3M','1Y','3Y','5Y','10Y']].max(axis=1) - df_min
return_rank = ((df_wt_avg + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['wt_avg']) +\
                ((df_min + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['min']) +\
                ((df_range + df['Dividend Yield'] - df['Expense Ratio']) * wt_avg_rng_min['range'])
df.insert(loc=0,column='return_rank',value=return_rank)
df = df.sort_values(by=['CATEGORY','SUB-CATEGORY','return_rank'],ascending=[True,True,False])\
    [['return_rank','CATEGORY','SUB-CATEGORY','Ticker','Fund Name','5Y','10Y','wt_avg','Dividend Yield','Expense Ratio']].head(10)
print(df)

#wt_return = pd.read_excel(source_xl,'PARAM', usecols="L:M").dropna().set_index('Period').T.to_dict('list')
# df_result = df.groupby('SUB-CATEGORY',as_index=False).max('return_rank')[['SUB-CATEGORY','return_rank']]
# #left join like in access db - very useful
# df_result = df_result.merge(df[['Ticker','CATEGORY','SUB-CATEGORY','return_rank']], how='left', on=['SUB-CATEGORY','return_rank'])
#to mass-comment, select all lines to comment>Command+/, new field to add under df = df.assign(new_field_name = )
#to-dos
#compile all data from different tabs and attach category and sub-category fields
#create a sub-category weight dictionary
#final result fields = CATEGORY,SUB-CATEGORY,TICKER,Name,weight,df_return,Dividend Yield,Expense Ratio,#shs,USD,Suggested Move USD,Expected Return,Current Return
