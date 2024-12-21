import pandas as pd

def set_body_to_candle(df:pd.DataFrame) -> pd.DataFrame:
    df['body_to_candle'] = df['body_size'] / df['candle_size']

    return df