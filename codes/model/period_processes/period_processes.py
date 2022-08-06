
# 0. after bankruptcies when regeneration time passes, add new firms
def add_new_firms():
    """After bankruptcy, add new firms when the regeneration period has passed."""
    global add_firms, FIRMs
    for country in range(no_countries):
        N = add_firms[country].pop(0)             # number of firms to add in the current period
        add_firms[country].append(0)              # add to the end of list for new bankruptcy entries
        for i in range(N):
            ID = FIRMs[country][-1].ID_no + 1
            new_firm = Firm(country,ID)
            new_firm.wage = random.choice(FIRMs[country]).wage       # initial wage is randomly copied from another firm
            FIRMs[country].append(new_firm)
            


# In[ ]:





# labor_market function

# In[23]:


# 3. labor market
def labor_market():
    """Firms offer wages, unemployed households choose the best ones. Contracts are made if the best wage is high enough.
    Market is closed within each country."""
    global l_providers, all_HSHs, shuffled_HSHs, FIRMs
    #G = providers                             # makes reference quicker
    unemployed = [[not hsh.employed for hsh in country] for country in shuffled_HSHs]   # HSHs are already shuffled
    unemployed_HSHs = [shuffled_HSHs[i][unemployed[i]] for i in range(no_countries)]    # arrays of all unemployed HSHs
    
##    # version 0 is with only offering firms considered,  version 1 with all non-bankrupt as in the JAMEL code
##    offering = [np.array([firm.job_offering for firm in country]) for country in FIRMs]
##    offering_firms = [FIRMs[i][offering[i]] for i in range(no_countries)]   # arrays of all job-offering firms
    for hsh in all_HSHs:
        hsh.res_wage_update()     # all HSHs update their reservation wage

    for country, un_HSHs in enumerate(unemployed_HSHs):  # country's number and shuffled unemployed HSHs 
        for hsh in un_HSHs:
##            # version 0 - considering only firms which actually offer new jobs
##            if len(offering_firms[country]) > G:
##                firms = np.random.choice(offering_firms[country], G, replace = False)    # labor market only for domestic firms
##            elif len(offering_firms[country]) > 0:
##                firms = offering_firms[country]
##            else:        # no more firms which offer jobs
##                break         
##            offers = {firm : firm.wage  for firm in firms}               ## seems like using lists, list.index(max(list)) 
                                                                          ## would be actually quicker
            # version 1 - version from JAMEL code, considers all firms                                                 
            firms = random.choices(FIRMs[country], k = l_providers)     # with replacement as in JAMEL code
            offers = {firm : firm.wage  for firm in firms if firm.job_offering}
            if len(offers) == 0:     
                continue                            # no firms offering jobs were drawn, hsh remains unemployed
            
            winner = max(offers, key = offers.get)  # firm with highest offered wage     
            if winner.wage >= hsh.res_wage:        # job accepted only if offered wage >= reservation wage
                contr = Contract(hsh, winner)      # creates new contract
                winner.job_update(contr)           # updates firm's labor information
            else:
                hsh.vol_unemployed = True          # hsh refused offered wage - voluntarily unemployed
                
##                # version 0
##                if not winner.job_offering:   # remove winner from job-offering firms if they fulfilled their demand
##                    offering_firms[country] = np.delete(offering_firms[country],
##                                                        np.where(offering_firms[country] == winner))
        


# market_creation, goods_market functions

# In[24]:


# 5. goods markets
def market_creation():
    """Based on trade quotas, randomly chooses firms which are allowed to participate in countries' goods markets."""
    global FIRMs, free_market, trade_quotas
    if free_market:                     # all firms are allowed to all markets
        result = [firm for country in FIRMs for firm in country]
        return [result for country in FIRMs]
    else:
        result = [[] for country in FIRMs]
        for i, quotas in enumerate(trade_quotas):
            for j, quota in enumerate(quotas):  # each country has its own goods market made of all domestic and ...
                if quota == 1:                   # ...quota of allowed randomly chosen foreign firms
                    result[i].extend(FIRMs[j])
                elif quota == 0:
                    continue
                else:
                    number = int(quota*len(FIRMs[j]))
                    result[i].extend(random.sample(FIRMs[j], k = number))
        return result
    
