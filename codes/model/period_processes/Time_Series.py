
class TS:
    """Time series for a chosen variable."""
    def __init__(self, agent, variable, summary_stats, customized_list_f = None):
        self.name = agent + ": " + variable
        self.data = []                                            ####[[agent, variable, summary_stats]] + change indexing in methods
        self.agent = agent
        self.variable = variable
        self.summary_stats = summary_stats
        self.customized_list_f = customized_list_f     # function which returns list of chosen agents
        
        
    def update(self):
        """Collects current cross-sectional data, appends it to the time series."""
        self.data.append(collect_data(self.agent, self.variable, self.summary_stats, self.customized_list_f))
        
    
    def sums(self):
        """Returns list of country-specific time series of sums from data."""
        no_countries = len(self.data[0])
        return [[period_data[i][0] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    
    def means(self):
        """Returns list of country-specific time series of means from data."""
        no_countries = len(self.data[0])
        return [[period_data[i][1] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    
    def mins(self):
        """Returns list of country-specific time series of minima from data."""
        no_countries = len(self.data[0])
        if self.summary_stats:
            return [[period_data[i][2] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    
    def medians(self):
        """Returns list of country-specific time series of medians from data."""
        no_countries = len(self.data[0])
        if self.summary_stats:
            return [[period_data[i][3] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    
    def maxs(self):
        """Returns list of country-specific time series of maxima from data."""
        no_countries = len(self.data[0])
        if self.summary_stats:
            return [[period_data[i][4] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    
    def stds(self):
        """Returns list of country-specific time series of standard deviations from data."""
        no_countries = len(self.data[0])
        if self.summary_stats:
            return [[period_data[i][5] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]


# In[19]:


# customized_list_f for TS objects and collect_data(), functions specifying lists of agents from which data is to be collected
def working_hsh():
    """Function for choosing only employed households; to be used for collection of data."""
    global HSHs
    return [[hsh for hsh in country if hsh.worked] for country in HSHs]

def unemployed_hsh():
    """Selects households which are unemployed."""
    global HSHs
    return [[hsh for hsh in country if not hsh.employed] for country in HSHs]

def exporting_firms_fun():                              ### added at the end for chosen
    """Selects firms that have exported goods during the period."""
    global FIRMs
    return [[f for f in country if f.exporting] for country in FIRMs]


# Special_TS class

# In[20]:


class Special_TS:
    """Some additional time series."""
    def __init__(self, variable):
        self.data = []
        self.variable = variable
        self.name = variable
        
    def update(self):
        if self.variable == "no_of_firms":     # number of active firms in the current period
            global FIRMs
            self.data.append([len(country) for country in FIRMs]) 
            
        elif self.variable == "trade_fees":
            global trans_firms
            self.data.append([tr.old_profits for tr in trans_firms])    
        
        elif self.variable in ["trade_balances", "exch_rates", "natural_exch_rates", 
                             "export_details", "import_details", "bank_accounts"]:
            global wto
            if self.variable == "trade_balances":              # calculate and add to TS     
                exp = np.array(wto.export_details)
                wto.trade_balances = exp - exp.T                                    ## keep attribute as np array
                self.data.append(list(wto.trade_balances))                          ## make a copy
            elif self.variable == "import_details":            # calculate and add to TS     
                wto.import_details = np.array(wto.export_details).T                        ## no need to keep as attribute
                self.data.append(list(wto.import_details))                          ## make a copy
            elif self.variable == "export_details":
                self.data.append(np.array(wto.export_details)) # make a FULL copy 
            else:
                self.data.append(getattr(wto, self.variable).copy())  ## lists or arrays are referenced by default, copy needed
            
    
    def sums(self, country = 0):
        """Returns list of country-specific time series from data."""
        no_countries = len(self.data[0])
        if self.variable in ["trade_balances", "exch_rates", "natural_exch_rates", 
                             "export_details", "import_details"]:          # matrices   
            return [[period_data[country][i] for period_data in self.data] for i in range(no_countries)]
        
        return [[period_data[i] for period_data in self.data] for i in range(no_countries)]  # [country1_ts, country2_ts,...]
    

