import numpy as np
import joblib
from sklearn.model_selection import train_test_split

from filltables import filltables
from graddesc import gradient_descent
from modelbase import createmodelbase
#create the model
def modelcreate(X,Y):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    Pricemodel=createmodelbase(X_train,y_train)

    return Pricemodel, X_train, y_train, X_test, y_test
#running the model
def loadandrunmodel(X):
    pricemodel=joblib.load('Pricemodel.joblib')
    X_run=X.reshape(-1,1)
    y_run=pricemodel.predict(X_run)
    return X_run,y_run
if __name__=="__main__":
    X,y=filltables()
    Pricemodel, X_train, y_train, X_test, y_test=modelcreate(X,y)
    #Pricemodel = gradient_descent(createmodelbase(X, y), X_train, y_train, 1000, 0.001)
    joblib.dump(Pricemodel, 'Pricemodel.joblib')

    X_run,y_run=loadandrunmodel(X_test)
    print(X_run)
    print(y_run)



