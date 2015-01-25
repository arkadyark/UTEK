import numpy as np

HISTORY_TO_CONSIDER = 30 # Number of previous prices to look back in prediction

def predict(coeffs, values):
    '''
    Predict the next value, given the coefficients of
    the linear get_model
    '''
    prediction = coeffs[0]
    for i in range(1, len(coeffs)):
        prediction += coeffs[i]*values[-1-i]
    return prediction

def get_model(prices):
    '''
    Train a linear regression model where the features
    are the previous 30 data points
    '''
    prev_prices = [[0] for i in range(HISTORY_TO_CONSIDER)]
    current_price = [prices[0]]
    for stock in range(HISTORY_TO_CONSIDER, len(prices)):
        for prev_price_number in range(HISTORY_TO_CONSIDER):
            prev_prices[prev_price_number].append(prices[max(0, stock-prev_price_number)])
        current_price.append(prices[stock])

    x = np.array(prev_prices)
    y = np.array(current_price)
    n = np.max(x.shape)
    X = np.vstack([np.ones(n), x]).T
    a = np.linalg.lstsq(X, y)
    return a[0]
