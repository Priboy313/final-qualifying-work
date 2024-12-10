
import pandasflow as pd
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
import sys
import os

sys.path.append(os.path.abspath("./app/visual"))
from app.visual import get_graph


R1L1 = 7
R2L1 = 7
C1L2 = 7
C2L2 = 7

PLOT_WINDOW_S = 24
PLOT_WINDOW_X = 7


def main():
    model_R1L1 = CatBoostRegressor().load_model(f"Model/R1L1_{R1L1}.cbm")
    model_R2L1 = CatBoostRegressor().load_model(f"Model/R2L1_{R2L1}.cbm")
    
    model_C1L2 = CatBoostClassifier().load_model(f"Model/C1L2_{C1L2}.cbm")
    model_C2L2 = CatBoostClassifier().load_model(f"Model/C2L2_{C2L2}.cbm")
    
    data = pd.read_csv('Data/test_m7.csv')
    data.index = pd.to_datetime(data['date'] + " " + data['time'])

    get_graph(data.tail(PLOT_WINDOW_S * PLOT_WINDOW_X), volume=True)
    

if __name__ == "__main__":
    main()