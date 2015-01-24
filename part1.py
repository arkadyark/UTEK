import urllib2
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime

def get_stock_prices(url):
    response = urllib2.urlopen(url)
    values = []
    cr = csv.reader(response)
    for row in cr:
        values.append(float(row[1]))
    return values


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

plot_stock('https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?sort_order=asc&exclude_headers=true&trim_start=2014-01-01&trim_end=2014-12-31&column=4')
