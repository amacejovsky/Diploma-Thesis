# parameters
# overall
no_countries = 2
ns = [5000,5000]              # no HSHs
ms = [550,550]                # no firms
global_bank = False           # just one bank for the whole world?

# HSHs
wage_resist = [12]*no_countries  # wage resistance in unemployment; 12 in baseline, 8 in alternative
wage_flex = [0.05]*no_countries  # wage flexibility;                0.05 in baseline, 0.08 or 0.25 in alternative
prop_to_save_O = 0.15        # optimistic saving target
prop_to_save_P = 0.2         # pessimistic saving target
cons_of_excess_savings = 0.5 # rate of cons. of excess savings
l_providers = 10             # number of firms to be considered on labor market 

# firms
K = 10                # no of machines
productivity = 100    # machine productivity

production_time = 8           # length of production
inv_normal = 2                # periods of full prod. for targeted inventories
price_flex = 0.05             # adjustment parameter
#d_p = random.randrange(1,4)  # price rigidity;  for a firm, drawn after each price change 
targeted_vacancies = 0.03     # targeted vacancies 
#d_w_e = random.randrange(6,18) # length of employment constracts - drawn for each new contract separately
mu_F = 0.5                    # goods to be sold
capital_normal_ratio = 0.2    # optimisstic targeted net wealth
capital_high_ratio = 0.5      # pessimistic targeted net wealth
sales_normal_ratio = 0.83     # targeted sales - to use for sentiment; in paper it is 0.85
#t_f = random.randrange(12,36) # regeneration time after bankruptcy; drawn anew for each bankruptcy
in_T = inv_normal*K*productivity # targeted inventories

#util_rate = random.randrange(50,100)   # initial targeted utilization rate of machinery for a firm; drawn for each firm at creation
util_flex = 10                # flexibility (adjustment) of utilization rate

wage_flex_up = 0.06       # firms' upward wage flexibility  
wage_flex_down = 0.09     # firms' downward wage flexibility

# bank
r = 0.05           # normal interest rate
r_ = 0.1           # premium interest rate
normal_length = 12      # normal credit length
extended_length = 12    # extended credit length
kappa_B = 0.085         # targeted capital;   in the paper it is 0.1

# opinion
p = 0.7     # animal spirits, firms
p2 = 0.7    # animal spirits, households
h = 3       # size of neighbourhood



# international trade parameters
pegged_rates = [-1]*no_countries     # which currencies are pegged together, -1 if to none
trade_sensitivity = 0.1              # sensitivity in exchange factors updating    ## gamma
normal_variance = 0.002

trade_costs = np.array([[0.05]*no_countries]*no_countries)                         ## tau
np.fill_diagonal(trade_costs, [0]*no_countries)                              ## keep as np array 

free_market = True                 # all quotas are 1?
trade_quotas = np.array([[1]*no_countries]*no_countries)                                  
np.fill_diagonal(trade_quotas, [1]*no_countries) 
trade_quotas = [list(country) for country in trade_quotas]                   ## quicker to have it as list

if no_countries == 2:
    providers = 15                 # market selection - no of firms considered by each hsh on goods market
elif no_countries == 6:
    providers = 30                
else:
    providers = 10

transport_firms = 2    # trade costs are distributed to: 0 for nowhere, 1 for exporting country, 2 for importing country, 3 for 50:50



def parameters(name = None, seeds = None):
    """Returns dictionary with the current parameter values."""
    global period
    try:
        pp = period
    except:
        pp = -1                                        # if period is not defined yet
    return {"name": str(name) , "random_seeds": str(seeds),
            "period": "current period = " + str(pp), 
            "no_countries": "number of countries = " + str(no_countries),        
            "global_bank": "if there is only 1 global bank = " + str(global_bank),
            "ns": "number of HSHs = " + str(ns),                               
            "ms": "number of firms = " + str(ms),
                            
            "wage_resist": "hsh - wage resistance in unemployment = " + str(wage_resist),  
            "wage_flex": "hsh - wage flexibility = " + str(wage_flex),
            "prop_to_save_O": "hsh - optimistic saving target = " + str(prop_to_save_O), 
            "prop_to_save_P": "hsh - pessimistic saving target = " + str(prop_to_save_P),
            "cons_of_excess_savings": "hsh - rate of cons. of excess savings = " + str(cons_of_excess_savings),    
            "l_providers": "hsh - number of firms to be considered on labor market = " + str(l_providers),
            "providers": "hsh - number of firms to be considered on goods market = " + str(providers),
            
            "K": "f - number of machines = " + str(K),                         
            "productivity": "f - machine productivity = " + str(productivity),   
            "production_time": "f - length of production = " +str(production_time),                    
            "inv_normal": "f - periods of full prod. for targeted inventories = " + str(inv_normal),
            "price_flex": "f - adjustment parameter = " + str(price_flex),       
            "targeted_vacancies": "f - targeted rate of vacancies = " + str(targeted_vacancies),            
            "mu_F": "f - portion of goods to be sold = " + str(mu_F),          
            "capital_normal_ratio": "f - optimisstic targeted net wealth = " + str(capital_normal_ratio),
            "capital_high_ratio": "f - pessimistic targeted net wealth = " + str(capital_high_ratio), 
            "sales_normal_ratio": "f - targeted sales = " + str(sales_normal_ratio),
            "in_T": "f - targeted inventories = inv_normal*K*productivity = " + str(in_T), 
            "util_flex": "f - flexibility of utilization rate = " + str(util_flex),
            "wage_flex_up": "f - upward wage flexibility = " + str(wage_flex_up), 
            "wage_flex_down": "f - downward wage flexibility = " + str(wage_flex_down),
            
            "r": "B - standard interest rate = " + str(r),                     
            "r_": "B - premium interest rate = " + str(r_),
            "normal_length": "B - credit length of repayment = " + str(normal_length), 
            "extended_length": "B - extended length of repayment = " + str(extended_length),
            "kappa_B": "B - targeted capital = " + str(kappa_B),
            
            "p": "f - opinion model - strength of animal spirits = " + str(p),
            "p2": "hsh - opinion model - strength of animal spirits = " + str(p2), 
            "h": "opinion model - size of neighbourhood = " + str(h),
                        
            "trade_sensitivity": "sensitivity of exchange factors = " + str(trade_sensitivity), 
            "normal_variance": "variance parameter for random exchange rates factors = " + str(normal_variance),
            "trade_costs": "costs of trade from country i to country j = " + str(trade_costs), 
            "trade_quotas": "proportion of firms from country j allowed to sell in country i = " + str(trade_quotas),
            "free_market": "whether can all firms participate in all goods markets = " + str(free_market), 
            "pegged_rates": " which currencies are pegged together, -1 if to none = " + str(pegged_rates),
            "transport_firms": "to where are trade costs distributed = " + str(transport_firms)
            }
    
