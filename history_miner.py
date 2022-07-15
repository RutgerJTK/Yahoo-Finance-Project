import time
import datetime
import pandas as pd
import glob
import csv
import yfinance as yf
import yahoofinancials as yfs
from yahoofinancials import YahooFinancials
from yahoofinancials import YahooFinanceETL
import re
import matplotlib.pyplot as plt

import lxml
from lxml import html
from lxml import etree
import requests


def criterion_1(ticker):
    """ Criterion 1: Dividend yield is undervalued on historical basis.
    """
    yfticker = yf.Ticker(ticker)
    yfsticker = YahooFinancials(ticker)
    file_name = 'dividend_info_vscode_{}.csv'.format(ticker)
    print(yfticker.info['exchange'])
    print("BETA:", yfticker.info['beta'])
    print(yfticker.info['industry'])
    files_present = glob.glob(file_name)
    if files_present:
        f = open(file_name, "w+")
        f.truncate()
    print("-" * 100)
    print("Criterion 1 for", ticker)
    print("Q1: Is the dividend undervalued on historical basis?")
    historical_dividend = yfticker.info['fiveYearAvgDividendYield']
    print(type(historical_dividend))
    print(historical_dividend)

    historical_dividend = float(historical_dividend)
    current_dividend = yfticker.info['dividendYield']
    if historical_dividend >= 0:
        print(historical_dividend)
    else:
        print("No Historic Dividend available")
        
    if historical_dividend < (current_dividend * 100):
        print("A1: Dividend yield currently undervalued, it adheres to rule 1. It is a buy.")
    else:
        print("A1: Dividend yield currently overvalued, it does not adhere to rule 1. It is not a buy.")


def criterion_2(ticker, url, header):
    print("-" * 100)
    ## Criterion 2 - part 1: Has the company raised dividends at an annual compound rate of at least 12% in the past 12 years.
    print("Criterion 2 for ", ticker)
    print("Does the stock offer a 12 year dividend CAGR of at least 10% ?")

    ## answer: maybe xpaths? --> used medium article:
    "https://medium.com/c%C3%B3digo-ecuador/python-web-scraping-yahoo-finance-stock-dividend-history-d9084c85c805"
    dividends = scrape_page(url, header)
    # added_divs_list = order_dividends(dividends)  # Done!
    # calculate_dgy(added_divs_list)
    # calculate_cagr(years_list, dividends2)
    return dividends


def criterion_3(ticker, url, header):
    print("crit 3 for ", ticker)
    print("Does the stock offer a decent payout ratio? This should be below 50% :")
    yfticker = yf.Ticker(ticker)
    payout = ((float(yfticker.info['payoutRatio'])) * 100)
    if payout < 50:
        print("Payout ratio: ", payout, "%")
        print(" ~ ~ ~ Ratio is below 50%, it adheres to the criteria")
    elif payout > 49.99:
        print("Payout ratio: ", payout, "%")
        print(" ~ ~ ~ Ratio is above 50%, it is not a buy")


def scrape_page(url, header):   # dividends page
    page = requests.get(url, headers=header, timeout=5)
    element_html = html.fromstring(page.content)
    table = element_html.xpath("//table[@data-test = 'historical-prices']")
    table_tree = lxml.etree.tostring(table[0], method='xml')
    dividends_table = pd.read_html(table_tree)
    dividends = dividends_table[0]
    index = len(dividends)
    dividends = dividends.drop(index - 1)
    dividends = dividends.set_index('Date')
    dividends = dividends['Dividends']
    dividends = dividends.str.replace(r'\Dividend', '')
    dividends = dividends.astype(float)
    return dividends


def order_dividends(dividends):
    divs_ordered = []
    for i in dividends.index:
        i = (i[7:11])
        if i not in divs_ordered:
            divs_ordered.append(i)

    # sum all dividends for each year:
    dividends = str(dividends)
    dividends = dividends.split("\n")
    div2 = 0
    counter = 0
    added_divs_list = []
    for line in dividends:
        if not line.startswith("Date" and "Name") and "0" in line:
            counter += 1
            div = float(line[15:(len(line))])
            div2 += div
            div2 = round(div2, 4)
            if counter == 4:
                added_divs_list.append(div2)
                div2 = 0
                counter = 0
    added_divs_list.append(div2)
    print("List of cummulative dividends the past years: ", added_divs_list)
    return added_divs_list


