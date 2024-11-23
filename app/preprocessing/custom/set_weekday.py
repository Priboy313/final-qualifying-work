from datetime import datetime
import pandas as pd

def set_weekday(df:pd.DataFrame) -> pd.DataFrame:

    df['weekday'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y.%m.%d').strftime("%A"))
    
    return df