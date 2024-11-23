import pandas as pd


def set_trend(df: pd.DataFrame, segments=0) -> pd.DataFrame:
    df['trend_cls'] = (df['close'] > df['open']) * 1
    if segments > 0:
        for i in range(segments):
            shift_ = i + 1
            df[f'trend_cls_{shift_}'] = df['trend_cls'].shift(shift_).fillna(0).astype(int)
    return df