import pandas as pd

def set_sma_candle_range(df:pd.DataFrame,
                         period:int=20) -> pd.DataFrame:
    df['sma_candle_range'] = df['candle_size'] / df['close'].rolling(window=period).mean()

    return df