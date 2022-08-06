
class Firm:
    """Individual firm."""
    
    def __init__(self, country, ID):
        global HSHs                                                                          ## write in parameters ??
        # parameters              pouzit ako globalnu (setri pamat) alebo ako attribute (asi setri cas)??
        self.K = K                        # no of machines
        self.productivity = productivity  # machine productivity 
        self.max_prod = productivity*K    # max production in a period
        
        self.price_flex = price_flex         # adjustment parameter for price of goods
        self.util_flex = util_flex           # flexibility (adjustment) of utilization rate
        self.wage_flex_up = wage_flex_up     # upward wage flexibility
        self.wage_flex_down = wage_flex_down # downward wage flexibility
        
        self.vacancy_T = targeted_vacancies                     # targeted vacancies                            
        
        self.sell_ratio = mu_F                # goods to be sold                                 ## not used in the current version
        self.optimist = capital_normal_ratio  # optimisstic targeted net wealth
        self.pessimist = capital_high_ratio   # pessimistic targeted net wealth
        self.sales_T = sales_normal_ratio     # targeted sales - to use for sentiment
        self.inv_T = in_T                     # targeted inventories
        
        self.neighborhood = h             # size of sentiment-influencing neighborhood
        self.spirits = p                  # strength of animal spirits
        
        # individual firm-specific attributes
        self.type = "f"    #  bank, firm, hsh
        self.country = country
        self.ID_no = int(ID) 
        self.ID = str(self.country) + "_" + "f" + "_" + str(ID)
        self.owner = random.choice(HSHs[country])    # randomly chooses owner (possibility of repetition for diff. firms)
        self.owner.rec_div += 1
        self.bankrupt = False         # nonactive for t_f periods if goes bankrupt, then recreation as a new firm (with new owner)
        self.machines = [Machine(self, self.ID+"_m"+str(no)) for no in range(self.K)]    # K machines for a firm
        
        # variables and initial values
        
        # inventories
        self.inv = 0                # volume of finished goods
        self.inv_value = 0          # equals cost of its production, ie wage of corresponding workers
        self.unit_cost = 0          # average cost
        self.new_prod = 0           # newly finished goods during a current period
        self.new_prod_value = 0
        
        # labor demand
        self.job_offering = True                      # if looking for new employees
        self.util_rate_T = random.randrange(50,100)   #targeted utilization rate of machinery for a firm; drawn for each firm at creation
        self.labor_d = int(self.util_rate_T*self.K/100)  # initial demand for labour 
        self.hiring = self.labor_d                    # difference between employed and demanded labor
        self.new_hirings = 0                          # newly employed workers in the current period
        self.labor = 0                                # actual labor employed in the current period
        self.contracts = []                   # list of job contracts held
        self.contracts_to_cancel = []         # list of contracts to terminate 
        self.labor_d_series = []              # list of demanded labor (in the last 4 periods)
        
        # goods supply
        self.goods_offering = False
        self.supply = 0           # goods supply volume for a period
        self.curr_supply = 0      # supply volume but updated after each sale
        self.price = 0            # sale price of goods
        self.prices = []          # sale prices in different countries
        self.high_price = 0       # used in price updates
        self.low_price = 0        # used in price updates
        self.price_rigidity = 0   # number of periods until next price adjustment is allowed   
        self.sales = 0              # volume of goods sold in the current period
        self.cost_of_sales = 0      # production value of sold goods
        self.sales_value = 0        # sale value of sold goods 
        self.sales_series = []      # past 12-month sales volumes        
        
        # wage offer
        self.skip_in_first = True   # so we skip wage and sentiment determination in the 1st period of firm's existence
        self.vacancy_rate = 0            
        self.vacancies = 0           # number of vacancies in a period
        self.wage = 3000             # wage offer,   initial==3000
        self.vacancy_series = []     # list of number of vacancies (in the last 4 periods)
        
        # account
        self.account = Account(self.country, self) 
        
        # sentiment
        self.sentiment = True                 # determined by opinion model, initially optimistic  
        self.old_sentiment = self.sentiment   # needed when influencing other firms' sentiments
        
        # dividends
        self.assets = 0         # = deposit + value_of_inv + value_of_unfinished_goods
        self.capital = 0        # = assets - debts
        self.wealth_ratio = self.optimist if self.sentiment else self.pessimist
        self.capital_T = 0     # target net wealth, determined by sentiment and assets
        self.dividend = 0      
        
        # archive, might be filled for chosen firms   
        self.archive = ["archive of " + self.ID]  
        
        #self.exporting = False                ### added at the end for chosen
        
        
    def new_period(self):                                                   ## old sentiment could be updated beforehand
        """Updates attributes for new period."""                            ## and contracts cleared during sentiment_update
        self.old_sentiment = self.sentiment
        #self.exporting = False                       ### added at the end for chosen
        # cancelation of old contracts
        for contr in self.contracts_to_cancel:
            contr.cancel()
            self.contracts.remove(contr)
        self.contracts_to_cancel = []
        self.labor = len(self.contracts)
        
    
    def sentiment_update(self):
        """Updates the sentiment and targeted wealth ratio of the firm."""
