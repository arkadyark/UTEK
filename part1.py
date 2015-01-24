import urllib2
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib import cm

def get_stock_prices():
    f = open('part1_output.txt')
    prices = []
    for row in f:
        prices.append(float(eval(row)[1]))
    return prices

def get_value(trades, values):
    # Helper function to get the value of a set of trades
    value = 0
    for i in range(len(trades)/2):
        value -= trades[2*i][1]
        value += trades[2*i + 1][1]
    return value

def get_max_trades(values, n = 5):
    nn = 10
    trades = []
    previous_state = None
    while True:
        minima = get_peaks(values, nn, False)
        maxima = get_peaks(values, nn, True)
        trades = get_trades(minima, maxima)
        if trades != -1:
            if previous_state == 'working' or previous_state == None:
                print trades
                print get_value(trades, values)
                previous_state = 'working'
                nn += 1
            else:
                minima = get_peaks(values, nn, False)
                maxima = get_peaks(values, nn, True)
                trades = get_trades(minima, maxima)
                break
        else:
            if previous_state == 'not working' or previous_state == None:
                previous_state = 'not working'
                nn -= 1
            else:
                minima = get_peaks(values, nn - 1, False)
                maxima = get_peaks(values, nn - 1, True)
                trades = get_trades(minima, maxima)
                break

    return trades

def get_trades(minima, maxima, n = 5):
    if len(minima) < 5 or len(maxima) < 5:
        return -1
    trades = []
    buy_index = 0
    sell_index = 0
    # Check if we can alternate between minima and maxima for n trades
    for trade_number in range(n):
        buy = minima[buy_index]
        sell = maxima[sell_index]
        if len(trades) > 0 and buy[0] < trades[-1][0]:
            # You can't buy/sell twice in a row!
            while (buy_index < len(minima) and minima[buy_index][0] < trades[-1][0]):
                buy_index += 1
            if buy_index >= len(maxima):
                return -1
            else:
                trades.append(minima[buy_index])
                trades.append(sell)

        elif sell[0] < buy[0]:
            # You can't sell before you buy!
            while (sell_index < len(maxima) and minima[buy_index][0] > maxima[sell_index][0]):
                sell_index += 1
            if sell_index >= len(maxima):
                return -1
            else:
                trades.append(buy)
                trades.append(maxima[sell_index])
                buy_index += 1
                sell_index += 1
        else:
            trades.append(buy)
            trades.append(sell)
            buy_index += 1
            sell_index += 1
    return trades
    
def get_peaks(values, num_neighbors = 10, max_peaks = True):
    peaks = []
    for value_index in range(num_neighbors, len(values) - num_neighbors):
        value = values[value_index]
        not_a_peak = False
        for neighbor_index in range(num_neighbors):
            if max_peaks:
                if value < values[value_index - neighbor_index]:
                    not_a_peak = True
                    break
                if value < values[value_index + neighbor_index]:
                    not_a_peak = True
                    break
            else:
                if value > values[value_index - neighbor_index]:
                    not_a_peak = True
                    break
                if value > values[value_index + neighbor_index]:
                    not_a_peak = True
                    break
        if not_a_peak:
            continue
        else:
            peaks.append((value_index, values[value_index]))
    return peaks


url = 'https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?sort_order=asc&exclude_headers=true&trim_start=2014-01-01&trim_end=2014-12-31&column=4'
print get_max_trades(get_stock_prices(), 1)

def plot_stock():
    f = open('part1_output.txt')
    dates = []
    values = []
    for row in f:
        row = eval(row)
        split_date = row[0].split('-')
        dates.append(date2num(datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))))
        values.append(float(row[1]))
    colours = get_colours(values)
    plt.scatter(dates, values, c=colours, cmap=cm.seismic)
    plt.show()

def get_colours(values):
    colours = [0]
    for value in range(1, len(values)):
        colours.append(values[value] - values[value - 1])
    max_colour = max(colours)
    scaled_colours = []
    for colour in colours:
        scaled_colours.append(str(max(0, 0.5*(colour/max_colour + 1))))

    return scaled_colours

if __name__ == "__main__":
    plot_stock()
