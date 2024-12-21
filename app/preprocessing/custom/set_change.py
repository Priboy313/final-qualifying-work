
import pandas as pd

def set_change(df:pd.DataFrame) -> pd.DataFrame:
    df['open_change']  = (df['open']  - df['close'].shift(1)) / df['close'].shift(1)
    df['close_change'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
    df['high_change']  = (df['high']  - df['close'].shift(1)) / df['close'].shift(1)
    df['low_change']   = (df['low']   - df['close'].shift(1)) / df['close'].shift(1)

    return df