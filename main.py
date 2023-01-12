import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import datetime as dt 
import statistics as st
import csv

from stock_checker import check_stock

#input loop
isValid = False

while not isValid:
    symbol = input("Enter Stock Ticker: ")
    isValid = check_stock(symbol)

iterations = int(input("Amount of interations: "))

stockData = yf.download(symbol)



# pulls the return data and calculates random return values
returns = np.log(1 + stockData['Adj Close'].pct_change())
mu, sigma= returns.mean(), returns.std()

# most recent price of stock
recentPrice = stockData['Adj Close'].iloc[-1]

# lists to keep track of all the simulated prices created
simulatedEndPrices = []
simulatedPricesTotal = []

# store overall max and min estimations
overallMax = recentPrice
overallMin = recentPrice

# value of range determines how many simulations are run
for i in range(iterations):
    simulationReturns = np.random.normal(mu, sigma, 252)
    simulatedPrices = recentPrice * (simulationReturns + 1).cumprod()
    simulatedEndPrices.append(simulatedPrices[-1])
    simulatedPricesTotal.append(simulatedPrices)

    tempMax = max(simulatedPrices)
    tempMin = min(simulatedPrices)

    if tempMax > overallMax:
        overallMax = tempMax
    
    if tempMin < overallMin:
        overallMin = tempMin

    plt.plot(simulatedPrices)

# calculation of final statistics
endMean = st.mean(simulatedEndPrices)
endStd = st.stdev(simulatedEndPrices)
endMax = max(simulatedEndPrices)
endMin = min(simulatedEndPrices)
endAvgPctChng = ((recentPrice - endMean) / recentPrice) * 100

print("starting price:", recentPrice)
print("mean of end prices:",endMean)
print("stdev of end prices:",endStd)
print("min and max of end prices:", endMin, endMax)
print("average percent change", endAvgPctChng)
print(len(simulatedEndPrices))

print("These are the overall max and mins", overallMax, overallMin)

#date formatting
year = dt.datetime.now().year
month = dt.datetime.now().month
day = dt.datetime.now().day
minute = dt.datetime.now().minute
second = dt.datetime.now().second


# adding axes and title of the chart
plt.axhline(recentPrice, c='k')
plt.title(symbol + " Monte Carlo Simulation")

# adding x y axis labels
plt.xlabel(f'Days after {year}/{month}/{day}')
plt.ylabel('Stock Price ($ USD)')

#plotting horizontal lines on max and min predicted final prices
plt.axhline(y=endMax, color='r', label='final max price')
plt.axhline(y=endMin, color='b', label='final min price')

#plotting the overall highest and lowest prices
plt.axhline(y=overallMax, color='g', label='overall max price')
plt.axhline(y=overallMin, color='y', label='overall min price')

#plotting legend
plt.legend()

#name generation
specName = f'{symbol}_MonteCarlo_{year}-{month}-{day}-{minute}-{second}.png'

#saving plot
plt.savefig(os.path.join('plots', specName))


# save Data to Excel spreadsheet
headers = [
    "Starting Price",
    "Mean end price",
    "STDEV end price",
    "Max end price",
    "Min end price",
    "Average percent change in price",
    "Overall max price",
    "Overall min price"
]

data = [
    recentPrice,
    endMean,
    endStd,
    endMax,
    endMin,
    endAvgPctChng,
    overallMax,
    overallMin
]

cvsName = f"spreadsheets/{symbol}_Analysis_{year}-{month}-{day}-{minute}-{second}.csv"

with open(cvsName, "w", newline='') as stock_data:
    writer_main = csv.writer(stock_data)
    writer_main.writerow(headers)
    writer_main.writerow(data)
    writer_main.writerow('\n')
    writer_main.writerow(['Simulation Data'])
    writer_main.writerow(['Iteration', 'Data'])

    for i in range(iterations):
        curr_data = np.concatenate(([int(i)], simulatedPricesTotal[i]))
        writer_main.writerow(curr_data)
     