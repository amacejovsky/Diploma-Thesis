
class Trans_firm:
    def __init__(self, country, ID):
        global HSHs, no_countries
        self.type = "t"    #  bank, firm, hsh
        self.country = country
        self.ID_no = int(ID) 
        self.ID = str(self.country) + "_" + "t" + "_" + str(ID)
        self.owner = random.choice(HSHs[country])    # randomly chooses owner (possibility of repetition for diff. firms)
        self.owner.rec_div += 1
        
##        self.profits = [0]*no_countries
        self.total_profits = 0
        self.old_profits = 0
        
    def pay_out(self):
        """At the end of period, pays out all gained trade costs to its owner."""
##        self.total_profits = sum(self.profits) 
        self.owner.account.deposit += self.total_profits
        self.owner.income += self.total_profits 
        self.owner.yearly_income[-1] += self.total_profits
##        self.profits = [0]*no_countries
        self.old_profits = self.total_profits
        self.total_profits = 0

