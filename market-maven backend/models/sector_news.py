import requests
import pandas as pd
from datetime import datetime, timedelta
import finnhub
import os


def sectorNews(stock_symbol):

    finnhub_client = finnhub.Client(
        api_key="cin8gnhr01qhp3kcv460cin8gnhr01qhp3kcv46g")

    # Replace 'YOUR_API_KEY' with your actual News API key
    API_KEY = os.environ['NEWS_APIKEY_1']
    BASE_URL = 'https://newsapi.org/v2/everything'

    # Define the category you want to search for (e.g., business, technology, sports, etc.)
    category = finnhub_client.company_profile2(
        symbol=stock_symbol)['finnhubIndustry']

    # Get the current date and the date 8 days ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    # Convert dates to the required format (YYYY-MM-DD)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Prepare the API parameters
    params = {
        'q': category,
        'from': start_date_str,
        'to': end_date_str,
        'apiKey': API_KEY,
        'language': 'en'
    }

    # Send a GET request to the News API
    response = requests.get(BASE_URL, params=params)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if any articles were found
        if data['totalResults'] > 0:
            # Get the list of articles
            articles = data['articles']

            # Create a list to store dictionaries representing articles
            article_list = []
            for article in articles:
                article_dict = {
                    'title': article['title'],
                    'publishedAt': article['publishedAt'],
                }
                article_list.append(article_dict)

            # Create a pandas DataFrame from the list of dictionaries
            df = pd.DataFrame(article_list)
            # Convert the 'publishedAt' column to datetime type for sorting
            df['publishedAt'] = pd.to_datetime(df['publishedAt'])

            # Sort the DataFrame by the 'publishedAt' column in ascending order
            df.sort_values(by='publishedAt', inplace=True)

            # Convert the 'publishedAt' column to date type
            df['publishedAt'] = df['publishedAt'].dt.date

            # Assuming 'df' is your DataFrame
            df.rename(columns={'title': 'headline',
                      'publishedAt': 'datetime'}, inplace=True)

            # Drop duplicate news based on the 'headline' column
            df = df.drop_duplicates(subset=['headline'], keep="last")

            # Reset the index after sorting
            df.reset_index(drop=True, inplace=True)
            df.to_csv('data/sector/sector_news.csv')

            return df

        else:
            return "No articles found."

    return "Failed to fetch articles. Check your API key or try again later."


def specificSectorNews(sector):

    # Replace 'YOUR_API_KEY' with your actual News API key
    API_KEY = os.environ['NEWS_APIKEY_2']
    BASE_URL = 'https://newsapi.org/v2/everything'

    # Get the current date and the date 8 days ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    # Convert dates to the required format (YYYY-MM-DD)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Prepare the API parameters
    params = {
        'q': sector,
        'from': start_date_str,
        'to': end_date_str,
        'apiKey': API_KEY,
        'language': 'en'
    }

    # Send a GET request to the News API
    response = requests.get(BASE_URL, params=params)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if any articles were found
        if data['totalResults'] > 0:
            # Get the list of articles
            articles = data['articles']

            # Create a list to store dictionaries representing articles
            article_list = []
            for article in articles:
                article_dict = {
                    'title': article['title'],
                    'url': article['url'],
                    'urlToImage': article['urlToImage'],
                    'publishedAt': article['publishedAt'],
                    'description': article['description'],
                }
                article_list.append(article_dict)

            # Create a pandas DataFrame from the list of dictionaries
            df = pd.DataFrame(article_list)
            # Convert the 'publishedAt' column to datetime type for sorting
            df['publishedAt'] = pd.to_datetime(df['publishedAt'])

            # Sort the DataFrame by the 'publishedAt' column in ascending order
            df.sort_values(by='publishedAt', inplace=True)

            # Convert the 'publishedAt' column to date type
            df['publishedAt'] = df['publishedAt'].dt.date

            # Assuming 'df' is your DataFrame
            df.rename(columns={'title': 'headline',
                      'publishedAt': 'datetime'}, inplace=True)

            # Drop duplicate news based on the 'headline' column
            df = df.drop_duplicates(subset=['headline'], keep="last")

            # Reset the index after sorting
            df.reset_index(drop=True, inplace=True)
            df.to_csv('data/sector/sector_news.csv')

            return df

        else:
            return "No articles found."

    return "Failed to fetch articles. Check your API key or try again later."
