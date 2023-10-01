import pandas as pd


def aggregate_sentiments_by_day(df):
    df['datetime'] = pd.to_datetime(df['datetime'])

    grouped_df = df.groupby(['datetime', 'sentiment']
                            ).size().reset_index(name='count')

    pivot_df = grouped_df.pivot(
        index='datetime', columns='sentiment', values='count').reset_index()

    pivot_df.fillna(0, inplace=True)
    pivot_df.columns = ['datetime', 'Negative', 'Neutral', 'Positive']

    pivot_df[['Negative', 'Neutral', 'Positive']] = pivot_df[[
        'Negative', 'Neutral', 'Positive']].astype(int)

    pivot_df['datetime'] = pivot_df['datetime'].dt.strftime('%Y-%m-%d')

    # Convert the 'date' column to datetime type in both dataframes
    result_df = pd.read_csv('data/result_df/result.csv')

    # Get the dates present in the result dataframe
    valid_dates = result_df['datetime']

    # Filter the original dataframe based on the valid dates
    filtered_df = pivot_df[pivot_df['datetime'].isin(valid_dates)]

    return filtered_df
