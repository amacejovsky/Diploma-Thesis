
class WTO:
    """Worl Trade Organization keeps track of international trade variables and parameters."""
    def __init__(self):
        global no_countries, trade_sensitivity, normal_variance, trade_costs, trade_quotas
        # parameters
        self.no_countries = no_countries
        self.trade_sensitivity = trade_sensitivity   # sensitivity in exchange factors updating    ## gamma
        self.normal_variance = normal_variance       # std, actually, for exchange rate regime equation
        self.trade_costs = trade_costs                                        ## keep as np array  ## tau   ###not needed here
        self.trade_quotas = trade_quotas                                      ## quicker to have it as list ###not needed here
        
        
        # initial values
        self.export_details = [[0]*self.no_countries for i in range(self.no_countries)]
        self.import_details = [[0]*self.no_countries for i in range(self.no_countries)] 
##        self.exports = [0]*self.no_countries    # in volume                           ## keep as list
##        self.imports = [0]*self.no_countries    # in volume                           ## keep as list
        self.trade_balances = np.array([[0]*self.no_countries]*self.no_countries)
        self.total_product = 0             # volume of globally newly produced goods 
        self.exch_factors = np.array([1]*self.no_countries)
        self.exch_rates = np.outer(self.exch_factors, 1/self.exch_factors)            ## keep as np array
        self.natural_exch_rates = self.exch_rates.copy()
        
        self.bank_accounts = [0]*self.no_countries     # to keep track of interbank transactions
        
        
    def update(self):
        """Updates exchange rates."""
        global TSs, pegged_rates
        self.total_product = sum([country[0] for country in TSs["production"].data[-1]]) ## sums are in position 0
##        balances = self.trade_balances                                  ## already updated during time series collection
        balances = self.trade_balances.sum(axis = 1)     # total trade balances, detailed ones already updated
        tr_sen = self.trade_sensitivity
        
        if self.total_product != 0:
##            random_factors = np.random.normal(0, self.normal_variance, self.no_countries)      # should be this
            random_factors = np.random.uniform(0, self.normal_variance, self.no_countries)       # this is actually a mistake
            self.exch_factors = (1 + tr_sen/self.total_product * balances + random_factors)*self.exch_factors
        self.exch_rates = np.outer(self.exch_factors, 1/self.exch_factors) 
        self.natural_exch_rates = self.exch_rates.copy()
        for i, pegging in enumerate(pegged_rates):
            if pegging != -1:
                self.exch_rates[pegging][i] = 1               # country i is pegged to country "pegging"
                self.exch_rates[i] = self.exch_rates[pegging] # country i takes exchange rates of its pegging country
        
        self.export_details = [[0]*self.no_countries for i in range(self.no_countries)]     # refreshing
##        self.import_details = [[0]*self.no_countries for in in range(self.no_countries)]     # refreshing
##        self.exports = [0]*self.no_countries       # refreshing
##        self.imports = [0]*self.no_countries       # refreshing

