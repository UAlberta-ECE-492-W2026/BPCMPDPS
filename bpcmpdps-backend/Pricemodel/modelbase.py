
import numpy as np

from sklearn.linear_model import LinearRegression

#to create the models base
def createmodelbase(X,y):
    Pricemodel=LinearRegression()
    Pricemodel.fit(X,y)
    #Pricemodel.fit(X_sintrans,y)
    return Pricemodel