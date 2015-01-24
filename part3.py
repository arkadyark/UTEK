import numpy as np

def get_colours(values):
    '''
    Colour the data points to be more red for decreasing prices
    and more green for increasing prices
    '''

    colours = [0]
    for value in range(1, len(values)):
        colours.append(values[value] - values[value - 1])
    max_colour = max(colours)
    scaled_colours = []
    for colour in colours:
        scaled_colours.append(max(0, 0.5*(colour/max_colour + 1)))
    return scaled_colours

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
    prev_prices = [[0] for i in range(30)]
    current_price = [prices[0]]
    for stock in range(30, len(prices)):
        for prev_price_number in range(30):
            prev_prices[prev_price_number].append(prices[max(0, stock-prev_price_number)])
        current_price.append(prices[stock])

    x = np.array(prev_prices)
    y = np.array(current_price)
    n = np.max(x.shape)
    X = np.vstack([np.ones(n), x]).T
    a = np.linalg.lstsq(X, y)
    print a[0]
    return a[0]
