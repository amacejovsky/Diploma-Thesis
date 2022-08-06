class Contract:
    """Job contract. Listed within a firm. Keeps track of the partakers, its wage and length, pays out wages."""
    def __init__(self, hsh, firm):
        self.hsh = hsh
        self.firm = firm
        self.wage = round(firm.wage)
        self.length = random.randrange(6,18)          # how long it will last
        self.time = 0                        # number of periods since initialization
        hsh.employed = True
        #hsh.months_u = 0                                                           ## as in JAMEL code, do not update yet
        hsh.wage = self.wage
        
    def update(self):
        """Pays wage, updates time, in due time adds itself to firm's list of contracts to cancel."""
        self.time += 1
        self.hsh.worked = True                # hsh was employed in the current period, used for opinion model
        self.hsh.account.deposit += self.wage  
        self.hsh.income += self.wage
        self.firm.account.deposit -= self.wage  
        if self.time >= self.length:
            self.firm.contracts_to_cancel.append(self)
            
    def cancel(self, delete_wage = False):
        """Cancels the contract in due time or if layed-off."""
        self.hsh.employed = False
        if delete_wage:               # if layed-off during production planning
            self.hsh.wage = 0

