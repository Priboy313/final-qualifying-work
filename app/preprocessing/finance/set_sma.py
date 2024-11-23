import pandas as pd


def set_sma(df:pd.DataFrame, 
            segments: int = 0,
            short_ma: int = 5) -> pd.DataFrame:
    
    df['sma'] = df['close'].rolling(short_ma).mean()
    if segments > 0:
        for i in range(segments):
            shift_ = i + 1
            df[f'sma_{shift_}'] = df['sma'].shift(shift_)

    return df