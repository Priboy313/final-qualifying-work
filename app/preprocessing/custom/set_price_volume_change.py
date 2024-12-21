import pandas as pd


def set_price_volume_change(df:pd.DataFrame) -> pd.DataFrame:
    df['price_volume_change'] = df['close_change'] * df['volume']
    
    return df