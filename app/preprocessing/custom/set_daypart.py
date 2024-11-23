import pandas as pd
from datetime import datetime


def set_daypart(df:pd.DataFrame) -> pd.DataFrame:
    
    def get_daypart(time):
        
        if 6 <= time.hour < 12:
            return "Morning"
        elif 12 <= time.hour < 18:
            return "Day"
        elif 18 <= time.hour < 22:
            return "Evening"
        else:
            return "Night"
    
    df['daypart'] = df['datetime'].apply(get_daypart)
    
    return df