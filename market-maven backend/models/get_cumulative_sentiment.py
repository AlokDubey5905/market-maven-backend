import pandas as pd

def cumulative_sentiment(dataframe):
    # Assuming your DataFrame is named 'df' and it has 'date' and 'sentiment' columns
    df=dataframe
    # Convert 'date' column to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Group the DataFrame by 'date' and calculate the mode of 'sentiment'
    grouped_df = df.groupby('datetime')['sentiment'].apply(lambda x: x.mode().iloc[0]).reset_index()

    # dataframe for datewise sentiment
    # grouped_df.to_csv('data/datewise_sentiment.csv')
    # Print the combined DataFrame with the mode of sentiment for each date
    return grouped_df