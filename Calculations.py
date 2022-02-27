class stock_valuation_calculations:

    # Calculates the intrinsic value of a stock
    def intrinsic_value_10yr_calc_option_one(self, Earnings_per_share, Growth_rate, Minumim_rate_of_return,
                                             Margin_of_safety, P_e_ratio, years=10):
        '''Calculates the value of a stock based on future earnings and growth, standard 10 year basis
        Prices will be rounded to 2 decimals when returned'''
        # given the current growth how much will the EPS be after 10 years
        ten_year_growth_eps = Earnings_per_share * ((1 + (1 * Growth_rate)) ** (years-1))
        # Value after 10 years ( how many times earning does the stock trade?)
        value_year_ten = ten_year_growth_eps * P_e_ratio
        # Value today
        Intrinsic_value_today = value_year_ten / ((1 + Minumim_rate_of_return) ** (years-1))
        # What to buy it for including the safety margin
        Safe_value = Intrinsic_value_today*Margin_of_safety

        return round(Intrinsic_value_today,2),round(Safe_value,2)


kaas = stock_valuation_calculations
print(kaas().intrinsic_value_10yr_calc_option_one(11.89,0.12,0.15,0.5,15.5))