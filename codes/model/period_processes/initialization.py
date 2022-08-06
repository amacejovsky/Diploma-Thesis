

def init():
    """Create agents and time series."""
    # create lists of per-country arrays of  HSHs, firms and banks
    global HSHs, all_HSHs, BANKs, FIRMs, add_firms, wto, TSs, period, global_bank
    HSHs = [[HSH(country,ID) for ID in range(ns[country])] for country in range(no_countries)]
##    all_HSHs = list(np.concatenate(HSHs))      # HSHs from all countries in 1 long list 
    all_HSHs = []
    for country in HSHs:                       # HSHs from all countries in 1 long list 
        all_HSHs.extend(country)
    
    if global_bank:
        the_bank = Bank(0, 0)        # 1 global bank, always in the country 0
        BANKs = [the_bank for country in range(no_countries)]  # all references go to the global bank
    else:
        BANKs = [Bank(country, 0) for country in range(no_countries)]
    
    FIRMs = [[Firm(country,ID) for ID in range(ms[country])] for country in range(no_countries)]
    
    [hsh.create_account() for hsh in all_HSHs]     # create accounts for households
    
    add_firms = [ [0]*36 for i in range(no_countries)]  # numbers of firms to replace after bankruptcies in next periods
    
    wto = WTO()
    
    global transport_firms
    if transport_firms != 0: 
        global trans_firms
        trans_firms = [Trans_firm(country, 0) for country in range(no_countries)]
        

    # time series
    TSs = { # HSH
        "employment": TS("H", "worked", False),
        "wages": TS("H", "wage", True),
        "working_wages": TS("H", "wage", True, working_hsh),
        "vol_unemployed": TS("H", "vol_unemployed", False),
        "months_u": TS("H", "months_u", True),
        "unemployed_months_u": TS("H", "months_u", False, unemployed_hsh),
        "hsh_sentiment": TS("H", "sentiment", False),
        "hsh_income": TS("H", "income", True),
        "savings_T": TS("H", "savings_T", True),
        "budget": TS("H", "budget", True),
        "cons": TS("H", "cons", False),
        "cons_value": TS("H", "cons_value", True),
        "forced_savings": TS("H", "forced_savings", True),
        "hsh_deposits": TS("Hacc", "deposit", True),
        
        # firms
        "prices": TS("F", "price", True),
        "offered_wages": TS("F", "wage", True),
        "production": TS("F", "new_prod", False),
        "production_value": TS("F", "new_prod_value", True),
        "labor_demand": TS("F", "labor_d", False),
        "labor": TS("F", "labor", False),
        "job_offers": TS("F", "hiring", False),
        "vacancies": TS("F", "vacancies", True),
        "inventories": TS("F", "inv", True),
        "sales": TS("F", "sales", True),
        "sales_value": TS("F", "sales_value", True),
        "sales_costs": TS("F", "cost_of_sales", True),
        "firm_assets": TS("F", "assets", True),
        "firm_capital_target": TS("F", "capital_T", True),
        "firm_capital": TS("F", "capital", True),
        "firm_dividends": TS("F", "dividend", True),
        "firm_sentiment": TS("F", "sentiment", False),
        "firm_deposits": TS("Facc", "deposit", True),
        "loans": TS("Facc", "loans", True),
        
        #"exporting_firms": TS("F", "exporting", False),                                      ### added at the end for chosen
        #"exporting_prices": TS("F", "exporting_price", True, exporting_firms_fun) ,
        #"exporting_received_prices": TS("F", "price", True, exporting_firms_fun) ,
        #"exporting_assets": TS("F", "assets", True, exporting_firms_fun) ,
        #"exporting_capital": TS("F", "capital", True, exporting_firms_fun) ,
        #"exporting_capital_target": TS("F", "capital_T", True, exporting_firms_fun) ,
        #"exporting_loans": TS("Facc", "loans", True, exporting_firms_fun) ,                            ######
        
        #"nom_supply": TS("F", "nom_supply", True),   ######### added at the end just for experiment
        #"supply": TS("F", "supply", True),           ######### added at the end just for experiment
        #"unsold_supply": TS("F", "curr_supply", True),           ######### added at the end just for experiment
        
        # bank
        "bank_capital": TS("B", "capital", False),
        "bank_deposit": TS("B", "own_deposit", False),
        "deposits": TS("B", "deposits", False),
        "doubtful_loans": TS("B", "doubtful_loans", True),
        "doubtful_ratio": TS("B", "doubtful_ratio", False),
        "bankruptcies": TS("B", "no_of_bankruptcies", False),
        "bank_dividend": TS("B", "dividend", False),
##        "doubtful_ratio2": TS("B", "doubtful_ratio2", False),         #######################################
        
        # special additions
        "spec_no_of_firms": Special_TS("no_of_firms"),
        "spec_exch_rates": Special_TS("exch_rates"),
        "spec_natural_exch_rates": Special_TS("natural_exch_rates"),
        "spec_export_details": Special_TS("export_details"),
        "spec_import_details": Special_TS("import_details"),      ## make sure it is updated before trade balances
        "spec_trade_balances": Special_TS("trade_balances"),      ## important part for functioning of the model
        "spec_bank_accounts": Special_TS("bank_accounts")
        
    }

    if transport_firms != 0:
        TSs["spec_trade_fees"] = Special_TS("trade_fees")    
    
    period = -1
    

