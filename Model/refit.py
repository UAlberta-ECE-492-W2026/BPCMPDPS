
import numpy as np

#to refit data once it has been introduced
def refit(newInfo,Pricemodel ,Y):
    newinfosintrans=np.hstack([np.sin(2*np.pi*newInfo.Tempature/24),np.cos(2*np.pi*newInfo.Tempature/24),np.sin(2*np.pi*newInfo.Time/24),np.cos(2*np.pi*newInfo.Time/24),newInfo.Date, newInfo.PreviousPrices])
    Pricemodel.partial_fit(newinfosintrans,Y)
    return Pricemodel
