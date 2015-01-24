import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib import cm
import part1
import part2
import part3

def plot_stock(dates, stock_prices):
    '''
    Plots the stock, including the predictions for the future
    '''
    
    coeffs = part3.get_model(stock_prices)
    colours = np.array(get_colours(stock_prices))

    for prediction in range(int(0.1*len(stock_prices))):
        dates.append(dates[-1] + 1)
        stock_prices.append(predict(coeffs, stock_prices))
        np.append(colours, 1.0)

    plt.scatter(dates, stock_prices, c=colours, cmap=cm.RdYlGn)
    plt.show()

if __name__ == "__main__":
    company = raw_input('Enter a company name: ')
    try:
        dates, stock_prices = part1.call_api(company)
        trades = part2.get_max_trades(stock_prices)
        plot_stock(dates, stock_prices)

    except Exception:
        print 'HTTP Error. Perhaps you entered the wrong company name?'