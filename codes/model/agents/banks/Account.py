
class Account:
    """Bank account for firms and households."""
    def __init__(self, country, holder):                           ## to modify what bank is it in if foreign debts allowed
        global BANKs, global_bank
        self.country = country
        self.holder = holder
        self.deposit = 0
        self.loans = 0
        self.doubtful_loans = 0
        self.domestic_loans = 0        # value of loans in domestic currency when in regime of 1 global bank
        self.debts = []
        self.extended_debts = []
        self.debts_to_remove = []
        BANKs[country].accounts.append(self)
        if global_bank:
            BANKs[country].accounts_bc[country].append(self)
        if "f" in holder.ID:                # if holder is a firm
            BANKs[country].firm_accounts.append(self)
            self.bad = False
            if global_bank:
                BANKs[country].firm_accounts_bc[country].append(self)
    
    def sort_debts(self):
        """Extended debts should be dealt with first."""
        self.debts = self.extended_debts + [debt for debt in self.debts if not debt.extended]
    
    
    def get_amount(self):                                                              ## not needed 
        """Returns overall value of the account."""
        return self.deposit - self.loans
    
    def get_status(self):                                                              ## not needed 
        """Returns debtor status."""
        return sum([loan.extended for loan in self.debts]) > 0  # is status doubtful?
