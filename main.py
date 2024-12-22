
import pandasflow as pdf
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
import sys
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

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

threshold = 0.2

def get_data(mod:str = 'file') -> pd.DataFrame:
    df:pd.DataFrame
    
    if mod == 'file':
        df = pd.read_csv('Data/EURUSD_H1_2015-01-21_2024-10-31.zip')
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    return df

def preprocessing(df:pd.DataFrame) -> pd.DataFrame:
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


    df['y_close'] = df['close'].shift(-1)
    df['y_true'] = (df['close'] < df['y_close']) * 1
    df['y_true_down'] = (df['close'] > df['y_close']) * 1

    return df.dropna()

def get_lists(df:pd.DataFrame) -> list:
    list_base_time = ['time', 'weekday', 'daypart']
    list_base = ['open_change',
        'close_change', 'high_change', 'low_change',
        'open_ratio', 'close_ratio', 'high_low_range', 'log_volume',]

    list_L1_ind = ['rsi', 'sma', 'lma', 'return', 'stoch', 'momentum', 'volatility']
    list_L1_cst = ['shd', 'trend', 'candle_size', 'body_size','upper_wick', 'lower_wick', 'body_to_candle']

    list_cat_feat = ['cls', 'weekday', 'daypart', 'time']

    X1L1 = list_base_time.copy() + list_base.copy()
    for x1 in list_L1_cst:
        for x2 in list(df.columns):
            if x1 in x2: X1L1.append(x2)
    
    X2L1 = list_base_time.copy() + list_base.copy()
    for x1 in list_L1_ind:
        for x2 in list(df.columns):
            if x1 in x2: X2L1.append(x2)
    
    list_L2 = ['predict_R1L1',  'predict_R2L1', 'predict_cls_R1L1', 'predict_cls_R2L1']
    XL2 = list_base_time.copy() + list_L2.copy()

    cat_features = []
    for c1 in list_cat_feat:
        for c2 in list(df.columns):
            if c1 in c2: cat_features.append(c2)
    
    return X1L1, X2L1, XL2, cat_features

def get_inds(df:pd.DataFrame) -> pd.DataFrame:
    df['ind_up'] = ((df['pred_y_up'] - df['pred_y_down']) > threshold).astype(float)
    df.loc[df['ind_up'] != 1, 'ind_up'] = float("NaN")
    df.loc[df['ind_up'] == 1, 'ind_up'] = df['low'] - 0.0003

    df['ind_down'] = ((df['pred_y_down'] - df['pred_y_up']) > threshold).astype(float)
    df.loc[df['ind_down'] != 1, 'ind_down'] = float("NaN")
    df.loc[df['ind_down'] == 1, 'ind_down'] = df['high'] + 0.0003

    return df

def get_metrics(df:pd.DataFrame):
    res = df[['y_true', 'ind_up', 'y_true_down', 'ind_down']]

    res.loc[res['ind_up'] > 0, 'ind_pred'] = 1
    res.loc[res['ind_down'] > 0, 'ind_pred'] = 0

    res = res[(res['ind_pred'] == 1) | (res['ind_pred'] == 0)]

    print(f'THR:\t {threshold}')
    pdf.metrics.metrics_class(res.loc[:,'y_true'], res.loc[:,'ind_pred'])

def main():

    model_R1L1 = CatBoostRegressor().load_model(f"Model/R1L1_{R1L1}.cbm")
    model_R2L1 = CatBoostRegressor().load_model(f"Model/R2L1_{R2L1}.cbm")
    model_C1L2 = CatBoostClassifier().load_model(f"Model/C1L2_{C1L2}.cbm")
    model_C2L2 = CatBoostClassifier().load_model(f"Model/C2L2_{C2L2}.cbm")

    df = get_data()
    df = df.tail(10000)

    df = preprocessing(df)

    X1L1, X2L1, XL2, cat_features = get_lists(df)
    
    def asint(x): return x.astype(int) if x.dtype == float else x
    df[cat_features]  = df[cat_features].apply(asint, axis=0)

    df['predict_R1L1']      = model_R1L1.predict(df[X1L1])
    df['predict_cls_R1L1']  = (df['close'] < df['predict_R1L1']) * 1
    
    df['predict_R2L1']      = model_R2L1.predict(df[X2L1])
    df['predict_cls_R2L1']  = (df.loc[:,'close'] < df.loc[:,'predict_R2L1']) * 1

    df['pred_y_up']         = model_C1L2.predict_proba(df[XL2])[:,1]
    df['pred_y_down']       = model_C2L2.predict_proba(df[XL2])[:,1]

    df = get_inds(df)
    get_metrics(df)

    df.index = pd.to_datetime(df['date'] + " " + df['time'])
    get_graph(df.tail(PLOT_WINDOW_S * PLOT_WINDOW_X), volume=True)
    

if __name__ == "__main__":
    main()