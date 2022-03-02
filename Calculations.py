class stock_valuation_calculations:

    # Calculates the intrinsic value of a stock
    def intrinsic_value_n_yr_calc_including_minimalreturnrate(self, Earnings_per_share, Growth_rate,
                                                              Minumim_rate_of_return,
                                                              Margin_of_safety, P_e_ratio, years=10):
        '''Calculates the value of a stock based on future earnings and growth, standard 10 year basis
        Prices will be rounded to 2 decimals when returned

        based on : https://www.youtube.com/watch?v=nX2DcXOrtuo&ab_channel=InvestingwithTom '''
        # given the current growth how much will the EPS be after n years
        growth_eps = Earnings_per_share * ((1 + (1 * Growth_rate)) ** (years - 1))
        # Value after n years ( how many times earning does the stock trade?)
        value = growth_eps * P_e_ratio
        # Value today
        Intrinsic_value_today = value / ((1 + Minumim_rate_of_return) ** (years - 1))
        # What to buy it for including the safety margin
        Safe_value = Intrinsic_value_today * Margin_of_safety

        return round(Intrinsic_value_today, 2), round(Safe_value, 2)

    def intrinsic_value_n_yr_calc_including_WACC(self, Earnings_per_share, Growth_rate, Discount_rate,
                                                 Margin_of_safety, P_e_ratio, years=10):
        '''Calculates the value of a stock based on future earnings and growth, standard 10 year basis
        Uses the WACC to discount the stock to the present value
        Prices will be rounded to 2 decimals when returned

        based on : https://www.youtube.com/watch?v=mScv_kl3zzc '''

        # given the current growth how much will the EPS be after n years
        growth_eps = Earnings_per_share * ((1 + (1 * Growth_rate)) ** (years - 1))
        # Value after n years ( how many times earning does the stock trade?)
        value = growth_eps * P_e_ratio
        # Value today including WACC
        Intrinsic_value_today = value / ((1 + Discount_rate) ** (years - 1))
        # What to buy it for including the discounted cash flow
        Safe_value = Intrinsic_value_today * Margin_of_safety

        return round(Intrinsic_value_today, 2), round(Safe_value, 2)

    def weighted_average_cost_of_capital(self, intrest_expense, short_term_debt, long_term_debt, income_tax_expence,
                                         income_before_tax, risk_free_rate, beta, market_return, market_cap):
        '''Calculates the Weighted average of capital

        The weighted average cost of capital (WACC) is the rate that a company is expected to pay on average to all its security holders to finance its assets'''
        weigth_of_debt = (short_term_debt + long_term_debt) / ((short_term_debt + long_term_debt) + market_cap)
        weight_of_equity = market_cap / ((short_term_debt + long_term_debt) + market_cap)

        WACC = weigth_of_debt * (
            self.calculate_costs_of_debt(intrest_expense, short_term_debt, long_term_debt, income_tax_expence,
                                         income_before_tax)) + weight_of_equity * (
                   self.calculate_costs_of_equity(risk_free_rate, beta, market_return))

        return WACC

    def calculate_costs_of_debt(self, intrest_expense, short_term_debt, long_term_debt, income_tax_expence,
                                income_before_tax):
        '''Calculates the costs of the short and long term debts ( part of the WACC )'''
        cost_of_debt = intrest_expense / (short_term_debt + long_term_debt)
        effective_tax_rate = income_tax_expence / income_before_tax
        cost_of_debt_t = cost_of_debt * (1 - effective_tax_rate)

        return cost_of_debt_t

    def calculate_costs_of_equity(self, risk_free_rate, beta, market_return):
        '''Calculates the costs of the equity ( part of the WACC )
        risk free rate is based on the 10 yr treasure return'''

        cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)
        return cost_of_equity


kaas = stock_valuation_calculations

Earnings_per_share = 11.89
Growth_rate = 0.12
Minumim_rate_of_return = 0.15
Margin_of_safety = 0.5
P_e_ratio = 24

print("Test 1 ( calculate intrinsic value ) : ")
print(kaas().intrinsic_value_n_yr_calc_including_minimalreturnrate(Earnings_per_share, Growth_rate,
                                                                   Minumim_rate_of_return,
                                                                   Margin_of_safety, P_e_ratio))

# print(kaas().intrinsic_value_10yr_calc_option_one(1.91, 0.2, 0.12, 0.5, 5.28))

# test data in duizenden, en percentages in decimale getallen
intrest_expense = 3576
short_term_debt = 0
long_term_debt = 91807
income_tax_expence = 10481
income_before_tax = 65737

risk_free_rate = 0.00951
beta = 1.29
market_return = 0.0851

market_cap = 1280000

print("\nWACC: ")
print(kaas().weighted_average_cost_of_capital(intrest_expense, short_term_debt, long_term_debt, income_tax_expence,
                                              income_before_tax, risk_free_rate, beta, market_return, market_cap))

print("\nWACC int value:")
print(kaas().intrinsic_value_n_yr_calc_including_WACC(Earnings_per_share, Growth_rate,
                                                      kaas().weighted_average_cost_of_capital(intrest_expense,
                                                                                              short_term_debt,
                                                                                              long_term_debt,
                                                                                              income_tax_expence,
                                                                                              income_before_tax,
                                                                                              risk_free_rate, beta,
                                                                                              market_return,
                                                                                              market_cap),
                                                      Margin_of_safety, P_e_ratio, years=10))
