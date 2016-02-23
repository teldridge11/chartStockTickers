import urllib.request
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests
import collections

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
    
# Parse CSV for daily prices
def parseCSV(ticker, csv_url):
    sourceCode = requests.get(csv_url)
    csv_text = sourceCode.text
    point = []
    points = []
    curDay = 0
    day = []
    commas = 0               
    lines = csv_text.split("\n")
    lineOne = True
    for line in lines:
        commas = 0
        if lineOne == True:
            lineOne = False
        else:
            for c in line:
                if c == ",":
                    commas += 1
                if commas == 4:
                    point.append(c)
                elif commas == 5:
                    for x in point:
                        if x == ",":
                            point.remove(x)
                    point = ''.join(point)
                    point = float(point)
                    points.append(point)
                    day.append(curDay)
                    curDay += 1
                    point = []
                    commas = 0
    points = list(reversed(points))
    plotStock(ticker, points)

# Plot the data
def plotStock(ticker, points):
    plt.plot(points)
    plt.ylabel(ticker)
    plt.show()
