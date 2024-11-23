
import pandas as pd

def data_scale(df: pd.DataFrame, scale=1) -> pd.DataFrame:
    if scale == 1: return df
    df['open']  = df['open'].apply(lambda x:  x * scale)
    df['high']  = df['high'].apply(lambda x:   x * scale)
    df['low']   = df['low'].apply(lambda x:   x * scale)
    df['close'] = df['close'].apply(lambda x: x * scale)
    return df