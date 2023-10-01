import ast
import csv
import pandas as pd
from datetime import datetime, timedelta
import os
import requests


# def companyNews(name):

#     print("Creating Dataframe")
#     # Initialize Finnhub client with your API key
#     finnhub_client = finnhub.Client(
#         api_key="cin8gnhr01qhp3kcv460cin8gnhr01qhp3kcv46g")

#     #python code for symbol lookup
#     # symbols = finnhub_client.symbol_lookup('apple')
#     # print(symbols)

#     # Calculate the date range
#     end_date = datetime.now().date()
#     # end_date = 2023-07-19
#     start_date = end_date - timedelta(days=12)
#     # start_date = 2023-07-11

#     # Fetch the data from the API
#     data = finnhub_client.company_news(name, _from=start_date.strftime(
#         '%Y-%m-%d'), to=end_date.strftime('%Y-%m-%d'))

#     # Convert the UNIX timestamp to datetime
#     for item in data:
#         timestamp = item['datetime']
#         item['datetime'] = datetime.fromtimestamp(timestamp)

#     # Convert the data into a DataFrame
#     df = pd.DataFrame(data)

#     # Save the DataFrame as a CSV file
#     df.to_csv('data/company/company_news.csv', index=False)

#     companyNewsDf = pd.read_csv('data/company/company_news.csv')
#     companyNewsDf['datetime'] = companyNewsDf['datetime'].apply(
#         lambda x: x.split(' ')[0])
#     companyNewsDf.drop(['category', 'id', 'image', 'url'],
#                        axis=1, inplace=True)

#     companyNewsDf.dropna(inplace=True)
#     companyNewsDf.to_csv('data/company/company_news.csv', index=False)

#     # datetime formatting
#     companyNewsDf['datetime'] = companyNewsDf['datetime'].apply(
#         lambda x: x.split(' ')[0])

#     sectorNewsRequest.sector(name)

#     return companyNewsDf

def companyNews(name):
    # Set up the API key and base URL
    api_key = os.environ['NEWS_APIKEY_3']
    base_url = "https://newsapi.org/v2/everything"

    # Set the search parameters
    company = name
    days = 14
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    # Format the dates as required by the API
    date_format = "%Y-%m-%d"
    start_date_str = start_date.strftime(date_format)
    end_date_str = end_date.strftime(date_format)

    # Make the API request
    params = {
        "q": company,
        "apiKey": api_key,
        "from": start_date_str,
        "to": end_date_str,
        "language": "en"
    }
    response = requests.get(base_url, params=params)

    # Process the response
    if response.status_code == 200:
        news_articles = response.json()["articles"]

        # Define the desired CSV file path
        csv_file_path = 'data/company/company_news.csv'

        field_names = news_articles[0].keys()

        with open(csv_file_path, 'w', newline='') as csv_file:
            # Create a CSV writer object
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the column headers to the CSV file
            writer.writeheader()

        # Write each JSON object as a row in the CSV file
            writer.writerows(news_articles)
    else:
        print("Error:", response.status_code)

    df = pd.read_csv('data/company/company_news.csv')
    df.drop(['author'], axis=1, inplace=True)
    # Convert the 'Published At' column to datetime
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df.rename(columns={'publishedAt': 'datetime',
              'title': 'headline'}, inplace=True)
    df['datetime'] = df['datetime'].dt.date

    # Sort the DataFrame by datetime
    dataframe = df.sort_values('datetime')

    dataframe['source'] = dataframe['source'].apply(
        lambda x: ast.literal_eval(x)['name'])

    # datetime formatting
    # dataframe['datetime'] = dataframe['datetime'].apply(lambda x: x.split(' ')[0])
    dataframe['datetime'] = dataframe['datetime'].apply(
        lambda x: x.strftime('%Y-%m-%d'))
    # Drop duplicate news based on the 'headline' column
    dataframe = dataframe.drop_duplicates(subset=['headline'], keep="last")

    dataframe.to_csv('data/company/company_news.csv')
    return dataframe


reader = pd.read_csv('data/stocks_data.csv')
# Function to find stocksymbol from stockname


def find_stock_symbol(company_name):
    for index, row in reader.iterrows():
        column1 = row['Name']
        if column1.lower() == company_name.lower():
            return row['Symbol']
    return None
