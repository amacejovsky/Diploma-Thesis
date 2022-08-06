class HSH:
    """Individual household."""
        
    def __init__(self, country, ID):
        # parameters       pouzit ako globalnu (setri pamat) alebo ako attribute (asi setri cas)?
        self.wage_resist = wage_resist[country]      # length of wage resistance in unemployment
        self.wage_flex = wage_flex[country]          # wage adjustment
        self.optimist = prop_to_save_O               # optimistic saving target
        self.pessimist = prop_to_save_P              # pessimistic saving target
        self.excess_cons = cons_of_excess_savings    # rate of cons. of excess savings
        self.neighborhood = h            # size of sentiment-influencing neighborhood
        self.spirits = p2                 # strength of animal spirits
        
        # individual hsh-specific attributes
        self.type = "h"    #  bank, firm, hsh
        self.country = country
        self.ID_no = int(ID) 
        self.ID = str(self.country) + "_" + "h" + "_" + str(ID)
        
        # initial values, variables
        self.rec_div = 0       # no of dividends this hsh receives                               ## not needed
        # wage taking
        self.res_wage = 0             # reservation wage                                  
        self.wage = 0                 # actual wage, determined on job market
        self.months_u = 0             # months since unemployed        
        self.employed = False         # currently employed?
        self.worked = True            # did work during the previous period? initially true due to its use in sentiment updating
        self.vol_unemployed = False   # if refused the best wage offer
        
        # sentiment
        self.sentiment = random.choice([True, False])   # optimistic if True
        self.old_sentiment = self.sentiment             # needed if influencing other households' sentiments
        self.saving_fraction =  self.optimist if self.sentiment else self.pessimist
        
        # consumption
        self.yearly_income = []     # list of incomes in past 12 months 
        self.income = 0             # current period income
        self.avg_income = 0         # 12 month average income                                 ## not needed as attribute
        self.savings_T = 0          # targeted savings
        self.cons_T = 0             # targeted consumption
        self.budget = 0             # actual budget as minimum between targeted consumption and cash on hand 
        self.cons = 0               # volume of current consumption
        self.cons_value = 0         # value of current consumption
        self.forced_savings = self.budget - self.cons_value # unused budget
        
        # archive of data - might be used for chosen households
        self.archive = ["archive of " + self.ID] 
        
    def create_account(self):
        """At initialization, creates a bank account."""
        self.account = Account(self.country, self)     # note - must be seperate from __init__ because we need to have bank 
                                            # for it, but we also need households for initialization of banks (ownership)
    
    
    def sentiment_update(self):
        """Updates households sentiment and saving behaviour. 
        As timing technicality, refreshes income, wage and voluntary unemployment."""
        self.income = 0                      # refreshing
        self.vol_unemployed = False          # refreshing
        if not self.employed:                # refreshing, here in order to avoid inconsistencies during bankruptcies
            self.wage = 0
        
        influenced = random.random()
##        # version of immidiate dependency on job status
##        if not self.worked:            # unemployed in the previous period?   then not depended on animal spirits
        # version from JAMEL code - dependednt on work from 2 periods before, everyone pessimistic in the second period
        if self.months_u > 0:            # unemployed in the second-to-last period?   then not depended on animal spirits
            self.sentiment = False     # false for pessimist
            self.saving_fraction = self.pessimist
        else:
            if influenced > self.spirits:    # does not rely on others
                self.sentiment = True        # true for optimist
                self.saving_fraction = self.optimist
            else:                            # relies on others
##                neighbors = np.random.choice(np.delete(HSHs[self.country],self.ID_no), self.neighborhood, replace = False)
                global HSHs
                neighbors = random.sample(HSHs[self.country], k=self.neighborhood) # can actually contain intself
                votes = sum([hsh.old_sentiment for hsh in neighbors])  # use old sentiment of neighbors
                if votes > self.neighborhood/2:
                    self.sentiment = True
                    self.saving_fraction = self.optimist
                else:
                    self.sentiment = False
                    self.saving_fraction = self.pessimist
        self.worked = False            # refreshing
        
        
    def res_wage_update(self):
        """Updates reservation wage, count of unemployed months. Part of labor market."""
        if self.employed:
            self.res_wage = self.wage
            self.months_u = 0
        else:
            if self.months_u == 0:
                self.months_u = random.random()          # so there is some small chance of adjustment, also used in sentiment updating
            else:
                self.months_u += 1
            alpha, beta = random.random(), random.random()
            if alpha*self.wage_resist < self.months_u:   # not resistant to lowering of reservation wage?
                self.res_wage *= 1 - beta*self.wage_flex
        
       
    def consumption_update(self):                                 
        """Updates targeted consumption. As timing technicality, updates old sentiment."""
        self.cons, self.cons_value = 0, 0               # refreshing
        self.yearly_income.append(self.income)            # updating
        self.yearly_income = self.yearly_income[-12:]
        self.avg_income = sum(self.yearly_income)/len(self.yearly_income)                    ## not needed as attribute
        
        self.savings_T = int(12*self.avg_income*self.saving_fraction)     # truncated
        
        savings = int(self.account.deposit - self.avg_income)             # truncated
        if savings < self.savings_T:
            self.cons_T = int((1 - self.saving_fraction)*self.avg_income) # truncated
        else:
            self.cons_T = int(self.avg_income + self.excess_cons*(savings - self.savings_T)) # truncated
        self.budget = min(self.account.deposit, self.cons_T)
        
        self.old_sentiment = self.sentiment
        
    def purchase(self, volume, value):
        """Purchase and consumption of goods. Part of goods market."""
        self.account.deposit -= value
        self.cons += volume
        self.cons_value += value
    
    
    def archiving(self, *attributes):
        """Adds to archive chosen attribute values."""
        global period
        if not period % 5:                       # ie. if period % 5 == 0
            self.archive.append(attributes)
        new_report = ["period: " + str(period)]
        for attr in attributes:
            sub_attributes = attr.split(".")
            obj = self
            for sub_attr in sub_attributes:      # consider eg. account.deposit
                obj = getattr(obj, sub_attr)
            new_report.append(obj)   
        self.archive.append(new_report)
    
