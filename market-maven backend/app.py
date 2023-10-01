from flask import Flask, request, jsonify
from flask_cors import CORS
import finnhub
import pandas as pd
from models.stockData import stockdata
from models.companyNews import find_stock_symbol,companyNews
import models.request as rq
import models.sectorSpecific as sf
import models.get_cumulative_sentiment as gcs
import models.sectorWise as sw
import models.companyNewsRequest as cnr
import os


allowed_origins = ['http://localhost:3000', 'https://stockpredictor-frontend-urtjok3rza-wl.a.run.app'] 
app = Flask(__name__)
CORS(app, origins=allowed_origins)

reader=pd.read_csv('data/stocks_data.csv')


trending_stockname= ['Apple', 'Netflix', 'eBay', 'Walmart', 'FedEx', 'Goldman Sachs', 'IBM', 'JPMorgan Chase', 'Microsoft', 'Amazon']


#API: FinnhubMarketNews
# Function for first page to get trending news 
@app.route('/dashboard/trending_news', methods=['GET'])
def get_trending_news():
    news_data = finnhub.Client(api_key= os.environ['FINNHUB_APIKEY'])
    return news_data.general_news('general', min_id=0)[:9]


#API: Yfinance
#function to give stock data
@app.route('/dashboard/stockcard_data', methods= ['GET'])
def stockcard_data():

    all_stock_data = {}  # Create an empty dictionary to hold data for all companies

    for company_name in trending_stockname:
        stock_symbol = find_stock_symbol(company_name)
        df = stockdata(company_name, stock_symbol)
        df=df.assign(symbol=stock_symbol)
        df=df.round(3)
        json_data = df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
        all_stock_data[company_name] = json_data  # Add data for the current company to the dictionary

    return jsonify(all_stock_data)


#Search Function to do partial search implementation
@app.route('/dashboard/partial_search', methods= ['GET'])
def partial_search():
    input_data = request.args.get('search_term', '')
    if input_data == '' or input_data == None:
        return jsonify({"error": "Input data is empty."}), 404
    
    input_data = input_data.lower()
    results = {}
    ind = 0
    for index,row in reader.iterrows():
        symbol = row['Symbol']
        company_name = row['Name']

        if symbol.lower().startswith(input_data) or company_name.lower().startswith(input_data):
           url = f"https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/{symbol.upper()}.svg"
           results[ind] = {'Symbol': symbol, 'CompanyName': company_name, 'logo': url}
           ind+=1

    return jsonify(results)


#API: FinnhubMarketNews
#Function for News Page to get trending news
@app.route('/news/trending_news', methods= ['GET'])
def all_trending_news():
    news_data = finnhub.Client(api_key= os.environ['FINNHUB_APIKEY'])
    return news_data.general_news('general', min_id=0)[:50]


#Function to get stock price data for particular stock for 8 days.
@app.route('/predict_stock/stock_data/<stock_name>', methods= ['GET'])
def stock_data(stock_name):
    stock_symbol = find_stock_symbol(stock_name)
    df = stockdata(stock_name, stock_symbol)
    df=df.assign(symbol=stock_symbol)
    df=df.round(3)
    json_data = df.to_json(orient='records')
    return json_data


#Function to get data for doughnout chart
@app.route('/predict_stock/cummulative_sentiments/<stock_name>', methods=['GET'])
def cumm_sentiment(stock_name):
    prediction =predict_stock(stock_name=stock_name)
    res=pd.read_csv('data/result_df/result.csv')
    sentiment_counts = {
    'Positive': 0,
    'Negative': 0,
    'Neutral': 0
    }
    for index, row in res.iterrows():
        sentiment = row['sentiment_mode']
        sentiment_counts[sentiment] += 1

    json_data = {
    'Positive': sentiment_counts['Positive'],
    'Negative': sentiment_counts['Negative'],
    'Neutral': sentiment_counts['Neutral'],
    'prediction': prediction
    }    
    return json_data


#Function to get cummulative sentiment result for 7 days
@app.route('/predict_stock/cummulative_result/<stock_name>', methods=['GET'])
def predict_stock(stock_name):
    prediction=rq.request(stock_name)
    res = ''
    if prediction == 'Negative':
        res = 'Based on our analysis, the stock sentiment currently indicates a potential decrease in price.'
    elif prediction == 'Positive':
        res = 'Based on our analysis, the stock sentiment currently indicates a potential increase in price'
    elif prediction == 'Neutral':
        res = 'Based on our analysis, the stock sentiment at the moment there is no clear indication of a significant price increase or decrease in the immediate future'

    return res


#Function to get company fundamentals data.
@app.route('/predict_stock/stock_details/<stock_name>', methods =['GET'])
def stock_details(stock_name):
    client = finnhub.Client(api_key= os.environ['FINNHUB_APIKEY'])
    stock_symbol = find_stock_symbol(stock_name)
    return client.company_profile2(symbol=stock_symbol)


#Function to give latest news related to Particular Stockname
@app.route('/predict_stock/stock_news/<stock_name>', methods=['GET'])
def stock_news(stock_name):
    res= cnr.compn_news(stock_name)
    json_data = res.to_json(orient='records')
    
    return json_data

@app.route('/predict_stock/sentiment_count/', methods=['GET'])
def sentiment_count():
    res =pd.read_csv('data/company/company_Sentiment_Count.csv')
    json_data = res.to_json(orient='records')

    return json_data


@app.route('/sector/sector_news/<sector_name>', methods=['GET'])
def sector_news(sector_name):
    df = sf.sector_news_generation(sector_name=sector_name)
    jsondata = df.to_json(orient='records')
    return jsondata


@app.route('/sector/cummulative_result/<sector_name>', methods=['GET'])
def sector_cummulative(sector_name):
    df = sf.sector_news_generation(sector_name=sector_name)
    cummsn = gcs.cumulative_sentiment(df)
    sentiment_counts = {
    'Positive': 0,
    'Negative': 0,
    'Neutral': 0
    }
    for index, row in cummsn.iterrows():
        sentiment = row['sentiment']
        sentiment_counts[sentiment] += 1

    json_data = {
    'Positive': sentiment_counts['Positive'],
    'Negative': sentiment_counts['Negative'],
    'Neutral': sentiment_counts['Neutral'],
    }    

    return json_data


@app.route('/sector/top_gainer/<sector_name>', methods=['GET'])
def sector_top_gainer(sector_name):
    top_gainer = sw.topGainerTopLooser(sector=sector_name)
    res = top_gainer.to_json(orient='records')
    return res



#stock_name = request.args.get('stock_name', '')
    # if stock_name == ''or stock_name == None:
    #     return jsonify({"error": "Stock name not found or wrong input"}), 404
    # stock_symbol = find_stock_symbol(company_name=stock_name)
    # if stock_symbol is None:
    #     return jsonify({"error": "Stock symbol not found for the given company name."}), 404