
def good_sum(data):
    """Corrected against overflowing."""
    return np.sum(data, dtype = np.float)

def good_mean(data):
    """Corrected against overflowing."""
    return np.mean(data, dtype = np.float)

def good_min(data):
    """Corrected against empty data."""
    try:
        l = len(data)
    except:
        return np.min(data)
    if l == 0:
        return np.nan
    else:
        return np.min(data)
    
def good_max(data):
    """Corrected against empty data."""
    try:
        l = len(data)
    except:
        return np.max(data)
    if l == 0:
        return np.nan
    else:
        return np.max(data)


# In[17]:


def collect_data(agent, variable, summary_stats = True, customized_list_f = None):
    """Collects cross-sectional data from individual agents."""                  ## could be as method in TS
    if customized_list_f is not None:
            list_of_agents = customized_list_f()    # applying function which returns list of chosen agents
    elif agent == "H" or agent == "Hacc":         # HSHs or HSH accounts
        global HSHs
        list_of_agents = HSHs
    elif agent == "F" or agent == "Facc":         # firms or firm accounts
        global FIRMs
        list_of_agents = FIRMs
    else:                                         # banks
        global BANKs
        data = [getattr(bank, variable) for bank in BANKs]   
    
    if agent == "Hacc" or agent == "Facc":        # bank accounts variables
        data = [np.array([getattr(agent.account, variable) for agent in country]) for country in list_of_agents]
    elif agent == "H" or agent == "F":            # agents' variables
        data = [np.array([getattr(agent, variable) for agent in country]) for country in list_of_agents]
    
    if summary_stats:
##        functions = [np.sum, np.mean, np.min, np.median, np.max, np.std]
        functions = [good_sum, good_mean, good_min, np.median, good_max, np.std]
        stats = [[round(fun(country), 3) for fun in functions] for country in data] 
        return stats
    else:                      # only sum and average
        return [[good_sum(country), round(good_mean(country), 3)]  for country in data]
        
