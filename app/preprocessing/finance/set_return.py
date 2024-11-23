import pandas as pd


def set_return(df:pd.DataFrame, 
               segments:int=0) -> pd.DataFrame:
    
    df['return'] = df['close'].pct_change()
    
    if segments > 0:
        for i in range(segments):
            shift_ = i + 1
            df[f'return_{shift_}'] = df['return'].shift(shift_)

    return df