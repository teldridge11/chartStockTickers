import urllib
from urllib.request import urlopen
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
    parseCSV(ticker, csv)

# Find the CSV URL        
def findCSV(soupPage):
    CSV_URL_PREFIX = 'http://real-chart.finance.yahoo.com/table.csv?s='
    links = soupPage.findAll('a')
    for link in links:
        href = link.get('href', '')
        if href.startswith(CSV_URL_PREFIX):
            return href

def parseCSV(ticker, csv_url):
    response = urlopen(csv_url)
    reader = csv.reader(response.read().decode('utf-8').splitlines())
    csv_rows = [row for row in reader]
    prices = [row[4] for row in csv_rows if len(row) > 4]
    points = []
    i = 0
    for price in prices[1:]:
        points.append(price)
        i += 1
    plotStock(ticker, points[::-1])

# Plot the data
def plotStock(ticker, points):
    plt.plot(points)
    plt.ylabel(ticker)
    plt.show()
