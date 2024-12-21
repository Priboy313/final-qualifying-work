import pandas as pd

def set_volume_to_avg(df:pd.DataFrame, 
                      period:int=20) -> pd.DataFrame:
    df['volume_to_avg'] = df['volume'] / df['volume'].rolling(window=period).mean()

    return df