

def do_period():
    """Executes all action of a period."""
    # 0. initialing new period
    global period, HSHs, all_HSHs, FIRMs, BANKs, wto, global_bank
    period += 1
    add_new_firms()
    
    if period == 120:                      # in JAMEL it is in 01/2010
        for bank in BANKs:
            bank.accommodating = False     # firms can go bankrupt
            
    global shuffled_HSHs
    shuffled_HSHs = [np.random.permutation(country_hshs) for country_hshs in HSHs]  # shuffling so order in markets etc is random
    random.shuffle(all_HSHs)                                                        # shuffle in place
##    shuffled_FIRMs = [np.random.permutation(country_firms) for country_firms in FIRMs]  
    
    
    
    # 0. refresh data, update sentiments
    if period > 0:
        wto.update()
    [firm.new_period() for country in FIRMs for firm in country]                          ## keep this as first
    [firm.sentiment_update() for country in FIRMs for firm in country]  
    [hsh.sentiment_update() for hsh in all_HSHs]                       ## actually no need to shuffle here
          
    # 1. dividends are paid
    if global_bank:
        BANKs[0].pay_dividend()
    else:
        for bank in BANKs:
            bank.pay_dividend()
    [firm.pay_dividend() for country in FIRMs for firm in country]
    
    
    # 2.  production planning
    [firm.production_plan() for country in FIRMs for firm in country]
        
    
    # 3.a labor market together with production and wage pay
    labor_market()
    
    # 3.b production is undertaken, wages are paid
    [firm.produce() for country in FIRMs for firm in country] 
    
    
    # 4.a firms choose amount of inventories to offer
    [firm.determine_supply() for country in FIRMs for firm in country]
    
    # 4.b HSHs adjust consumption         
    [hsh.consumption_update() for hsh in all_HSHs]
    
    
    # 5. market with goods
    goods_market()
    
    global transport_firms
    if transport_firms != 0:
        global trans_firms
        [tr.pay_out() for tr in trans_firms]     # paying out trade costs to households owning transportation firms
    
    # 6. debt recovery
    if global_bank:
        BANKs[0].debt_recovery()
        BANKs[0].review()
    else:
        for bank in BANKs: 
            bank.debt_recovery()
            bank.review()
        
    # 7. data collection
    update_ts()

