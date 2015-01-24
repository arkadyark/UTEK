import urllib2
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime

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
        value -= values[trades[2*i]]
        value += values[trades[2*i + 1]]
    return value

def get_max_trades(values, n = 5):
    print values
    min_stock = min(values)
    min_index = values.index(min_stock)
    max_stock = max(values)
    max_index = values.index(max_stock)
    if n == 1:
        trades = [min_index, max_index]
        value = get_value(trades, values)
        return trades, value

def get_peaks(values, num_neighbors = 15, max_peaks = True):
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
            peaks.append(value_index)
    return peaks


url = 'https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?sort_order=asc&exclude_headers=true&trim_start=2014-01-01&trim_end=2014-12-31&column=4'
print get_max_trades(get_stock_prices(), 1)
peaks = get_peaks(get_stock_prices(), max_peaks = True)
peaks = get_peaks(get_stock_prices(), max_peaks = False)
for peak in peaks:
    print peak, get_stock_prices()[peak]

def plot_stock(url):
    response = urllib2.urlopen(url)
    dates = []
    values = []
    cr = csv.reader(response)
    for row in cr:
        split_date = row[0].split('-')
        dates.append(date2num(datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))))
        values.append(float(row[1]))
    plt.plot_date(dates, values)
    plt.show()

#plot_stock('https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?sort_order=asc&exclude_headers=true&trim_start=2014-01-01&trim_end=2014-12-31&column=4')
