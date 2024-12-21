import pandas as pd 

def set_volatility(df:pd.DataFrame,
                   k:int=20) -> pd.DataFrame:
    
    df['volatility'] = df['close'].rolling(window=k).std()

    return df