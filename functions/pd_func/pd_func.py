import pandas as pd
class pd_func:
    def filter(df: pd.DataFrame, filter_dict: dict) -> dict:
        result = df.copy()
        for key, value_list in filter_dict.items():
            result = result[result[key].str.contains('|'.join(value_list))]
        return result

    def sumifs(df: pd.DataFrame, filter_dict: dict, sum_col: str) -> float:
        result = df.copy()
        for key, value_list in filter_dict.items():
            result = result[result[key].str.contains('|'.join(value_list))]
        return result[sum_col].sum()



    # unused
    # pviot = pd.pivot_table(df, values= 'Size', index= ['Stock'], columns= None, aggfunc= np.sum)
    # result = df.iloc[0:0] # empty df (columns included)
    # tempdf.drop(tempdf.index[is_new_entry], inplace= True) # is_new_entry = bool
    # result = pd.concat([result, tempdf[is_new_entry]]) # adding more lines