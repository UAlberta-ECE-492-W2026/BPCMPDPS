import random

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# to fill tables with desired data


#to create the train test split
def TrainTestSplit(X,y):
   TempTrain, Temptest, Timetrain, Timetest, Datetrain, DateTest, PPTrain, PPtest  = train_test_split(X,y, test_size=0.2, random_state=random.randint(0,100), stratify=y)
   return TempTrain, Temptest, Timetrain, Timetest, Datetrain, DateTest, PPTrain, PPtest