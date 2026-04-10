#gradient descent of the model
from featurecreation import FEATURE_COLUMNS
def gradient_descent(Pricemodel, X, Y, iterations, lrate):
    coeff_map=dict(zip(FEATURE_COLUMNS,Pricemodel.coef_))
    bias=Pricemodel.intercept_
    n=len(Y)
    cost_check=[]
    for i in range(iterations):
        ypred=Pricemodel.predict(X)
        cost=(1/n)*sum((Y-ypred)**2)
        cost_check.append(cost)
        d_bias = (2 /n) * sum(ypred - Y)
        #updateparams
        for j in range(len(FEATURE_COLUMNS)):
            dX= (2/n) * sum(coeff_map[FEATURE_COLUMNS[j]] * (ypred - Y))
            dxfin=lrate- dX
            coeff_map[FEATURE_COLUMNS[j]]=dxfin
        biasfin= bias - lrate * d_bias
        bias =biasfin
    return bias, cost_check, coeff_map