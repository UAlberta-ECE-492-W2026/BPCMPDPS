

import pandas as pd
import numpy as np
from featurecreation import build_supervised_dataset
from featurecreation import FEATURE_COLUMNS
# to fill tables with disired data
def filltables():
    df=pd.read_csv("C:\\Users\\ktgar\\PycharmProjects\\BPCMPDPS\\bpcmpdps-backend\\Pricemodel\\data\\Price_weather_training.csv")
    df=build_supervised_dataset(df,12)
    X=df[FEATURE_COLUMNS]
    # this is how to pull from the database
    # cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
    X=sintransformtables(X)
    y=df['target_Price']
    return X,y
def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def sintransformtables(X):
    sintransyearlist = [
    "Price_roll_mean_3",
    "Price_roll_max_3",
    "Price_roll_mean_6",
    "Price_roll_max_6",
    "Price_roll_mean_12",
    "Price_roll_max_12",
    "Price_roll_mean_24",
    "Price_roll_max_24",
    "Price_roll_mean_48",
    "Price_roll_max_48",
    "precipitation_mm",
    "NatGas_price_$perkj"]

    sintransydlist=[
        "Price_lag_1",
        "Price_lag_3",
        "Price_lag_6",
        "Price_lag_12",
        "Price_lag_24",
        "Price_lag_48",
        "Price_lag_168",
        "temperature_c",
        "wind_speed_kph",
        "heating_degree",
        "cooling_degree",
        "humidity",
        "precipitation_mm",
        "temp_x_humidity",
        "feels_like_diff"]

    for i in sintransydlist:
        sintransday=np.sin(2*np.pi*X[i]/24)+np.cos(2*np.pi*X[i]/24)
        sintransyear=np.sin(2*np.pi*X[i]/365)+np.cos(2*np.pi*X[i]/365)
        X[i+"year"]=sintransyear
        X[i+"day"]=sintransday
    for i in sintransyearlist:
        sintransyear = np.sin(2 * np.pi * X[i] / 365)+np.cos(2*np.pi*X[i]/365)
        X[i + "year"] = sintransyear
    return X


gasprice=[
    {"Date": "2020-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.06
  },
  {
    "Date": "2020-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.79
  },
  {
    "Date": "2020-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.6
  },
  {
    "Date": "2020-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.56
  },
  {
    "Date": "2020-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.66
  },
  {
    "Date": "2020-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.65
  },
  {
    "Date": "2020-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.62
  },
  {
    "Date": "2020-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.85
  },
  {
    "Date": "2020-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2
  },
  {
    "Date": "2020-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.99
  },
  {
    "Date": "2020-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.58
  },
  {
    "Date": "2020-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.41
  },
  {
    "Date": "2021-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.32
  },
  {
    "Date": "2021-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3
  },
  {
    "Date": "2021-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.54
  },
  {
    "Date": "2021-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.33
  },
  {
    "Date": "2021-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.56
  },
  {
    "Date": "2021-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.78
  },
  {
    "Date": "2021-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.17
  },
  {
    "Date": "2021-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.78
  },
  {
    "Date": "2021-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.15
  },
  {
    "Date": "2021-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4.01
  },
  {
    "Date": "2021-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4.57
  },
  {
    "Date": "2021-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.99
  },
  {
    "Date": "2022-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.88
  },
  {
    "Date": "2022-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4.26
  },
  {
    "Date": "2022-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4.26
  },
  {
    "Date": "2022-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 5.22
  },
  {
    "Date": "2022-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 5.97
  },
  {
    "Date": "2022-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 6.53
  },
  {
    "Date": "2022-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 5.44
  },
  {
    "Date": "2022-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.55
  },
  {
    "Date": "2022-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4
  },
  {
    "Date": "2022-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.53
  },
  {
    "Date": "2022-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 5.12
  },
  {
    "Date": "2022-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 5.65
  },
  {
    "Date": "2023-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 4.55
  },
  {
    "Date": "2023-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 3.24
  },
  {
    "Date": "2023-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.72
  },
  {
    "Date": "2023-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.24
  },
  {
    "Date": "2023-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2
  },
  {
    "Date": "2023-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.94
  },
  {
    "Date": "2023-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.93
  },
  {
    "Date": "2023-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.24
  },
  {
    "Date": "2023-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.25
  },
  {
    "Date": "2023-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.07
  },
  {
    "Date": "2023-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.3
  },
  {
    "Date": "2023-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.04
  },
  {
    "Date": "2024-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.63
  },
  {
    "Date": "2024-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.73
  },
  {
    "Date": "2024-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.48
  },
  {
    "Date": "2024-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.25
  },
  {
    "Date": "2024-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.01
  },
  {
    "Date": "2024-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.78
  },
  {
    "Date": "2024-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.64
  },
  {
    "Date": "2024-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.53
  },
  {
    "Date": "2024-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.43
  },
  {
    "Date": "2024-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.66
  },
  {
    "Date": "2024-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.33
  },
  {
    "Date": "2024-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.62
  },
  {
    "Date": "2025-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.62
  },
  {
    "Date": "2025-02-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.75
  },
  {
    "Date": "2025-03-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.64
  },
  {
    "Date": "2025-04-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.79
  },
  {
    "Date": "2025-05-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.65
  },
  {
    "Date": "2025-06-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 1.05
  },
  {
    "Date": "2025-07-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.9
  },
  {
    "Date": "2025-08-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.61
  },
  {
    "Date": "2025-09-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.5
  },
  {
    "Date": "2025-10-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 0.95
  },
  {
    "Date": "2025-11-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.04
  },
  {
    "Date": "2025-12-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.71
  },
  {
    "Date": "2026-01-01T00:00:00",
    "Type ": "NatGas",
    "Unit": "$CDN/GJ",
    "Value": 2.46
  }
]