import yfinance as yf
import pandas as pd
pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999


def get_stock_data_yahoo(ticker):
    ticker_info = yf.Ticker(ticker).info
    return ticker_info



ticker = 'T'


for i in get_stock_data_yahoo(ticker):
    print(i)





