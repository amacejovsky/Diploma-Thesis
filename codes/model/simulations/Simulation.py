
class Simulation:
    """Initiliazes and runs a simulation of the model. Exports created datasets."""
    def __init__(self, 
                 seed1 = None, seed2 = None,
                 chosen_agents_indeces = "default",
                 chosen_variables = "default"):
        """Initiliazes a simulation. 
        Random seeds can be specified for replication purposes. They are inherited throughout the methods of the class.
        Chosen individual agents can archive their chosen micro-data."""
        global no_countries
        if chosen_agents_indeces == "default":
            chosen_agents_indeces = [ [[0]]*no_countries, [[0]]*no_countries ]
        if chosen_variables == "default":
            chosen_variables = [ ["cons_value"], ["dividend"] ]                               ## or something
        
        self.seed1 = seed1
        self.seed2 = seed2
        if seed1 is not None:                                     ## or leave it even if seed == None, doesnt really matter
            random.seed(seed1)   
        if seed2 is not None:
            np.random.seed(seed2)   # random seeds hold for the whole simulation
        
        init()                           # initialization of agents, time series
        global HSHs, FIRMs, chosen_HSHs, chosen_FIRMs, hsh_archive_variables, firm_archive_variables
        # create lists of agents who archive their micro-data
        chosen_HSHs = [country[hsh_i] for c, country in enumerate(HSHs) for hsh_i in chosen_agents_indeces[0][c] ]
        chosen_FIRMs = [country[f_i] for c, country in enumerate(FIRMs) for f_i in chosen_agents_indeces[1][c] ] 
        hsh_archive_variables, firm_archive_variables = chosen_variables
                
        
    def run(self, no_of_periods = 12, seeds = "continue"):
        """Run given number of periods. Random seeds can be changed; 
        choose "continue" for inheriting the current random state."""
        if seeds != "continue":
            self.seed1, self.seed2 = seeds
            random.seed(seeds[0])               # seed == None is equivalent to no seed
            np.random.seed(seeds[1])            # seed == None is equivalent to no seed
        
        for t in range(no_of_periods):
            do_period()
            
    def finalize_data(self):
        """Prepares final data - constructs ratios, growth rates, yearly time series."""
        global TSs, K, BANKs
        self.additional_ts = {}
        # yearly inventories
        self.additional_ts["inventories_y"] = periodize(TSs["inventories"].sums(), False)
        
        # motnhly and yearly unemployment rates
        unemployment_m = differences("ones", TSs["employment"].means())
        self.additional_ts["unemployment_m"] = unemployment_m
        self.additional_ts["unemployment_y"] = periodize(unemployment_m, True, True)
        self.additional_ts["vol_unemployed_rate_m"] = ratios(TSs["vol_unemployed"].means(), unemployment_m)
        self.additional_ts["vol_unemployed_rate_y"] = ratios(periodize(TSs["vol_unemployed"].means()), self.additional_ts["unemployment_y"])
        
        # monthly and yearly inflation, sales
        price_level_m = ratios(TSs["sales_value"].sums(), TSs["sales"].sums())
        self.additional_ts["price_level_m"] = price_level_m
        self.additional_ts["inflation_m"] = growths(price_level_m)
        sales_y = periodize(TSs["sales"].sums())
        self.additional_ts["sales_y"] = sales_y
        sales_value_y = periodize(TSs["sales_value"].sums())
        self.additional_ts["sales_value_y"] = sales_value_y
        price_level_y = ratios(sales_value_y, sales_y)
        self.additional_ts["price_level_y"] = price_level_y
        self.additional_ts["inflation_y"] = growths(price_level_y, add_zero = True)
        
        # yearly vacancy rates
        self.additional_ts["vacancy_rates_m"] = ratios(TSs["vacancies"].sums(), TSs["labor_demand"].sums())
        vacancies_y = periodize(TSs["vacancies"].sums())
        self.additional_ts["vacancies_y"] = vacancies_y
        labor_demand_y = periodize(TSs["labor_demand"].sums())
        self.additional_ts["labor_demand_y"] = labor_demand_y
        self.additional_ts["vacancy_rates_y"] = ratios(vacancies_y, labor_demand_y)
        
        # banks' capital adequacy ratio
        self.additional_ts["capital_adequacy_ratio_m"] = ratios(TSs["bank_capital"].sums(), TSs["loans"].sums())
        
        # yearly and monthly profits, total income and share of profits and wages
        gross_profits_m = differences(TSs["sales_value"].sums(), TSs["sales_costs"].sums(), relative = False)
        self.additional_ts["gross_profits_m"] = gross_profits_m
        total_income_m = differences(TSs["wages"].sums(), gross_profits_m, relative = False, reverse = True)  # sum
        self.additional_ts["total_income_m"] = total_income_m
        self.additional_ts["wage_share_m"] = ratios(TSs["wages"].sums(), total_income_m)
        self.additional_ts["profits_share_m"] = ratios(gross_profits_m, total_income_m)
        gross_profits_y = periodize(gross_profits_m)
        self.additional_ts["gross_profits_y"] = gross_profits_y
        total_income_y = periodize(total_income_m)
        self.additional_ts["total_income_y"] = total_income_y
        wages_y = periodize(TSs["wages"].sums())
        self.additional_ts["wages_y"] = wages_y
        self.additional_ts["wage_share_y"] = ratios(wages_y, total_income_y)
        self.additional_ts["profits_share_y"] = ratios(gross_profits_y, total_income_y)
        
        # mean real profits per active firm
        self.additional_ts["mean_real_profits_m"] = ratios(ratios(gross_profits_m, price_level_m),  TSs["spec_no_of_firms"].sums())
        self.additional_ts["mean_real_profits_y"] = ratios(ratios(gross_profits_y, price_level_y),
                                                           periodize(TSs["spec_no_of_firms"].sums()), multiply = 12)  ## multiply because number of firms is accumulated
        
        # mark-ups over production costs, ie wages
        self.additional_ts["mark_ups_m"] = ratios(differences(TSs["sales_value"].sums(), TSs["wages"].sums(), relative = False),
                            TSs["wages"].sums())
        self.additional_ts["mark_ups_y"] = ratios( differences(sales_value_y, wages_y, relative = False),  wages_y )
        
        # bankruptcy rates
        bankruptcies_y = periodize(TSs["bankruptcies"].sums())
        self.additional_ts["bankruptcies_y"] = bankruptcies_y
        try:                             # if simulation ended at the end of december
            self.additional_ts["bankruptcy_rate_y"] = ratios(bankruptcies_y, 
                                                             periodize(TSs["spec_no_of_firms"].sums(),cumulation = False))
        except:                          # if simulation ended within an unfinished year
            self.additional_ts["bankruptcy_rate_y"] = ratios(bankruptcies_y, 
                                                             cut(periodize(TSs["spec_no_of_firms"].sums(),cumulation = False), end = -1)) 
        
        # capacity utilization
        self.additional_ts["capacity_utilization_m"] = ratios(TSs["labor"].sums(), TSs["spec_no_of_firms"].sums(), multiply = K)
        self.additional_ts["capacity_utilization_y"] = ratios(periodize(TSs["labor"].sums()), periodize(TSs["spec_no_of_firms"].sums()),  multiply = K)
        
        # mean and median monthly and yearly real wages among working population
        self.additional_ts["mean_real_wage_m"] = ratios(TSs["working_wages"].means(), price_level_m)       
        self.additional_ts["median_real_wage_m"] = ratios(TSs["working_wages"].medians(), price_level_m)
        self.additional_ts["mean_real_wage_y"] = ratios(ratios(
                                                 periodize(TSs["working_wages"].sums()), periodize(TSs["employment"].sums())
                                                               ), price_level_y)
        
        # firms' self-financing ratio and targeted debt
        self.additional_ts["self_financing_ratio_m"] = ratios(TSs["firm_capital"].sums(), TSs["firm_assets"].sums())
        self.additional_ts["targeted_debt_ratio_m"] = differences(TSs["firm_assets"].sums(), TSs["firm_capital_target"].sums(), relative = True)  # ratio
        self.additional_ts["targeted_debt_m"] = differences(TSs["firm_assets"].sums(), TSs["firm_capital_target"].sums())
        self.additional_ts["mean_targeted_debt_m"] = differences(TSs["firm_assets"].means(), TSs["firm_capital_target"].means())
        self.additional_ts["excessive_debt_rate_m"] = ratios(TSs["loans"].sums(), self.additional_ts["targeted_debt_m"])

        ### added at the end for chosen
        #self.additional_ts["exporting_self_financing_ratio_m"] = ratios(TSs["exporting_capital"].sums(), TSs["exporting_assets"].sums())
        #self.additional_ts["exporting_targeted_debt_m"] = differences(TSs["exporting_assets"].sums(), TSs["exporting_capital_target"].sums()) 
        #self.additional_ts["exporting_excessive_debt_rate_m"] = ratios(
        #    TSs["exporting_loans"].sums(), self.additional_ts["exporting_targeted_debt_m"])
        ### 
        
        # hsh hoarding
        self.additional_ts["hoarding_m"] = ratios(TSs["hsh_deposits"].sums(), TSs["hsh_income"].sums(), multiply = 1/12) # defined as in JAMEL
        
        # average unemployment duration
        self.additional_ts["unemployment_duration_y"] = periodize(TSs["unemployed_months_u"].means())
        
        # yearly velocity of money
        self.additional_ts["money_velocity_y"] = ratios(total_income_y, 
                                                        periodize(TSs["deposits"].sums(), cumulation = False, shift = 11)) # divided by december's deposits
        
        # yearly consumption, forced savings
        self.additional_ts["cons_y"] = periodize(TSs["cons"].sums())
        self.additional_ts["mean_cons_y"] = periodize(TSs["cons"].means())
        self.additional_ts["cons_value_y"] = periodize(TSs["cons_value"].sums())
        self.additional_ts["mean_cons_value_y"] = periodize(TSs["cons_value"].means())
        self.additional_ts["forced_savings_rate_m"] = ratios(TSs["forced_savings"].sums(), TSs["budget"].sums())
        self.additional_ts["forced_savings_rate_y"] = ratios(periodize(TSs["forced_savings"].sums()), 
                                                              periodize(TSs["budget"].sums()))
        
        # trade statistics
        bal, exp, imp, exp_r, imp_r, det_exp_r, det_imp_r = trade_stats(TSs)
        self.additional_ts["total_trade_balances_m"] = bal
        self.additional_ts["total_exports_m"] = exp
        self.additional_ts["total_imports_m"] = imp
        self.additional_ts["total_export_rates_m"] = exp_r
        self.additional_ts["total_import_rates_m"] = imp_r
        self.additional_ts["detailed_export_rates_m"] = det_exp_r
        self.additional_ts["detailed_import_rates_m"] = det_imp_r
        
        self.additional_ts["total_trade_balances_y"] = periodize(bal)
        self.additional_ts["total_exports_y"] = periodize(exp)
        self.additional_ts["total_imports_y"] = periodize(imp)
        self.additional_ts["total_export_rates_y"] = ratios(self.additional_ts["total_exports_y"], sales_y )
        self.additional_ts["total_import_rates_y"] = ratios(self.additional_ts["total_imports_y"], self.additional_ts["cons_y"])
        
        # bank bankruptcies
        self.additional_ts["bank_bankruptcies"] = [[bk.bankrupt] for bk in BANKs]
        
        
    def export_data(self, folder = "", note = "", hdf = True, csv = True):   
        """Exports data produced by the simulation to csv file saved in the given folder.
        Folder's name should end with slash (forward slashes are preffered in path names).
        Name of the exported file can be modified with the given note."""
        global no_countries, TSs
        name1 = str(no_countries) + "_" + str(self.seed1) + "_" + str(self.seed2) + "_" + note 
        name2 = name1 + "_additional"
        dataset1 = DF({variable: TSs[variable].data for variable in  TSs})
        #dataset = DF({series.name: series.data for series in list(TSs.values())})
        dataset2 = DF(self.additional_ts)
        seeds = [self.seed1, self.seed2]
        pars = DF(parameters(name1, seeds), index = [""])       # (current) parameters
#        pars["sim_name"] = name1
        
        if hdf:
            store = HDF(folder + name1 + ".h5")                               ## forward slashes seem to be needed in path 
            store["data"] = dataset1
            store["add"] = dataset2
            store["pars"] = pars
            store.close()
            
        if csv:
            dataset1.to_csv(folder + name1 + ".csv")
            dataset2.to_csv(folder + name2 + ".csv")
            pars.to_csv(folder + name1 + "_pars.csv")
        

