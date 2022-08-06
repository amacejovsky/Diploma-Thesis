class Machine:
    """Individual machine. Listed within a firm. Keeps track of its production process progress and value."""
   
    def __init__(self, firm, ID):
        self.productivity = productivity   # amount of volume added in 1 update
        self.prod_length = production_time             # length of production
    
        self.ID = ID         # firmID + "_m" + NUMBER
        self.firm = firm
        self.progress = 0    # how far is it in production process?
        self.value = 0       # wages spend on working this machine during current production process
    
    def update(self, wage):
        """Updates production process, add inventories when the process finishes."""
        self.progress += 1
        self.value += wage
        if self.progress >= self.prod_length:
            self.firm.new_prod += self.productivity*self.progress   # final volume is 8*productivity
            self.firm.new_prod_value += self.value
            self.progress = 0        # refresh
            self.value = 0           # refresh

