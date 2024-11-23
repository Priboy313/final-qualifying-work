import pandas as pd


def set_lma(df:pd.DataFrame, 
            segments:   int = 0,
            long_ma:    int = 12) -> pd.DataFrame:
    
    df['lma'] = df['close'].rolling(long_ma).mean()
    if segments > 0:
        for i in range(segments):
            shift_ = i + 1
            df[f'lma_{shift_}'] = df['lma'].shift(shift_)

    return df