def goods_market():
    """Global goods market - households and firms are paired, goods are bought and sold."""
    global period, all_HSHs, providers
    firms_to_choose = market_creation()
    
    for hsh in all_HSHs:      ## have been shuffled at the start of the period 
        d_c = hsh.country       # hsh's domestic country
        
        firms = random.sample(firms_to_choose[d_c], k = providers)  # sample without replacement
        firms = [f for f in firms if f.goods_offering]  # clear firms with zero supply
        firms.sort(key = lambda f: f.prices[d_c])       # firms are ordered by price, ascending
        budget = hsh.budget
        try:
            winner = firms.pop(0)     # firm with lowest price is returned and removed 
        except:                       # no firm that offers goods was drawn
            if (period > 35):    # in JAMEL if year > 2002
                for i in range(10):                     # try to spend rest of the budget on 10 random firms
                    winner = random.choice(firms_to_choose[d_c])                          #### perhaps choose domestic ???
                    if winner.goods_offering:
                        price = winner.prices[d_c]
                        if budget > price:              # strictly higher as in JAMEL code
                            volume = int(budget/price)  # truncated
                            value = int(price*volume)   # truncated
                            budget -= value
                            hsh.purchase(volume, value)
                            winner.goods_sale(volume, d_c)
                            if budget == 0: break
            hsh.forced_savings = budget
            continue                  
##        offers = {firm : firm.price  for firm in firms}                     
##        winner = min(offers, key = offers.get)  
        empty = False                        # when are offering firms emtpy
        price = winner.prices[d_c]
        while budget >= price*winner.curr_supply:       # hsh can buy all of the firm's supply
##            if winner.goods_offering:
            volume = winner.curr_supply      #int(hsh.budget/winner.price)       # truncated
            value = int(price*volume)           # truncated
            budget -= value
            hsh.purchase(volume, value)
            winner.goods_sale(volume, d_c)
            #if winner.country != hsh.country:
                #winner.exporting = True                                                     ### added at the end for chosen
##                offering[0] = np.delete(offering[0], np.where(offering[0] == winner))  # firm has sold what it offered
##            del offers[winner]
            try:
##                winner = min(offers, key = offers.get)        
                winner = firms.pop(0)               # continue with firm with next lowest price
                price = winner.prices[d_c]
            except:
                empty = True                        # no more offers
                break
        if (not empty) and (budget > 0):               # all of the (remaining) budget is spend on 1 firm
            volume = int(budget/price)       # truncated
            if volume > 0:
                value = int(price*volume)    # truncated
                budget -= value
                hsh.purchase(volume, value)
                winner.goods_sale(volume, d_c)
        
        if (period > 35) and (budget > hsh.budget/10):    # in JAMEL if year > 2002
            for i in range(10):                     # try to spend rest of the budget on 10 random firms
                winner = random.choice(firms_to_choose[d_c])  
                price = winner.prices[d_c]
                if winner.goods_offering:
                    if budget > price:              # strictly higher in JAMEL
                        volume = int(budget/price)  # truncated
                        value = int(price*volume)   # truncated
                        budget -= value
                        hsh.purchase(volume, value)
                        winner.goods_sale(volume, d_c)
                        if budget == 0: break
        hsh.forced_savings = budget


# In[ ]:





# update_ts function

# In[25]:


# 7. updates time series data
def update_ts():
    """At the end of a period, updates data time series."""
    global TSs, chosen_HSHs, chosen_FIRMs, hsh_archive_variables, firm_archive_variables
    for ts in list(TSs.values()):
        ts.update()
    
    for hsh in chosen_HSHs:
        hsh.archiving(*hsh_archive_variables)
    for firm in chosen_FIRMs:
        firm.archiving(*firm_archive_variables)
    
