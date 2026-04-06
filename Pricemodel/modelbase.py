
import numpy as np

from sklearn.linear_model import LinearRegression

#to create the models base
def createmodelbase(X,y):
    #X_sintrans=np.hstack(
        #[np.sin(2*np.pi*X.Tempature/24),
         #np.cos(2*np.pi*X.Tempature/24),
         #np.sin(2*np.pi*X.Time/24),
         #np.cos(2*np.pi*X.Time/24),
        # X.Date, X.Prices])
    Pricemodel=LinearRegression()
    Pricemodel.fit(X,y)
    #Pricemodel.fit(X_sintrans,y)
    return Pricemodel