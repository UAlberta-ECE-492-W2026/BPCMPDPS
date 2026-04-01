#new input data application
from Model.graddesc import gradient_descent
from Model.refit import refit

def newdatainputprot(Pricemodel, X, Y, iterations, lrate, newindata,newoutdata):
    X.concat(newindata)
    Y.concat(newoutdata)
    Pricemodel=refit(X,Pricemodel ,Y)
    bias, cost_check, coeff_map = gradient_descent(Pricemodel, X, Y, iterations, lrate)
    Pricemodel.coef_ = coeff_map.values()
    Pricemodel.intercept_ = bias
    return Pricemodel
