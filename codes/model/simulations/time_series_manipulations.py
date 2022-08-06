
def periodize(series, cumulation = True, averaging = False, perioda = 12, shift = 0):
    """Decreases frequency of the data or accumulates over given period."""
    results = []
    for country in series:
        if cumulation:
            end = len(country) - 11 - shift
            if averaging:
                res = [sum(country[shift+i:(shift+i+perioda)])/perioda for i in range(0,end,perioda)] # take only full years
            else:
                res = [sum(country[shift+i:(shift+i+perioda)]) for i in range(0,end,perioda)]         # take only full years
            results.append(res)
        else:
            if averaging:
                results.append(list(np.array(country[shift::perioda])/12))
            else:
                results.append(country[shift::perioda])
    return results


# growths function

# In[29]:


def growths(series, rate = True, add_zero = False):
    """Returns time series of growth or growth rates."""
    results = []
    for country in series:
        s1 = np.array(country[:-1])    # t-1
        s2 = np.array(country[1:])     # t
        diff = s2 - s1
        if rate:
            if add_zero:
                results.append([0] + list(diff/s1))
            else:
                results.append(list(diff/s1))
        else:
            if add_zero:
                results.append([0] + list(diff))
            else:
                results.append(list(diff))
    return results


# differences function

# In[30]:


def differences(series1 = "ones", series2 = None, relative = False, reverse = False):
    """Returns simple or relative differences or sums of two sets of time series."""
    results = []
    if series1 == "ones":           # to make inverse ratio, eg employment -> unemployment
        series1 = [[1 for i in range(len(series2[0]))] for j in range(len(series2))]
    for country_s1, country_s2 in zip(series1, series2):   # iterate over countries
        incon = len(country_s1) - len(country_s2)     # if we compare growth series with normal one there is difference in length
        if incon == 0:
            s1, s2 = np.array(country_s1), np.array(country_s2)
        else:
            s1, s2 = (np.array(country_s1[1:]), np.array(country_s2)) if incon > 0 else (np.array(country_s1), np.array(country_s2[1:]))
        if reverse:       # sum, actually
            diff = s1 + s2
        else:
            diff = s1 - s2
        if relative:
            results.append(list(diff/s1))
        else: 
            results.append(list(diff))
    return results


# ratios function

# In[31]:


def ratios(series1, series2, multiply = 1, constants = False):
    """Returns ratios of two sets of time series"""
    results = []
    if constants:
        series2 = [np.full([1, len(series1[i])], series2[i])[0] for i in range(len(series1))]
    for country_s1, country_s2 in zip(series1, series2):   # iterate over countries
##        incon = len(country_s1) - len(country_s2)     # if we compare growth series with normal one there is difference in length
##        if incon == 0:
        s1, s2 = np.array(country_s1), np.array(country_s2)
##        else:
##            s1, s2 = (np.array(country_s1[1:]), np.array(country_s2)) if incon > 0 else (np.array(country_s1), np.array(country_s2[1:]))
        results.append(list(multiply*s1/s2))
    return results


# trade_stats function

# In[32]:


def trade_stats(data_dict): 
    """Calculates total trade balances, relative trade volumes."""
    no_cc = len(data_dict["spec_trade_balances"].data[0])    # number of countries
    if no_cc == 1:                  # 1 country model
        global period
        return [[[0]*(period+1)]]*5 + [[[1]*(period+1)]]*2
    
    total_balances_ts = [np.sum(data_dict["spec_trade_balances"].sums(cc), axis = 0) for cc in range(no_cc)]
    
    total_exports_ts = []
    total_imports_ts = []
    for cc in range(no_cc):
        foreign_exports = [series for i, series in enumerate(data_dict["spec_export_details"].sums(cc)) if cc != i]
        total_exports_ts.append(np.sum(foreign_exports, axis = 0))    # foreign exports, excluding domestic sales
        foreign_imports = [series for i, series in enumerate(data_dict["spec_import_details"].sums(cc)) if cc != i]
        total_imports_ts.append(np.sum(foreign_imports, axis = 0))    # foreign imports, excluding domestic consumption
    
    export_rates = ratios(total_exports_ts, data_dict["sales"].sums())   # total foreign exports to sales
    import_rates = ratios(total_imports_ts, data_dict["cons"].sums())    # total foreign imports to consumption
    
    detailed_export_rates = [[ratios([data_dict["spec_export_details"].sums(cc)[i]], [data_dict["sales"].sums()[cc]]) for i in range(no_cc)] for cc in range(no_cc)]
    detailed_export_rates = [[details[0] for details in country] for country in detailed_export_rates]  # concatenating
    detailed_import_rates = [[ratios([data_dict["spec_import_details"].sums(cc)[i]], [data_dict["cons"].sums()[cc]]) for i in range(no_cc)] for cc in range(no_cc)]
    detailed_import_rates = [[details[0] for details in country] for country in detailed_import_rates]  # concatenating
    
    return total_balances_ts, total_exports_ts, total_imports_ts, export_rates, import_rates, detailed_export_rates, detailed_import_rates

    
def y_to_m(series, final_length = 1380):
    """Prepares yearly data for being plotted againts monthly data."""
    final_series = []
    lin = np.arange(12)
    for s in series:
        final_s = np.empty(final_length)
        final_s[:] = np.nan
        for i, point in enumerate(s[:-1]):
            final_s[12*(i+1):12*(i+2)] = point + (s[i+1] - point)*lin/12
        
        final_series.append(list(final_s))
    return final_series


# cut function
def cut(series, start = 0, end = None):
    """Cuts off the ends of time series."""
    return [s[start:end] for s in series]

# cut_dict function
def cut_dict(*data_dicts, start = 0, end = None):
    """Cuts the ends of each time series in each data dictionary."""
    from copy import deepcopy
    result = []
    for data_dict in data_dicts:
        new_dict = {}
        for key in data_dict.keys():
            if key == "bank_bankruptcies":
                new_dict[key] = deepcopy(data_dict[key])
                continue
            if key[-2:] == "_y":             # for yearly data
                try:
                    x = data_dict[key].data  # testing if it has data attribute
                    new_dict[key] = deepcopy(data_dict[key])
                    y_end = None if end is None else int(end/12)
                    new_dict[key].data = new_dict[key].data[int(start/12):y_end]
                except:
                    y_end = None if end is None else int(end/12)
                    new_dict[key] = cut(data_dict[key], int(start/12), y_end)
            
            else:                           # for the rest, ie monthly data
                try:
                    x = data_dict[key].data  # testing if it has data attribute
                    new_dict[key] = deepcopy(data_dict[key])
                    new_dict[key].data = new_dict[key].data[start:end]
                except:
                    new_dict[key] = cut(data_dict[key], start, end)
        result.append(new_dict)
    return result


