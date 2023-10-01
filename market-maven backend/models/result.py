import pandas as pd
import models.companySentimentCount as companySentimentCount


def modelResult():

    company_df = pd.read_csv('data/company/company_dated_sentiment.csv')

    sector_df = pd.read_csv('data/sector/sector_dated_sentiment.csv')

    stock_df = pd.read_csv('data/company/company_stock_prices.csv')

    # Custom function to map 'Status' to sentiment labels

    def map_status_to_sentiment(status):
        if status == "Increased":
            return "Positive"
        elif status == "Decreased":
            return "Negative"
        else:
            return "Neutral"

    # Add the 'Sentiment' column using the custom function
    stock_df['sentiment'] = stock_df['Status'].apply(map_status_to_sentiment)

    # Convert 'datetime' columns to datetime data type
    company_df['datetime'] = pd.to_datetime(company_df['datetime'])
    sector_df['datetime'] = pd.to_datetime(sector_df['datetime'])
    stock_df['datetime'] = pd.to_datetime(stock_df['datetime'])

    # Shift the 'sentiment' column in company and sector dataframes one day backward
    company_df['sentiment'] = company_df['sentiment'].shift(1)
    sector_df['sentiment'] = sector_df['sentiment'].shift(1)

    # Merge the DataFrames on the 'datetime' column using inner join to get common datetime values
    merged_df = pd.merge(company_df, sector_df, on='datetime', how='inner')
    merged_df = pd.merge(merged_df, stock_df, on='datetime', how='inner')

    # Calculate the mode of 'sentiment' for each row (datetime) in the merged DataFrame
    sentiment_mode = merged_df.groupby('datetime')[
        ['sentiment_x', 'sentiment_y', 'sentiment']].apply(lambda x: x.mode().iloc[0])

    # Rename the columns
    sentiment_mode.columns = ['sentiment_company',
                              'sentiment_sector', 'sentiment_stock']

    # Reset the index to get the 'datetime' back as a column
    sentiment_mode.reset_index(inplace=True)

    # Create a new column 'sentiment_mode' that contains the mode of all three sentiment columns
    sentiment_mode['sentiment_mode'] = sentiment_mode[[
        'sentiment_company', 'sentiment_sector', 'sentiment_stock']].mode(axis=1).iloc[:, 0]
    sentiment_mode.to_csv('data/result_df/result.csv')

    # get the datewise count for the sentiment, means no of positive, negative, and neutral sentiments.
    df = pd.read_csv('data/company/cohere_company_news_sentiment.csv')
    company_Sentiment_Count = companySentimentCount.aggregate_sentiments_by_day(
        df)
    company_Sentiment_Count.to_csv('data/company/company_Sentiment_Count.csv')

    return sentiment_mode

# import pandas as pd


# def modelResult():

#     # Load the three dataframes (company news, sector news, stock price)
#     company_df = pd.read_csv('data/company/company_dated_sentiment.csv')
#     sector_df = pd.read_csv('data/sector/sector_dated_sentiment.csv')
#     stock_df = pd.read_csv('data/company/company_stock_prices.csv')

#     def map_status_to_sentiment(status):
#         if status == "Increased":
#             return "positive"
#         elif status == "Decreased":
#             return "negative"
#         else:
#             return "neutral"

#     # Add the 'Sentiment' column using the custom function
#     stock_df['sentiment'] = stock_df['Status'].apply(map_status_to_sentiment)
#     stock_df.drop(['Open','High','Low','Close','Previous_Close'],axis=1,inplace=True)

#     # Convert 'datetime' columns to datetime data type
#     company_df['datetime'] = pd.to_datetime(company_df['datetime'])
#     sector_df['datetime'] = pd.to_datetime(sector_df['datetime'])
#     stock_df['datetime'] = pd.to_datetime(stock_df['datetime'])

#     # Shift the 'sentiment' column in company and sector dataframes one day backward
#     company_df['sentiment'] = company_df['sentiment'].shift(1)
#     sector_df['sentiment'] = sector_df['sentiment'].shift(1)

#     # Merge the stock price dataframe with the company and sector dataframes based on 'datetime'
#     merged_df = pd.merge(
#         stock_df, company_df[['datetime', 'sentiment']], on='datetime', how='left')
#     merged_df = pd.merge(merged_df, sector_df[[
#                          'datetime', 'sentiment']], on='datetime', how='left', suffixes=('_company', '_sector'))

#     # Drop any duplicate rows based on 'datetime' column
#     merged_df.drop_duplicates(subset='datetime', inplace=True)
#     # merged_df.to_csv()

#     # The merged_df will now contain the stock price data along with the previous day's sentiment for both company and sector news.
#     return merged_df
