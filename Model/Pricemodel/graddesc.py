#gradient descent of the model
def gradient_descent(Pricemodel, X, Y, iterations, lrate):
    feature_names=['Temperature', 'Time', 'Date', 'PreviousPrices']
    coeff_map=dict(zip(feature_names,Pricemodel.coef_))
    bias=Pricemodel.intercept_
    n=len(Y)
    cost_check=[]
    for i in range(iterations):
        ypred=Pricemodel.predict(X)
        cost=(1/n)*sum((Y-ypred)**2)
        cost_check.append(cost)
        d_bias = (2 /n) * sum(ypred - Y)
        #updateparams
        for j in range(len(feature_names)):
            dX= (2/n) * sum(coeff_map[feature_names[j]] * (ypred - Y))
            coeff_map[feature_names[j]]=lrate- dX
        bias = bias - lrate * d_bias
    return bias, cost_check, coeff_map