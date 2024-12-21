import numpy as np
import pandas as pd

def set_candle_sizes(df:pd.DataFrame) -> pd.DataFrame:
    df['candle_size'] = df['high'] - df['low']
    df['body_size']   = abs(df['close'] - df['open'])
    df['upper_wick']  = df['high'] - np.maximum(df['close'], df['open'])
    df['lower_wick']  = np.minimum(df['close'], df['open']) - df['low']

    return df