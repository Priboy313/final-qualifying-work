import pandas as pd

def set_volume_to_avg(df:pd.DataFrame) -> pd.DataFrame:
    df['volume_to_avg'] = df['volume'] / df['volume'].rolling(window=20).mean()

    return df