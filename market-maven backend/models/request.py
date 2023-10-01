import models.companyNewsRequest as companyNewsRequest
import models.sectorNewsRequest as sectorNewsRequest
import models.result as result
import models.companyNews as companyNews


def request(name):

    try:
        # get the stock symbol for the company name
        symbol = companyNews.find_stock_symbol(name)
        # get the company news
        companyNewsRequest.company(symbol)

        # get the sector news
        sectorNewsRequest.sector(symbol)

        # get the result
        result_df = result.modelResult()
        prediction = result_df['sentiment_mode'].mode().iloc[0]
        return prediction

    except Exception as e:
        return "Positive"
