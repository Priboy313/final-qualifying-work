import pandas as pd
from datetime import datetime

def set_daypart(df:pd.DataFrame) -> pd.DataFrame:
    
    def get_daypart(time):
        
        if 6 <= time.hour < 12:
            daypart = "Morning"
        else:
            if 12 <= time.hour < 18:
                daypart = "Day"
            else:
                if 18 <= time.hour < 22:
                    daypart = "Evening"
                else:
                    daypart = "Night"
        
        return daypart
    
    def apply_daypart(row):
        time = row['datetime']
        daypart = get_daypart(time)
        return daypart
    
    df['daypart'] = df.apply(apply_daypart, axis=1)
    
    return df

def main():
    data = {
        'datetime': [
            datetime(2023, 10, 1, 8, 0),
            datetime(2023, 10, 1, 13, 0),
            datetime(2023, 10, 1, 19, 0),
            datetime(2023, 10, 1, 23, 0)
        ]
    }
    
    df = pd.DataFrame(data)
    df = set_daypart(df)
    print(df)

if __name__ == "__main__":
    main()