import models.sector_news as sn
import models.sentiment_analysis as sa
import pandas as pd

def sector_news_generation(sector_name):
    df=sn.specificSectorNews(sector=sector_name)
    df['sentiment']=df['headline'].apply(sa.vaderPredict)
    df.to_csv('data/sector/vader_sector_news_sentiment.csv')
    df=pd.read_csv('data/sector/vader_sector_news_sentiment.csv')
    return df

sectors = ['Health Care', 'Industrials', 'Information Technology', 'Consumer Staples', 'Consumer Discretionary', 'Utilities', 'Financials', 'Materials', 'Real Estate', 'Communication Services', 'Energy']
