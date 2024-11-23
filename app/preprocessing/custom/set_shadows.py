import pandas as pd

def set_shadows(df: pd.DataFrame, segments=1) -> pd.DataFrame:
    df['grn_shd'] = df['high'] - df['close']
    df['red_shd'] = df['open'] - df['low']

    for i in range(segments):
        shift_ = i + 1
        df[f'grn_shd_{shift_}'] = df['high'].shift(shift_) - df['close'].shift(shift_)
        df[f'red_shd_{shift_}'] = df['open'].shift(shift_) - df['low'].shift(shift_)

    return df