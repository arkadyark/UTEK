import urllib2
import csv

def print_response(url):
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    for row in cr:
        print row

print_response('https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?sort_order=asc&trim_start=2014-01-01&trim_end=2014-12-31&column=4')
