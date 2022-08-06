
def experiment(rand_seeds, periods, note, hdf = True, csv = True):
    for seeds in rand_seeds:
        aa = Simulation(seeds[0], seeds[1])
        aa.run(periods)  
        aa.finalize_data()
        aa.export_data(note = note, hdf = hdf, csv = csv)


# exp_grid function

# In[36]:


def exp_grid(grid, parameters, rand_seeds, periods, note, start = 0, hdf = True, csv = True, notify = True):
    """Performs experiments for given grid of parameter values."""
    global model_tools
    if notify:
        print("start of exp_grid:", note)
    for i, value in enumerate(grid):
        if i < start:                 # when we need to finish what was already in progress
            continue
        for j, par in enumerate(parameters):    # set parameters for the current experiment
#            setattr(model_tools, par, value[j])
            globals()[par] = value[j] 
        curr_note = note + "_" + str(i+1)             # number them from 1
        experiment(rand_seeds, periods, curr_note, hdf, csv)
        if notify:
            print("experiment", i, "is finished")
    if notify:
        print("end of exp_grid:", note)


# make_grid function

# In[37]:


def make_grid(*values_list):
    """Creates grid of values. 
    Each input should be a complete set of parameter options. An item in such set should be a list."""
    from itertools import product
    grid = []
    list_of_sqaures = list(product( *values_list))
    for sqaure in list_of_sqaures:
        new = []
        [new.extend(pars) for pars in sqaure]
        grid.append(new)
    return grid


# make_matrix function

# In[38]:


def make_matrix(quota, costs = False):
    """Makes a matrix with 1 or 0 on diagonal and quota everywhere else."""
    global no_countries
    quotas = np.array([[quota]*no_countries]*no_countries)                                     
    if costs:
        np.fill_diagonal(quotas, [0]*no_countries)  # trade costs
        return quotas             # as np array
    else:
        np.fill_diagonal(quotas, [1]*no_countries)  # trade quotas
        return [list(country) for country in quotas] 


# time_exp function

# In[39]:


def time_exp(periods = 5, repeats = 5):
    import time
    times = []
    s = Simulation()
    for rep in range(repeats):
        tic = time.perf_counter()
        s.run(periods)
        toc = time.perf_counter()
        times.append(toc-tic)
    print(sum(times)/repeats)


# set_base_pars function

# In[40]:


def set_base_pars(no_hshs = None):
    """Sets all experiment-dependend parameters to base levels."""
    global ns, ms, global_bank, transport_firms, no_countries, wage_resist, wage_flex
    global trade_costs, free_market, trade_quotas, pegged_rates, trade_sensitivity, normal_variance, providers, p, p2
    
    if no_hshs is not None:         # leave unchanged by default
        ns = no_hshs
        ms = [int(11*n/100) for n in no_hshs]
    global_bank = False
    transport_firms = 2                                        ##################################
    no_countries = len(ns)
    
    wage_resist = [12]*no_countries           
    wage_flex = [0.05]*no_countries             
    
    trade_costs = make_matrix(0.2, True)                      
    
    free_market = True                
    trade_quotas = make_matrix(1)
    
    pegged_rates = [-1]*no_countries     
    
    trade_sensitivity = 0.1         
    normal_variance = 0.002
    
    if no_countries == 2:
        providers = 15          
    elif no_countries == 6:
        providers = 30                
    else:
        providers = 10
        
    p = 0.7
    p2 = 0.7

