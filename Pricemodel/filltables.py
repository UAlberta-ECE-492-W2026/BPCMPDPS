import pandas as pd
import numpy as np
from featurecreation import build_supervised_dataset
from featurecreation import FEATURE_COLUMNS
# to fill tables with disired data
def filltables():
    df=pd.read_csv("/Pricemodel/data/Price_weather_testing.csv")


    df=build_supervised_dataset(df,12)

    X=df[FEATURE_COLUMNS]
    # this is how to pull from the database
    # cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
    y=df['target_Price']
    return X,y