import pandas as pd

def set_momentum(df:pd.DataFrame,
                 k:int = 5) -> pd.DataFrame:
    df['momentum'] = df['close'] - df['close'].shift(k)

    return df