##        if not self.skip_in_first:
        influenced = random.random()
        if influenced > self.spirits:      # does not rely on others
            if self.skip_in_first:         # in the first period, when looking at its sales it is pessimistic for sure
                self.sentiment = False
            else:
                avg_past_sales = sum(self.sales_series)/len(self.sales_series) # past 12-month average sales                           
                if avg_past_sales/self.max_prod > self.sales_T:
                    self.sentiment = True      # true for optimist
                else:
                    self.sentiment = False
            
        else:           # relies on others
            global FIRMs
            neighbors = random.sample(FIRMs[self.country], k = self.neighborhood) # might choose itself
            votes = sum([firm.old_sentiment for firm in neighbors])
            if votes > self.neighborhood/2:
                self.sentiment = True
            else:
                self.sentiment = False
        self.wealth_ratio = self.optimist if self.sentiment else self.pessimist
        
        
    def pay_dividend(self):
        """Updates and pays dividend to its owner."""
        global bank_account, wto
        unfin_inv_value = sum([mach.value for mach in self.machines])     # production costs of unfinished goods
        assets = self.account.deposit + self.inv_value + unfin_inv_value
        
        if global_bank:             # updates loans' value with respect to current exchange rates
            self.account.domestic_loans = int(self.account.loans * wto.exch_rates[0][self.country])  # EUR/PLN
            capital = assets - self.account.domestic_loans
        else:
            capital = assets - self.account.loans
        capital_T = int(self.wealth_ratio*assets)           # truncated
        
        self.dividend = min(self.account.deposit, capital - capital_T) if capital > capital_T else 0
        if self.dividend > 0:                               # pays out dividend
            self.owner.account.deposit += self.dividend 
            self.owner.income += self.dividend
            self.account.deposit -= self.dividend 
        self.capital = capital                                        ## as attribute ???
        self.capital_T = capital_T                                    ## as attribute ???
        self.assets = assets                                          ## as attribute ???
        #self.owner.capital += self.capital                           ## do we need this? to add capital as HSH attribute ???
    
        
    def lay_off(self, number, delete_wage = False):
        """Lays-off workers. Part of new period-updates and production plan."""
        for i in range(number):
            contr = self.contracts.pop()       # returns and removes the most recent contract from the list
            contr.cancel(delete_wage)
        self.labor = len(self.contracts)
    
    
    def production_plan(self):
        """Updates labor demand, sale price, offered wage, makes new loan if needed."""
        # labor to hire
        alpha, beta = random.random(), random.random()
        alpha_beta = alpha*beta
               
        inv_diff = (self.inv_T - self.inv)/self.inv_T   # proportional difference between targeted and actual inventories
        if alpha_beta < inv_diff:          # lack of inventories, increase production 
            delta_labor_d = alpha*self.util_flex 
        elif alpha_beta < -inv_diff:       # the opposite
            delta_labor_d = -alpha*self.util_flex 
        else: 
            delta_labor_d = 0              # no change
        self.util_rate_T += delta_labor_d  # utilization rate of machinery, in % points
        self.util_rate_T = max(min(self.util_rate_T, 100), 0)              
        
        self.labor_d = int(self.K*self.util_rate_T/100)       # update labor demand, truncating
        
        hiring = self.labor_d - self.labor     # missing/excessive workers
        if hiring > 0:     
            self.job_offering = True
        else:
            self.job_offering = False
            self.lay_off(-hiring, True)              # lays off excessive workforce
        
        
        # price of goods
        self.price_rigidity -= 1         # passing of a period
        if self.supply == 0:             # use overall supply from the previous period
            sales_ratio = 0
        else:
            sales_ratio = self.sales/self.supply     # use overall sales and supply from the previous period
        
        if self.price == 0:
            self.price = self.unit_cost            # is zero before first finished goods;    no new price rigidity (?) 
            self.high_price = (1 + self.price_flex)*self.price
            self.low_price = (1 - self.price_flex)*self.price
        
        elif self.price_rigidity <= 0:
            # SmartPricingManager version, does not work as described in the paper           
            if sales_ratio == 1:                
                self.low_price = self.price
                if inv_diff > 0:                # fewer than targeted inventories, raise the price
                    self.price = random.uniform(self.low_price, self.high_price)
                    self.price_rigidity = random.randrange(1,4)
                self.high_price *= 1 + self.price_flex      # update only after eventual change in price
            else:
                self.high_price = self.price
                if inv_diff < 0:                # too many inventories, decrease the price
                    self.price = random.uniform(self.low_price, self.high_price)
                    self.price_rigidity = random.randrange(1,4)
                self.low_price *= 1 - self.price_flex       # update only after eventual change in price
            
