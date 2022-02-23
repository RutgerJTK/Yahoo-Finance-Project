class stock_analyse:

    def __init__(self, ticker_symbol):
        #todo insert scraper to get stock data

        #todo Calculate marketcap ( shares outstanding * share price )
        self.marketcap = int
        self. shares_outstanding = int

        #todo shareprice, maybe an last price or actual price
        self.shareprice_last_closing_day = float
        self.shareprice_current = float
        self.shareprice_avg_50_day = float
        self.shareprice_avg_100_day = float
        self.shareprice_avg_200_day = float

        #todo (5yr) profit calculation
        self.year_profit = int
        self.five_year_profit = int

        #todo net income calculation
        self.net_income_annual = int
        self.net_income_five_yr = int

        #todo dividents
        self.dividents_annual_amount = float
        self.dividents_annual_percentage = float

        #todo debt and equity
        self.debt = int
        self.equity = int
        self.assets = int
        self.longterm_liabitities = int

        #todo Revenue
        self.revenue = int
        self.revenue_five_yr = int

        #todo Cashflow
        self.free_cashflow = int
        self.operating_cashflow = int








        pass

    def get_balance_sheet(self):
        pass

    def get_income_statement(self):
        pass

    def get_cashflow_statement(self):
        pass

    def calculate_5yr_pe_ratio(self, market_cap, five_yr_profit):
        # market cap = shares outstanding * stock price
        # market cap / sum of 5yr profit

        pe = market_cap/five_yr_profit

        return pe


    def calculate_5yr_roic(self,net_income,dividends,debt,equity):
        # *calculation: ROIC = (net income – dividends) / (debt + equity)*

        roic = ((net income – dividends) / (debt + equity))

        return roic

    def calculate_ltl_vs_5yr_fcf(self, liabilities, free_cash_flow ):
        # *calculation: Long term liabilities devided by free cash flow*

        pass

    def calculate_5yr_price_to_cashflow(self,market_cap,free_cash_flow):
        # Price to FCF=Market Capitalization / Free Cash Flow
        ltl_vs_cash = market_cap/free_cash_flow

        return ltl_vs_cash

    def get_5yr_revenue_growth(self):
        # see if rev increased in 5 years
        pass

    def get_5yr_shares_outstanding(self):
        # see if shares decreased in last 5 yrs
        pass

    def get_5yr_cashflow_growth(self):
        # see if the free cashflow increased in last 5 yrs
        pass

    #todo more items:
    # #Price/sales ratio
    # #Price/book ratio
    # #Divident stuff (and if the company can afford it)
    # #Market cap and sector comparison











