import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import part1
import part2
import part3

def plot_stock(dates, stock_prices):
    '''
    Plots the stock, including the predictions for the future
    '''
    
    coeffs = part3.get_model(stock_prices)
    colours = get_colours(stock_prices)

    for prediction in range(int(0.1*len(stock_prices))):
        dates.append(dates[-1] + 1)
        stock_prices.append(part3.predict(coeffs, stock_prices))
        colours.append(0.0) # Colour all of the predictions the same)

    colours = np.array(colours)

    fig = plt.figure()
    plt.scatter(dates, stock_prices, c=colours, cmap=cm.RdYlGn)
    fig.suptitle('Stock prices over time')
    plt.xlabel('Trading day number in 2014')
    plt.ylabel('Stock price ($)')

    plt.show()

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

def write_trades(dates, trades, profit):
    f = open('output.txt', 'w')
    buying = True
    for trade in trades:
        if buying:
            f.write('You should buy on ' + dates[trade[0]] + '\n')
        else:
            f.write('You should sell on ' + dates[trade[0]] + '\n')
        buying = not buying
    f.write('You will make ' + str(profit))
    f.close()

if __name__ == "__main__":
    company = raw_input('Enter a company name: ')
    dates, stock_prices, original_dates = part1.call_api(company)
    trades, profit = part2.get_max_trades(stock_prices)
    write_trades(original_dates, trades, profit)
    plot_stock(dates, stock_prices)