
import pandas as pd

def set_stoch(df: pd.DataFrame, 
              segments: int     = 0, 
              abs_seg:  bool    = True, 
              clas:     bool    = True,
              k_period: int     = 14,
              d_period: int     = 3) -> pd.DataFrame:

    n_high = df['high'].rolling(k_period).max()
    n_low = df['low'].rolling(k_period).min()
    df['stoch'] = (df['close'] - n_low) / (n_high - n_low) * 100
    df['stoch'] = (df['close'] - n_low) / (n_high - n_low)
    # df['stoch_d'] = df['stoch'].rolling(d_period).mean()

    if clas:
        df['stoch_cls'] = pd.Series(df['stoch'] * 100).apply(cls_over)
    if segments > 0:
        for i in range(segments):
            shift_ = i+1
            if abs_seg:
                df[f'stoch_{shift_}'] = df['stoch'].shift(shift_)
            if clas:
                df[f'stoch_cls_{shift_}'] = df['stoch_cls'].shift(shift_)

    return df


def cls_over(row, overbuy:int|float=75, oversold:int|float=25) -> int:
    if row > overbuy: return 1
    elif row < oversold: return -1
    else: return 0