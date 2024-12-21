
import pandasflow as pd
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
import sys
import os

sys.path.append(os.path.abspath("./app/preprocessing"))
sys.path.append(os.path.abspath("./app/visual"))

from app.preprocessing import set_weekday
from app.preprocessing import set_daypart
from app.preprocessing import set_shadows
from app.preprocessing import set_trend
from app.preprocessing import set_volumes
from app.preprocessing import set_change
from app.preprocessing import set_volume_scale
from app.preprocessing import set_ratio
from app.preprocessing import set_log_volume
from app.preprocessing import set_candle_sizes
from app.preprocessing import set_body_to_candle
from app.preprocessing import set_price_volume_change
from app.preprocessing import set_volume_to_avg
from app.preprocessing import set_momentum
from app.preprocessing import set_volatility

from app.preprocessing import set_rsi
from app.preprocessing import set_rsi_price_change
from app.preprocessing import set_sma
from app.preprocessing import set_sma_candle_range
from app.preprocessing import set_lma
from app.preprocessing import set_return
from app.preprocessing import set_stoch

from app.visual import get_graph


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

    df = set_weekday(df)
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
    df = set_daypart(df)
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

    df = set_shadows(df, i_cst)
    df = set_trend(df, i_cst)
    df = set_volumes(df, i_cst)

    df = set_change(df)
    df = set_volume_scale(df)
    df = set_ratio(df)
    df = set_log_volume(df)

    
    df = set_rsi(df, i_ind, clas=True, abs_seg=False)
    df = set_sma(df, i_ind)
    df = set_lma(df, i_ind)
    df = set_return(df, i_ind)
    df = set_stoch(df, i_ind, abs_seg=False)


    df = set_candle_sizes(df)
    df = set_body_to_candle(df)
    df = set_price_volume_change(df)
    df = set_volume_to_avg(df)
    df = set_rsi_price_change(df)
    df = set_sma_candle_range(df)
    df = set_momentum(df)
    df = set_volatility(df)





    df.index = pd.to_datetime(df['date'] + " " + df['time'])
    get_graph(df.tail(PLOT_WINDOW_S * PLOT_WINDOW_X), volume=True)
    

if __name__ == "__main__":
    main()