from __future__ import annotations

import math
import random

import numpy as np
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


from sklearn.model_selection import train_test_split
from pathlib import Path
from filltables import filltables
from graddesc import gradient_descent
from featurecreation import FEATURE_COLUMNS

from modelbase import createmodelbase
#create the model
def modelcreate(X,Y):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=random.randint(1,100))
    Pricemodel=createmodelbase(X_train,y_train)

    return Pricemodel, X_train, y_train, X_test, y_test
#running the model
def loadandrunmodel(X,filename):
    pricemodel=joblib.load(filename)
    y_run=pricemodel.predict(X)
    return X,y_run
def checkaccuracy(yrun, y_test):
    ERRORSSE=[]

    for i in range(len(yrun)):
        #MSE
        # calculateing SE
        errorfunctresult=abs(y_test[i] - yrun[i])
        errorfunctdenom=abs(y_test[i] + yrun[i])/2
        errorfunctresult=errorfunctresult/errorfunctdenom
        ERRORSSE.append(errorfunctresult)
    total=sum(ERRORSSE)
    ERROR=total/len(yrun)
    return ERROR



if __name__=="__main__":


    df,y=filltables()
    Pricemodel, X_train, y_train, X_test, y_test=modelcreate(df,y)


    models_dir = Path.cwd() /  "Versions"
    models_dir.mkdir(parents=True, exist_ok=True)
    horizon_steps=12
    vrs=5

    model_filename = f"price_model_h{horizon_steps}_vrs{vrs}.joblib"

    joblib.dump(Pricemodel, models_dir / model_filename)
    vrs+=1
    X_run,y_run=loadandrunmodel(X_test,models_dir/model_filename)
    y_test=y_test.tolist()
    yrun=y_run.tolist()
    MSE=checkaccuracy(yrun,y_test)
    print(yrun)
    print(y_test)
    print(MSE)



