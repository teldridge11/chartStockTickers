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

def chartStocks(*tickers):

    # Run loop for each ticker passed in as an argument
    for ticker in tickers:
    
        # Convert URL into text for parsing
        url = "http://finance.yahoo.com/q/hp?s=" + str(ticker) + "+Historical+Prices"
        sourceCode = requests.get(url)
        plainText = sourceCode.text
        soup = BeautifulSoup(plainText, "html.parser")
        
        # Find all links on the page
        for link in soup.findAll('a'):
            href = link.get('href')
            link = []
            for c in href[:48]:
                link.append(c)
            link = ''.join(link)
            
            # Find the URL for the stock ticker CSV file and convert the data to text
            if link == "http://real-chart.finance.yahoo.com/table.csv?s=":
                csv_url = href
                res = urllib.request.urlopen(csv_url)
                csv = res.read()
                csv_str = str(csv)
                
                # Parse the CSV to create a list of data points
                point = []
                points = []
                curDay = 0
                day = []
                commas = 0               
                lines = csv_str.split("\\n")
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
                
                # Plot the data
                plt.plot(day,points)
                plt.ylabel(ticker)
                plt.show()
