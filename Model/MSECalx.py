
from sklearn.metrics import mean_squared_error

#to create the MSE calc for the gradient descent
def MSECalc(price_true, price_pred):
    return mean_squared_error(price_true, price_pred)