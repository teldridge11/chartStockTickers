import urllib.request
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests
import collections
import csv

# Loop to chart multiple stocks
def chartStocks(*tickers):
    for ticker in tickers:
        chartStock(ticker)
        
# Single chart stock method
def chartStock(ticker):
    url = "http://finance.yahoo.com/q/hp?s=" + str(ticker) + "+Historical+Prices"
    sourceCode = requests.get(url)
    plainText = sourceCode.text
    soup = BeautifulSoup(plainText, "html.parser")
    csv = findCSV(soup)
    parseCSV(csv)

# starsWith error
# Find the CSV URL        
def findCSV(soupPage):
    CSV_URL_PREFIX = 'http://real-chart.finance.yahoo.com/table.csv?s='
    links = soupPage.findAll('a')
    for link in links:
        href = link.get('href', '')
        if href.startswith(CSV_URL_PREFIX):
            return href
    
# Parse CSV for daily prices
def parseCSV(csv_text):
    csv_rows = csv.reader(csv_text.split('\n'))

    prices = [float(row[4]) for row in csv_rows]
    days = list(range(len(prices)))
    point = collections.namedtuple('Point', ['x', 'y'])

    for price in prices:
        i = 0
        p = point(days[i], prices[i])
        points = []
        points.append(p)

    plotStock(points)

# Plot the data
def plotStock(points):
    plt.plot(points)
    plt.show()

