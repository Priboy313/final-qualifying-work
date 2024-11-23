
import pandas as pd
import numpy as np
from finance.cls_over import cls_over

def set_rsi(df:pd.DataFrame, 
            segments:   int =   0, 
            abs_seg:    bool=   True, 
            clas:       bool=   True,
            rsi_period: int =   14) -> pd.DataFrame:

    up = pd.Series(np.maximum(df['close'].diff(), 0))
    down = pd.Series(np.maximum(-df['close'].diff(), 0))
    rs = up.rolling(rsi_period).mean() / down.rolling(rsi_period).mean()
    df['rsi'] = 100 - 100/(1 + rs)
    if clas:
        df['rsi_cls'] = df['rsi'].apply(cls_over)

    if segments > 0:
        for i in range(segments):
            shift_ = i + 1
            if abs_seg:
                df[f'rsi_{shift_}'] = df['rsi'].shift(shift_)
            if clas:
                df[f'rsi_cls_{shift_}'] = df['rsi_cls'].shift(shift_)

    del up
    del down
    del rs

    return df