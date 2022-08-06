
def yearly2monthly(annual_rate):
    """Recalculates yearly interest rate to monthly terms."""
    return (1 + annual_rate)**0.0833333358168602 - 1        # using the formula from the original JAMEL code


class Loan:
    """Individual loan. Keeps track of its length, interest rate, quality, pays back interest and principal, downgrades itself."""
    
    def __init__(self, amount, firm):
        """Increases receiving firm's deposit, loans."""
        global BANKs, global_bank, wto
        # parameters
        self.length1 = normal_length     # initial period expiration
        self.length2 = extended_length   # extended period of expiration
        self.extended = False
        self.y_rate = r                 # normal interest rate - yearly
        self.rate = yearly2monthly(r)   # monthly normal rate
        self.y_extended_rate = r_       # premium int rate - yearly
        self.extended_rate = yearly2monthly(r_) # nomthly premium rate
        self.time = 0       # start paying interests immidiately, in total 13 interest payments before recovery
        
        if global_bank:                                                     # need zloty, borrow in euro
            self.principal = int(amount*wto.exch_rates[firm.country][0])    # PLN/EUR, rounding down
##            self.account.domestic_loans += amount                           # PLN
        else:
            self.principal = amount
        self.firm = firm
        self.country = firm.country
        self.account = firm.account
        self.bank = BANKs[self.country]        # firm's domestic bank      
        self.account.deposit += amount         # when foreign bank then firm gets amount in its currency...
        self.account.loans += self.principal   #... but loan is denominated in bank's currency
        self.bank.loans += self.principal      #...  
        self.actual_rate = self.rate
        
    
    def pay_interest(self):
        """Pays back interest, if firm does not have money for it it adds the difference to the principal."""
        global global_bank, wto
        interest = int(self.principal*self.actual_rate)    # truncating
        if global_bank:
            diff = interest - int(self.account.deposit*wto.exch_rates[self.country][0]) # PLN/EUR
        else:
            diff = interest - self.account.deposit
        
        if diff > 0:                 # interest paid by additional borrowing
            self.principal += diff              
            self.account.loans += diff
            self.bank.loans += diff                                                    ## leave it to bank.review() ?
            if self.extended:
                self.bank.doubtful_loans += diff
                self.account.doubtful_loans += diff
            self.account.deposit = 0                                            ## neglecting residue from currency exchange 
        else:
            if global_bank:
                self.account.deposit -= int(interest*wto.exch_rates[0][self.country]) # EUR/PLN
            else:
                self.account.deposit -= interest
        self.bank.own_deposit += interest
        self.bank.interests += interest
    
   
    def pay_back(self):
        """Pays back (part of) principal if due or if doubtful."""
        global global_bank, wto
        if global_bank:
            funds = round(self.account.deposit*wto.exch_rates[self.country][0]) # PLN/EUR
        else:
            funds = self.account.deposit
        repayment = min(self.principal, funds)
        if self.extended:                   # repays what it can
            if self.time >= self.length2:        # is due
                if repayment < self.principal:   # not fully repaid
                    self.downgrade()
            self.principal -= repayment
            self.account.loans -= repayment   
            self.account.doubtful_loans -= repayment
            self.bank.loans -= repayment                        ## or maybe leave to cumulative summation in bank.review()
            self.bank.doubtful_loans -= repayment               ##
            if global_bank:
                self.account.deposit -= int(repayment*wto.exch_rates[0][self.country]) # EUR/PLN
            else:
                self.account.deposit -= repayment
        
        else:
            if self.time >= self.length1:       # is due
                self.principal -= repayment
                
                self.account.loans -= repayment   
                self.bank.loans -= repayment                    ## or maybe leave to cumulative summation in bank.review()
                if global_bank:
                    self.account.deposit -= int(repayment*wto.exch_rates[0][self.country]) # EUR/PLN
                else:
                    self.account.deposit -= repayment
                if 0 < self.principal:          # not fully repaid
                    self.downgrade()
                    
        self.time += 1
        if self.principal <= 0:                 # modify list of firm's debts
            self.account.debts_to_remove.append(self)           ## dont remove now so as to not mess with iteration through debts
##            self.account.debts.remove(self)
##            if self.extended:
##                self.account.extended_debts.remove(self)
        
        
    def downgrade(self):
        """Downgrades loan if principal is not paid back in due time."""
        self.time = 0                           # new repayment period starts
        if self.extended:
            if self.bank.accommodating:
                self.account.extended_debts.remove(self)
                self.account.extended_debts.append(self)  # now it is the newest extended loan
            else:
                self.bank.bankruptcies.append(self.firm)       # firm must go bankrupt
                self.account.bad = True
        else:
            self.extended = True
            self.actual_rate = self.extended_rate
            self.account.extended_debts.append(self)      # now it is the newest extended loan
            self.bank.doubtful_loans += self.principal
            self.account.doubtful_loans += self.principal
    
