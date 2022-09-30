import pandas as pd

class dict_func:
    # Excel sumifs equivalent
    def sumpivot(input_dict: dict, lookup_cols: str, sum_col: str) -> dict:
        sum_dict = {}
        is_multi_lookupcols = False
        if '|' in lookup_cols:
            is_multi_lookupcols = True
            lookup_col_list = lookup_cols.split('|')
        for i in input_dict:
            lookup_val = ''
            if is_multi_lookupcols:
                for lookup_col in lookup_col_list:
                    lookup_val = ('' if lookup_val == '' else lookup_val + '|') + input_dict[i][lookup_col]
            else:
                lookup_val = input_dict[i][lookup_cols]
            sum_val = input_dict[i][sum_col]
            if lookup_val in sum_dict:
                sum_dict[lookup_val] += sum_val
            else:
                sum_dict[lookup_val] = sum_val
        return sum_dict

    # Convert df (or dict) into dict (or df)
    def convert_dict_df(data):
        if type(data) == pd.DataFrame:
            return data.to_dict('index')
        elif type(data) == dict:
            return pd.DataFrame(data).T

