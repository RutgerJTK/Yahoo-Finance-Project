import csv
import yfinance as yf
import pandas as pd

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999


def get_stock_data_yahoo(ticker):
    ticker_info = yf.Ticker(ticker).info
    return ticker_info


# for i in get_stock_data_yahoo(ticker):
#     print(i)


def safe_info_to_csv(ticker):
    '''
    This function takes a ticker and returns a csv file with the info of the ticker.
    '''
    try:
        with open('Stock_info/{}.csv'.format(ticker), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dir = get_stock_data_yahoo(ticker)
            for key, values in dir.items():
                spamwriter.writerow([key, ":", values])
        return csvfile
    except Exception as e:
        print(e)
        return None


ticker = 'kaasbrod'
safe_info_to_csv(ticker)
