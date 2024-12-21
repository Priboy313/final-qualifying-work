
import pandasflow as pd
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
import sys
import os

sys.path.append(os.path.abspath("./app/preprocessing"))
sys.path.append(os.path.abspath("./app/finance"))
sys.path.append(os.path.abspath("./app/visual"))

from app.visual import get_graph
from app import preprocessing


R1L1 = 7
R2L1 = 7
C1L2 = 7
C2L2 = 7

PLOT_WINDOW_S = 24
PLOT_WINDOW_X = 7

i_cst = 10
i_ind = 10


def main():
    model_R1L1 = CatBoostRegressor().load_model(f"Model/R1L1_{R1L1}.cbm")
    model_R2L1 = CatBoostRegressor().load_model(f"Model/R2L1_{R2L1}.cbm")
    
    model_C1L2 = CatBoostClassifier().load_model(f"Model/C1L2_{C1L2}.cbm")
    model_C2L2 = CatBoostClassifier().load_model(f"Model/C2L2_{C2L2}.cbm")
    
    df = pd.read_csv('Data/EURUSD_H1_2015-01-21_2024-10-31.zip')
    df.columns = ['date', 
                  'open', 
                  'high', 
                  'low', 
                  'close', 
                  'volume'
                  ]

    df['datetime'] = pd.to_datetime(df['date'])
    df.index = pd.to_datetime(df['date'])
    df[['date', 'time']] = df['date'].str.split(' ', expand=True)[[0, 1]]
    df = df[
            ['datetime', 
            'date', 
            'time', 
            'open', 
            'high', 
            'low', 
            'close', 
            'volume']
        ]

    df = preprocessing.set_weekday(df)
    df = df[
            ['datetime', 
             'date', 
             'weekday', 
             'time', 
             'open', 
             'high', 
             'low', 
             'close', 
             'volume']
        ]
    df = preprocessing.set_daypart(df)
    df = df[
            ['date', 
             'weekday', 
             'time', 
             'daypart', 
             'open', 
             'high', 
             'low', 
             'close', 
             'volume']
            ]

    df = preprocessing.set_shadows(df, i_cst)
    df = preprocessing.set_trend(df, i_cst)
    df = preprocessing.set_volumes(df, i_cst)

    df = preprocessing.set_change(df)
    df = preprocessing.set_volume_scale(df)
    df = preprocessing.set_ratio(df)
    df = preprocessing.set_log_volume(df)

    
    df = preprocessing.set_rsi(df, i_ind, clas=True, abs_seg=False)
    df = preprocessing.set_sma(df, i_ind)
    df = preprocessing.set_lma(df, i_ind)
    df = preprocessing.set_return(df, i_ind)
    df = preprocessing.set_stoch(df, i_ind, abs_seg=False)




    df.index = pd.to_datetime(df['date'] + " " + df['time'])
    get_graph(df.tail(PLOT_WINDOW_S * PLOT_WINDOW_X), volume=True)
    

if __name__ == "__main__":
    main()