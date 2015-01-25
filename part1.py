import urllib2
import csv
from datetime import datetime
from matplotlib.dates import date2num

def call_api(company):
    '''
    Gets dates and stock_prices from an API call
    '''
    url = 'https://www.quandl.com/api/v1/datasets/WIKI/' + company + \
        '.csv?sort_order=asc&exclude_headers=true&trim_start=2014-01-01' + \
        '&trim_end=2014-12-31&column=4&auth_token=t6nJNUYrmEYrJjyE7tsV'

    response = urllib2.urlopen(url)
    dates = []
    stock_prices = []
    original_dates = []
    cr = csv.reader(response)
    for row in cr:
        split_date = row[0].split('-')
        dates.append(date2num(datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))))
        original_dates.append(row[0])
        stock_prices.append(float(row[1]))
    return dates, stock_prices, original_dates