##            # BasicPricingManager version, equations as described in the paper
##            if alpha_beta < inv_diff:                 # but not depended on unslod supply as mentioned in the paper  (?)
##                self.price *= 1 + alpha*self.price_flex        # update price
##                self.price_rigidity = random.randrange(1,4)  # rigidity starts anew
##            elif alpha_beta < -inv_diff:                
##                self.price *= 1 - alpha*self.price_flex       # update price
##                self.price = max(1, self.price)
##                self.price_rigidity = random.randrange(1,4)  # rigidity starts anew
        
        global wto, trade_costs, transport_firms
        self.prices = self.price*(1 + trade_costs[self.country]) * wto.exch_rates[self.country]
        #self.exporting_price =  self.prices[0] if self.country == 1 else self.prices[1]    ### added at the end for chosen
        
        if transport_firms == 1:                # exporting transportation firms
            self.trade_fees = list(self.price * trade_costs[self.country])
        elif transport_firms == 2:              # importing transportation firms
            self.trade_fees = list(self.price * trade_costs[self.country] * wto.exch_rates[self.country])
        elif transport_firms == 3:              # 50:50
            self.trade_fees_1 = list(0.5*self.price * trade_costs[self.country])
            self.trade_fees_2 = list(0.5*self.price * trade_costs[self.country] * wto.exch_rates[self.country])
        
        # wage offer
        if self.skip_in_first:     # in the first period leave initial wage to rule                            ???
            self.skip_in_first = False
            
        elif hiring > 0:
            alpha, beta = random.random(), random.random()
            alpha_beta =  alpha*beta
            sum_labor_d = sum(self.labor_d_series)
            self.vacancy_rate = 0 if sum_labor_d == 0 else sum(self.vacancy_series)/sum_labor_d # average rate over past 4 periods
            vacancy_diff = (self.vacancy_T - self.vacancy_rate)/self.vacancy_T    # proportional diff. between targeted and actual vacancy rates
            if alpha_beta < vacancy_diff:              # too few vacancies -> excessive labor supply, decrease wage
                delta_wage = -alpha*self.wage_flex_down 
            elif alpha_beta < -vacancy_diff:           # too many vacancies, increase wage
                delta_wage = alpha*self.wage_flex_up
            else:
                delta_wage = 0
            self.wage *= 1 + delta_wage               # not rounded, round only when making contract
                    
        
        # loans required
        wage_bill = sum([contract.wage for contract in self.contracts])   # wages of currently employed workers
        if hiring > 0:
            wage_bill += hiring*round(self.wage)              # add expected new wages
        needs = wage_bill - self.account.deposit
        if needs > 0:
            self.account.debts.append(Loan(needs, self))      # make a new loan
            
        self.hiring = hiring
        self.new_hirings = 0
    
    
    def job_update(self, contract): 
        """Adding a new employee, updating labor offering. Part of labor market."""
        self.contracts.append(contract)
        self.labor += 1
        self.new_hirings += 1
        if self.labor_d > self.labor:     
            self.job_offering = True                                                ## redundant
        else:
            self.job_offering = False
    
    
    def produce(self):
        """Advancing production, updating contracts, vacancy and labor data. After labor market."""
        self.new_prod = 0
        self.new_prod_value = 0
        self.vacancies = self.hiring - self.new_hirings if self.hiring > 0 else 0
        self.vacancy_series.append(self.vacancies)
        self.labor_d_series.append(self.labor_d)
        self.vacancy_series, self.labor_d_series = self.vacancy_series[-4:], self.labor_d_series[-4:]
        
        self.machines.sort(key = lambda machine: machine.progress, reverse = True)  # most advanced machines first
        for mach, contr in zip(self.machines[:self.labor], self.contracts):  
            mach.update(contr.wage)           # advances production, updates newly finished inventories
            contr.update()                    # pays wages, updates list of contracts to cancel
        self.inv += self.new_prod
        self.inv_value += self.new_prod_value
        
        if self.inv > 0:
            self.unit_cost = self.inv_value/self.inv                       ## needed except when price == 0 ?
        else:
            self.unit_cost = 0
                   
            
    def determine_supply(self):
        """Determination of the volume of goods offered to the market."""
        self.goods_offering = False           # refreshing
        if self.inv != 0 and self.price > 0:
            prod_level = self.util_rate_T/100
            # SmartStoreManager version, not what is described in the paper
            if self.inv <= self.inv_T:
                self.supply = int(prod_level*self.inv/2)                            # truncated value
            else:                                               
                # note - self.inv_T == 2*self.K*self.productivity 
                self.supply = int(prod_level*self.inv_T/2 + self.inv - self.inv_T)  # truncated value
