import pandas as pd

def set_rsi_price_change(df:pd.DataFrame) -> pd.DataFrame:
    df['rsi_price_change'] = df['rsi'] * df['close_change']

    return df