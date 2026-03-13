import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


df=pd.read_csv('../Data/train.csv')
X=df['Temperature', 'Time', 'Date', 'PreviousPeak']

y=df['Power']
X_sintrans=np.hstack([np.sin(2*np.pi*X.Tempature/24),np.cos(2*np.pi*X.Tempature/24),np.sin(2*np.pi*X.Time/24),np.cos(2*np.pi*X.Time/24),X.Date, X.PreviousPeak])
Pricemodel=LinearRegression()
Pricemodel.fit(X_sintrans,y)
Powermodel=LinearRegression()
Powermodel.fit(X,y)