##            # version from BasicStoreManager follows what is described in the paper   
##            self.supply = min(self.sell_ratio*self.inv, self.inv_T)     
        
        else:
            self.supply = 0
        
        if self.supply > 0:
            self.goods_offering = True
        
        self.curr_supply = self.supply
        self.sales, self.cost_of_sales, self.sales_value = 0, 0, 0       # refresh for the current period
        self.sales_series.append(0)
        self.sales_series = self.sales_series[-12:]

        self.nom_supply = self.supply*self.price            #####
        
    
    def goods_sale(self, volume, country):           
        """Sale of goods, a single transaction. Part of goods market."""
        value = int(volume * self.prices[country])                   # truncated
        domestic_value = int(volume * self.price)
        self.curr_supply -= volume
        self.sales += volume
        self.sales_series[-1] += volume                             ## to set once after all sales are done ?? no, leave it
##        self.sales_value += value
##        self.account.deposit += value
        self.sales_value += domestic_value
        self.account.deposit += domestic_value
        
        global transport_firms, trans_firms
        if transport_firms == 1:              # exporting transportation firms
            trans_firms[self.country].total_profits += int(volume*self.trade_fees[country])   # truncated
        elif transport_firms == 2:            # importing transportation firms
            import_costs = int(volume*self.trade_fees[country])   # truncated
            trans_firms[country].total_profits += import_costs
        elif transport_firms == 3:
            import_costs = int(volume*self.trade_fees_2[country])
            trans_firms[self.country].total_profits += int(volume*self.trade_fees_1[country])
            trans_firms[country].total_profits += import_costs
        
        
        global wto, global_bank
        if not global_bank:
##            wto.bank_accounts[self.country] += value    # transaction accounted for in inter-bank accounts
            if transport_firms in [2,3]:
                wto.bank_accounts[self.country] += domestic_value
                wto.bank_accounts[country] -= value - import_costs
            else:
                wto.bank_accounts[self.country] += domestic_value    
                wto.bank_accounts[country] -= value         # for receiving bank it offsets a new liability (deposit) and vice versa

##        if country != self.country:
##            wto.imports[country] += volume
##            wto.exports[self.country] += volume
        wto.export_details[self.country][country] += volume
##        wto.import_details[country][self.country] += volume        # symmetrical to exports
        
        transf_value = int(self.inv_value*volume/self.inv) # truncated
        self.inv_value -= transf_value                # value of inventories are decreased proportionally to volume
        self.inv -= volume   
        self.cost_of_sales += transf_value            # production cost of sold goods, based on average unit cost
        
        if self.curr_supply <= 0:
            self.goods_offering = False
        
        
    def go_bankrupt(self):
        """Lays-off all workers, remove itself from the list of firms. Part of debt recovery process."""
        global FIRMs, BANKs, add_firms, period, global_bank
##        if self.bankrupt:
##            print(str(period) + ": " + self.ID + " is already bankrupted")
##        else:
        self.bankrupt = period                                                  ## not needed anywhere
        self.lay_off(self.labor, False)               # lay off all workers
        self.contracts_to_cancel = []
        self.owner.rec_div -= 1
        t_f = random.randrange(12,36)          # time until a new firm replacing this one is created
        add_firms[self.country][t_f] += 1
        
        # updating list of firms and accounts
        FIRMs[self.country].remove(self)
        bank = BANKs[self.country]             
        bank.accounts.remove(self.account)
        bank.firm_accounts.remove(self.account)
        if global_bank:
            bank.accounts_bc[self.country].remove(self.account)
            bank.firm_accounts_bc[self.country].remove(self.account)
        
    
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
        
