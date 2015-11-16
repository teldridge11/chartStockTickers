import urllib.request
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests

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
