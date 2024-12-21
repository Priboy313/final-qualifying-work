import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def set_volume_scale(df:pd.DataFrame) -> pd.DataFrame:
    scaler = MinMaxScaler()
    df['volume_scaled'] = scaler.fit_transform(df[['volume']])

    return df