import numpy as np
import pandas as pd

def set_log_volume(df:pd.DataFrame) -> pd.DataFrame:
    df['log_volume'] = np.log1p(df['volume'])

    return df