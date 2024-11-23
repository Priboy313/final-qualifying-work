import pandas as pd


def set_volumes(df: pd.DataFrame, segments=1) -> pd.DataFrame:
    for i in range(segments):
        shift_ = i + 1
        df[f'volume_{shift_}'] = df['volume'].shift(shift_).fillna(0).astype(int)
    return df