# Set the symbol of the company you want to fetch data for
from datetime import datetime, timedelta

import pandas as pd
import yfinance


def stockdata(i, name):
    symbol = name  # Replace with your desired company symbol

    # Get the current date
    current_date = datetime.now().date()

    # Calculate the start date (8 days ago)
    start_date = current_date - timedelta(days=12)

    # Fetch the historical stock prices
    data = yfinance.download(symbol, start=start_date, end=current_date)

    # Save the data as a CSV file
    data.to_csv('data/company/company_stock_prices.csv')

    stockDataDf = pd.read_csv('data/company/company_stock_prices.csv')
    stockDataDf.drop(['Adj Close', 'Volume'], axis=1, inplace=True)

    # stockDataDf.head(10)

    #  Create a shifted column with previous day's close price
    stockDataDf['Previous_Close'] = stockDataDf['Close'].shift(1)

    # Compare close price with previous day's close price and store the result
    stockDataDf['Status'] = stockDataDf['Close'] - \
        stockDataDf['Previous_Close']

    # Convert result to 'Increased' or 'Decreased' based on sign
    stockDataDf['Status'] = stockDataDf['Status'].apply(
        lambda x: 'Increased' if x > 0 else 'Decreased')

    stockDataDf.fillna(0, inplace=True)
    stockDataDf.rename(columns={'Date': 'datetime'}, inplace=True)

    if (i == 'Apple'):
        # stockDataDf=stockDataDf.assign(name='Apple')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AAPL.svg")

    elif (i == 'Netflix'):
        # stockDataDf=stockDataDf.assign(name='Domino\'s Pizza')
        stockDataDf = stockDataDf.assign(
            icon='https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/NFLX.svg')

    elif (i == 'eBay'):
        # stockDataDf = stockDataDf.assign(name='eBay')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/EBAY.svg")

    elif (i == 'Walmart'):
        # stockDataDf = stockDataDf.assign(name='Walmart')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/WMT.svg")

    elif (i == 'FedEx'):
        # stockDataDf = stockDataDf.assign(name='FedEx')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/FDX.svg")

    elif (i == 'Goldman Sachs'):
        stockDataDf = stockDataDf.assign(name='Goldman Sachs')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/GS.svg")

    elif (i == 'IBM'):
        # stockDataDf = stockDataDf.assign(name='IBM')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/IBM.svg")

    elif (i == 'JPMorgan Chase'):
        stockDataDf = stockDataDf.assign(name='JPMorgan Chase')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/JPM.svg")

    elif (i == 'Microsoft'):
        # stockDataDf = stockDataDf.assign(name='Microsoft')
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/MSFT.svg")

    elif (i == 'Amazon'):
        stockDataDf = stockDataDf.assign(
            icon="https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AMZN.svg")

    stockDataDf.to_csv('data/company/company_stock_prices.csv')
    stockDataDf.fillna(0, inplace=True)
    return stockDataDf
