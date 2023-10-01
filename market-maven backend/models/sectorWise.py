import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import models.request as request


def topGainerTopLooser(sector):

    def get_previous_trading_day(date):
        previous_day = date - timedelta(days=1)

        # Check if the previous day is a weekend (Saturday or Sunday)
        while previous_day.weekday() >= 5:
            previous_day -= timedelta(days=1)

        return previous_day

    def get_previous_day_stock_data(stock_symbol):
        # Get the current date
        current_date = datetime.now().date()

        start_date = get_previous_trading_day(current_date)
        data = yf.download(stock_symbol, start=start_date, end=current_date)
        return data

    def get_percentage_change(open_price, close_price):
        return ((close_price - open_price) / open_price) * 100

    def task(stock_symbols):
        # Create lists to store the results
        stock_symbol_list = []
        company_name_list = []
        percentage_change_list = []

        # Iterate over each stock symbol
        for stock_symbol in stock_symbols:
            data = get_previous_day_stock_data(stock_symbol)
            if not data.empty and 'Open' in data.columns and 'Close' in data.columns:
                open_price = data['Open'][0]
                close_price = data['Close'][0]
                percentage_change = get_percentage_change(
                    open_price, close_price)

                # Append the result to the lists
                stock_symbol_list.append(stock_symbol)
                percentage_change_list.append(percentage_change)

                company_df=pd.read_csv('data/stocks_data.csv')
                # Get the company name from the company DataFrame based on the stock symbol
                matching_row = company_df[company_df['Symbol'] == stock_symbol]
                if not matching_row.empty:
                    company_name = matching_row['Name'].iloc[0]
                    company_name_list.append(company_name)
                else:
                    print(f"No data found for {stock_symbol}")
                    company_name_list.append('N/A')

        # Create the DataFrame from the lists
        result_df = pd.DataFrame({
            'Stock Symbol': stock_symbol_list,
            'Company Name': company_name_list,
            'Percentage Change': percentage_change_list
        })

        return result_df

    def get_stock_symbols_by_sector(sector_name):
        company = pd.read_csv('data/stocks_data.csv')
        # Filter the DataFrame to include only rows with the specified sector
        sector_df = company[company['Sector'] == sector_name]

        # Extract the stock symbols and company names from the filtered DataFrame
        stock_symbols = sector_df['Symbol'].tolist()
        company_names = sector_df['Name'].tolist()

        return stock_symbols, company_names

    symbolList, companyNameList = get_stock_symbols_by_sector(sector)
    df = task(symbolList)
    df = df.sort_values(by='Percentage Change', ascending=False)
    topGainer = df[:5]
    topGainer.to_csv('data/company/topGainerSectorCompanies.csv')
    topGainer['sentiment']=topGainer['Company Name'].apply(request.request)
    topGainer.to_csv('data/company/topGainerSectorCompanies.csv')
    return topGainer
