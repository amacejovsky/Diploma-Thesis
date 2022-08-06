
class Bank:
    """Individual bank."""
    
    def __init__(self, country, ID):
        global HSHs, global_bank, no_countries
        # parameters       
        self.target_ratio = kappa_B   # targeted capital ratio
        self.accommodating = True        # firms dont go bankrupt until month 120
        self.bankrupt = False    
        
        # bank-specific attributes
        self.type = "b"    #  bank, firm, hsh
        self.country = country
        self.ID = str(self.country) + "_" + "b" + "_" + str(ID)
        self.owner = random.choice(HSHs[country])           # randomly chosen domestic HSH
        self.owner.rec_div += 1
                
        # variables and initial values
        self.own_deposit = 0         # bank's own money
        self.deposits = 0            # of firms and HSHs
        self.firm_deposits = 0
        self.hsh_deposits = 0
        self.interests = 0           # sum of interests paid by firms in a period
        self.loans = 0               # sum of loans currently on books
        self.doubtful_loans = 0
        self.doubtful_ratio = 0      # ratio of doubtful loans in terms of value   
        
        self.accounts = []           # list of accounts of HSHs and firms
        self.firm_accounts = []                       ## what is more efficient - keeping separate lists or subsetting ???
        if global_bank:
            self.accounts_bc = [[] for i in range(no_countries)]     # accounts sorted by countries
            self.firm_accounts_bc = [[] for i in range(no_countries)] 
        
        self.bankruptcies = []       # list of bankruptcies in the current period
        self.no_of_bankruptcies = 0
        self.losses = 0              # lost assets due bad loans in the current period
         
        self.capital = self.loans - self.deposits      # should be equal to own deposit           
        self.target = self.loans * self.target_ratio   # targeted level of capital                    
        self.dividend = max(0, self.capital - self.target)
        
        
    def pay_dividend(self):
        """Pays dividend to its owner."""
        if self.dividend > 0:
            self.owner.account.deposit += self.dividend 
            self.owner.income += self.dividend
            self.own_deposit -= self.dividend
            
            
    def debt_recovery(self):
        """Interests are paid, due debts recovered, firms go bankrupt."""
        global wto, global_bank, no_countries
        self.bankruptcies = []     # refreshing
        self.interests = 0         # refreshing
        self.losses = 0            # refreshing
##        shuffled_accounts = np.random.permutation(np.array(self.firm_accounts))
        random.shuffle(self.firm_accounts)  # shuffling accounts in place
##        for account in shuffled_accounts:
        for account in self.firm_accounts:
            for loan in account.debts:              
                loan.pay_interest()                  
            account.sort_debts()            # during pay_back() extended loans must be dealt with first              
##        for account in shuffled_accounts:    
        for account in self.firm_accounts:  # keep separate loops due to the need of financing bankruptcies
            for loan in account.debts:
                loan.pay_back()             # pays back principal, downgrades, and add bankruptcies
                if account.bad:
                    break
            [account.debts.remove(loan) for loan in account.debts_to_remove]
            [account.extended_debts.remove(loan) for loan in account.debts_to_remove if loan.extended]
            account.debts_to_remove = []
                
        if global_bank:
            self.no_of_bankruptcies = [sum([f.country == cc for f in self.bankruptcies]) for cc in range(no_countries)]
        else:
            self.no_of_bankruptcies = len(self.bankruptcies)
        
        doubtful_sub = 0
        for firm in self.bankruptcies:
            self.losses += firm.account.loans 
            doubtful_sub += firm.account.doubtful_loans
            firm.go_bankrupt()
        
        self.own_deposit -= self.losses    # bank loses money
        self.loans -= self.losses
        self.doubtful_loans -= doubtful_sub
        if not self.bankrupt:
            if self.own_deposit <= 0:       # bank has lost too much money
                global period
                self.bankrupt = period            
                print(str(period) + ": ", "Bank", self.ID, "is bankrupt!")
        
    def review(self):                                                                   ## to incorporate to debt_recovery ?
        """Calculates assets, liabilities, capital."""
        global wto, global_bank, period
        if global_bank:
            self.deposits = sum([sum([int(account.deposit*wto.exch_rates[i][0]) for account in cc]) for i, cc in enumerate(self.accounts_bc)])
            self.firm_deposits = sum([sum([int(account.deposit*wto.exch_rates[i][0]) for account in cc]) for i, cc in enumerate(self.firm_accounts_bc)])
        else:
            self.deposits = sum([account.deposit for account in self.accounts]) 
            self.firm_deposits = sum([account.deposit for account in self.firm_accounts]) 
        self.hsh_deposits = self.deposits - self.firm_deposits
##        self.loans = sum([account.loans for account in self.firm_accounts])    
##        self.doubtful_loans = sum([loan.amount for account in self.firm_accounts for loan in account.debts if loan.extended])
        self.doubtful_ratio = self.doubtful_loans/self.loans if self.loans != 0 else 0        ### can be calculated during data finalization
        
        ## JAMEL version of doubtful ratio                                   #################################
##        self.doubtful_loans2 = sum([account.loans for account in self.firm_accounts  if account.get_status()])
##        self.doubtful_ratio2 = self.doubtful_loans2/self.loans if self.loans != 0 else 0  
        
        
        # deposits flow to and from foreign banks is accounted for so it does not play any role in capital determination
        self.capital = self.loans - self.deposits + wto.bank_accounts[self.country]
        self.target = int((self.deposits - wto.bank_accounts[self.country])*self.target_ratio)   # truncated      
        self.dividend = max(0, self.capital - self.target)  
        
        
        if not self.bankrupt:
            if self.capital < 0:      # bank is bankrupt
                self.bankrupt = period 
                print(str(period) + ": ", "Bank ", self.ID, " is bankrupt!")
#        if self.capital != self.own_deposit:                                                 #########  to delete
#            print(str(period) + ": ", "Bank ", self.ID, " capital inconsistency!")

