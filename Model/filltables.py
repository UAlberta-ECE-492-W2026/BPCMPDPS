import pandas as pd

# to fill tables with disired data
def filltables():
    df=pd.read_csv('../Data/train.csv')
    #add in weekends, holidays, Windchill, humidity, raining
    #Add in regularization
    X=df['Temperature', 'Time', 'Date', 'PreviousPrices'].to_numpy()
    # this is how to pull from the database
    # cfg, _ = ThresholdConfig.objects.get_or_create(user=request.user)
    y=df['Price'].to_numpy()
    return X,y