import pandas as pd

def set_ratio(df:pd.DataFrame) -> pd.DataFrame:
    df['open_ratio']     = (df['open']  - df['low']) / (df['high'] - df['low'])
    df['close_ratio']    = (df['close'] - df['low']) / (df['high'] - df['low'])
    df['high_low_range'] = df['high']   - df['low']

    return df