def calculate_dgy(added_divs_list):
    print("Years of growth and CAGR (WIP)")
    counter = 0
    cur = 0
    prev = 0
    highest = 0
    old_highest = 0
    new_highest = 0
    for counter in range(len(added_divs_list)):
        cur = added_divs_list[counter]
        print(cur)
        if counter > 0:
            prev = added_divs_list[counter - 1]
        if prev > cur:
            highest += 1
            if highest > old_highest:
                old_highest = highest
        else:
            new_highest = highest
            highest = 0
        counter += 1
    if highest > new_highest:
        print("The recent dividend streak is the highest.")
        print("Years of consecutive dividend growth: ", old_highest)
    else:
        print("The highest dividend raise streak was before the current one.")
        print("Years of consecutive dividend growth: ", new_highest)


def calculate_cagr(years_list, dividends2):
    """ CAGR = ((l/f)^(1/n)) - 1
    CAGR for dividends year over year.
    In which:
    F = F here means the First value in your series of values.
    L = L here means the Last value in your series of values.
    N = N is the number of years between your First and Last value in your series of values.
    """
    print(dividends2)

    l = int(years_list[1])
    f = int(years_list[(len(years_list))-1])
    n = ((l - f) - 1)
    n2 = 12     # set this to be 12 as this is the desired amount of years for annual growth. Should be an input later.
    n3 = 5      # Personalised preferable amount of years to showcase CAGR.
    if len(dividends2) >= 12:
        cagr_n2 = ((((dividends2[1] / dividends2[(n2 - 1)]) ** (1/n2)) - 1) * 100)
        print("Compound annual growthrate spanning ", n2, "years: ", round(cagr_n2, 3), "%")
    if len(dividends2) >= 5:
        cagr_n3 = ((((dividends2[1] / dividends2[(n3 - 1)]) ** (1/n3)) - 1) * 100)
        print("Compound annual growthrate spanning ", n3, "years: ", round(cagr_n3, 3), "%")


def dataroma_miner():
    print("mining")
    roma_url = "https://www.dataroma.com/m/managers.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    page = requests.get(roma_url, headers=headers)
    element_html = html.fromstring(page.content)
    table = element_html.xpath("//table")
    table_tree = lxml.etree.tostring(table[0], method='xml')
    tabbie = pd.read_html(table_tree)
    tframe = tabbie[0]
    tframe['Top 10 holdings (left to right)'].value_counts()
    shitlist = []

    for i in range(len(tframe)):
        for j in range(len(tframe.iloc[i][3:])):
            try:
                ticker = str(tframe.iloc[i][3:][j][0:5])
                ticker = ticker.split(" ")
                shitlist.append(ticker[0])
            except TypeError:
                continue
    dtf = pd.DataFrame(shitlist)
    print(dtf.value_counts().sort_values(ascending=False).head(40))
    return shitlist


def sid(tickers_list):
    print("visualising")
    t_dict = {}
    for i in tickers_list:
        if tickers_list.count(i) >= 4:
            t_dict[i] = tickers_list.count(i)

    tickers = list(t_dict.keys())
    frequencies = list(t_dict.values())
    plt.bar(range(len(t_dict)), frequencies, tick_label=tickers, width=0.5)
    plt.xticks(rotation=90, ha='right')
    plt.title('Super investors most held stonks')
    plt.show()


def main():
    """Setting some simple global variables"""
    ticker = 'ADM'
    # Note: url period2 will age over time, thus not displaying the most recent dividend.
    url_divs = "https://sg.finance.yahoo.com/quote/{}/history?period1=1&period2=1728985600&interval=capitalGain%7Cdiv%7Csplit&filter=div&frequency=1d&includeAdjustedClose=true".format(
        ticker)
    url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker, ticker)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    """Actual criteria functions"""
    print("-" * 100)
    print("Start of assessment. Chosen ticker: ", ticker)
    print("-" * 100)
    criterion_1(ticker)
    print("+"*100)
    criterion_2(ticker, url_divs, headers)
    print("-"*100)
    criterion_3(ticker, url_stats, headers)
    print("-"*100)


if __name__ == "__main__":
    print("Main")
    shitlist = dataroma_miner() # mine super investor data
    sid(shitlist)    # super investor data - visualiser
