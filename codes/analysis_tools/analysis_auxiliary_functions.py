
def find_recs(series, cond = 0.03, percentile = 25, low = None):
    if low is None:
        low = np.percentile(series, percentile)
    ends = []
    starts = []
    depths, lengths = [], []
    i = 0
    ln = len(series)
    while i < ln:
        if series[i] < low:
            start = i
            end = "no"
            while end == "no" and i < (ln-1):
                i += 1
                if series[i] >= low:
                    end = i
            if end == "no":
                end = ln
            
            depth = min(series[start:end])
            if depth < low - cond:
                starts.append(start)
                if end < ln:
                    ends.append(end)
                    depths.append(depth)
                    lengths.append(end - start)
        i += 1
        
    return low, starts, ends, depths, lengths

def BC_synchronization(bc_data1, bc_data2, length = 1380):
    """bc_data = [starts, ends]"""
    series1 = np.zeros(length)
    series2 = np.zeros(length)
    for s, e in zip(*bc_data1):    # identify recessions
        series1[s:e] = 1
    if len(bc_data1[0]) > len(bc_data1[1]):    # if there is recession at the end of simulation
        series1[bc_data1[0][-1]:] = 1
    
    for s, e in zip(*bc_data2):    # identify recessions
        series2[s:e] = 1
    if len(bc_data2[0]) > len(bc_data2[1]):    # if there is recession at the end of simulation
        series2[bc_data2[0][-1]:] = 1
    return (series1, series2), (1-series1, 1-series2)
    #return np.corrcoef(series1, series2)#[0][1]

def round2(value, typ):
    if abs(value) > 2:
        if typ == 1:     # rounding of averages
            return round(value, 1)
        else:           # rounding of stds
            return round(value, 2)
    else:
        if typ == 1:
            return round(value, 4)
        elif typ == 2:
            return round(value, 4)
        else:
            return round(value, 4)

round2_vect = np.vectorize(round2)

def averaging(data_source, variable, subtype = "means", clear = False):
    """Averages time series for a country throughout all the simulations for a country. 
    Assumes the same length of data series."""
    all_mins, all_means, all_maxs, all_stds0, all_stds, all_stds_2 = [], [], [], [], [], []
    for scenario in data_source:
        scen_mins, scen_means, scen_maxs, scen_stds0, scen_stds, scen_stds_2 =  [], [], [], [], [], []
        if subtype == "data":
            no_countries = len(scenario[0][variable])
        elif subtype == "means":
            no_countries = len(scenario[0][variable].means())
        elif subtype == "sums":
            no_countries = len(scenario[0][variable].sums())
        for country in range(no_countries):
            means = []
            stds = []
            for sim in scenario:
                if subtype == "data":
                    data = sim[variable][country]
                elif subtype == "means":
                    data = sim[variable].means()[country]
                elif subtype == "sums":
                    data = sim[variable].sums()[country]
                    
                if clear:
                    data = [x for x in data if x is not None]
                means.append(np.mean(data))                 # same length - mean of averages will be the same as the overall average
                stds.append(np.std(data)) # will take average of individual simulation stds
            scen_mins.append(round2(min(means),1))
            scen_means.append(round2(np.mean(means),1))
            scen_maxs.append(round2(max(means),1))
            scen_stds0.append(round2(np.std(means),2))      # std of averages
            scen_stds.append(round2(np.mean(stds),2))       # average of stds
            scen_stds_2.append(round2(np.std(stds),3))      # std of stds
        all_mins.append(scen_mins)
        all_means.append(scen_means)
        all_maxs.append(scen_maxs)
        all_stds0.append(scen_stds0)
        all_stds.append(scen_stds)
        all_stds_2.append(scen_stds_2)
        
    return all_mins, all_means, all_maxs, all_stds0, all_stds, all_stds_2

def create_folder(path, trial = 0):
    if "os" not in globals():
        global os
        import os
    path2 = path
    if trial > 99:
        print("too many iterations")
        return None
    path2 += "_" + str(trial)
    try:
        os.mkdir(path2)
        return path2
    except:
        return create_folder(path, trial+1)

def markers(starts, ends, low, length = 1380, y_lim = 0.6):
    series = np.empty(length)
    series[:] = np.NaN
    if starts == []:
        return series
    series[starts] = low
    series[np.array(starts) + 1] = y_lim
    if ends == []:
        return series
    series[ends] = low
    series[np.array(ends)-1] = y_lim
    return series


def choose(starts, ends, indeces):
    i, j = indeces
    if len(ends[0]) <= i or len(ends[1]) <= j:
        return "finished", 0, 1
    
    if starts[0][i] > starts[1][j]:
        curr_end = ends[1][j]
        first_cc = 1
        second_cc = 0
    else:
        curr_end = ends[0][i]
        first_cc = 0
        second_cc = 1
    return curr_end, first_cc, second_cc


def connect_alg(starts, ends):
    st_1, st_2 = starts
    ends_1, ends_2 = ends
    if len(ends_1) == 0 or len(ends_2) == 0:
        return [[]]*2
    
    indeces = [0,0]
    crises = [[], []]
    
    curr_end, first_cc, second_cc = choose(starts, ends, indeces)
    
    if curr_end == "finished":
        cont = False
    else:
        cont = True
    curr_crisis = [[],[]]
    
    while cont:
        if curr_end > starts[second_cc][indeces[second_cc]]:   # crises are intersecting
            a, b = indeces
            if len(ends_1) <= a or len(ends_2) <= b:
                
                break
            curr_crisis[0].append(a)
            curr_crisis[1].append(b)
            
                        
            if ends[second_cc][indeces[second_cc]] > curr_end:  # current end shifts to second country
                curr_end = ends[second_cc][indeces[second_cc]]
                indeces[first_cc] += 1
                first_cc, second_cc = second_cc, first_cc
                
            else:                # crisis in second country is inside the first crisis
                indeces[second_cc] += 1
            
            cont = True
        
        else:                 # crises are not intersecting (anymore), we have finished global crisis
            
            indeces[first_cc] += 1
            
            curr_end, first_cc, second_cc = choose(starts, ends, indeces)
            crises[0].append(list(set(curr_crisis[0])))
            crises[1].append(list(set(curr_crisis[1])))
            curr_crisis = [[],[]] 
            cont = True
        
        if curr_end == "finished":
            cont = False
        a, b = indeces
        if len(st_1) <= a or len(st_2) <= b:       # nothing more to compare
            crises[0].append(list(set(curr_crisis[0])))
            crises[1].append(list(set(curr_crisis[1])))
            cont = False
            
    return crises
    
class crisis:
    
    def __init__(self, empl_data_c0, empl_data_c1):
        """Creates global crisis data for an individual simulation."""
        starts = [empl_data_c0[1].copy(), empl_data_c1[1].copy()]
        ends = [empl_data_c0[2].copy(), empl_data_c1[2].copy()]
        depths = [empl_data_c0[3].copy(), empl_data_c1[3].copy()]
        lengths= [empl_data_c0[4].copy(), empl_data_c1[4].copy()]
        
        crisis_indeces = connect_alg(starts, ends)
        
        first_countries = []       # which country is first in recession
        union_periods = []         # at least one country in crises
        union_lengths = []
        #intersection_periods = []  # both countries in crisis
        intersection_lengths = []
        first_depths, first_lengths  = [], []
        second_depths, second_lengths = [], []
        contained_crises = len(ends[0] + ends[1])
        
        for inds_0, inds_1 in zip(*crisis_indeces):
            if len(inds_0) == 0 or len(inds_1) == 0:
                continue
            i, j = inds_0[0], inds_1[0]
            if starts[0][i] <= starts[1][j]:
                first_cc = 0
                second_cc = 1
                first_indeces = inds_0
                second_indeces = inds_1
                overall_start = starts[0][i]
            else:
                first_cc = 1
                second_cc = 0
                first_indeces = inds_1
                second_indeces = inds_0
                overall_start = starts[1][j]
            first_countries.append(first_cc)
            overall_end = max(ends[0][inds_0[-1]], ends[1][inds_1[-1]])
            union_periods.append((overall_start, overall_end))
            union_lengths.append(overall_end - overall_start)
            
            first_depths.append(min([depths[first_cc][ii] for ii in first_indeces]))
            second_depths.append(min([depths[second_cc][ii] for ii in second_indeces]))
            first_lengths.append(sum(lengths[first_cc][ii] for ii in first_indeces))
            second_lengths.append(sum(lengths[second_cc][ii] for ii in second_indeces))
            
            inter_l = first_lengths[-1] + second_lengths[-1] - union_lengths[-1]
            intersection_lengths.append(inter_l)
            
            contained_crises -= len(inds_0+inds_1)
            
        self.first_countries = first_countries
        self.no_global_crises = len(first_countries)
        self.union_periods = union_periods
        self.union_lengths = union_lengths
        #self.intersection_periods = intersection_periods
        self.intersection_lengths = intersection_lengths
        self.depths = (first_depths, second_depths)
        self.lengths = (first_lengths, second_lengths)
        self.contained_crises = contained_crises 
        
        self.no_global_crises_0 = len([i for i in self.first_countries if i == 0])
        self.no_global_crises_1 = len([i for i in self.first_countries if i == 1])
        self.union_periods_0 = [union_periods[i] for i in range(self.no_global_crises) if self.first_countries[i] == 0]
        self.union_periods_1 = [union_periods[i] for i in range(self.no_global_crises) if self.first_countries[i] == 1]
        self.union_lengths_0 = [union_lengths[i] for i in range(self.no_global_crises) if self.first_countries[i] == 0]
        self.union_lengths_1 = [union_lengths[i] for i in range(self.no_global_crises) if self.first_countries[i] == 1]
        #self.intersection_periods = intersection_periods
        self.intersection_lengths_0 = [intersection_lengths[i] for i in range(self.no_global_crises) if self.first_countries[i] == 0]
        self.intersection_lengths_1 = [intersection_lengths[i] for i in range(self.no_global_crises) if self.first_countries[i] == 1]
        self.depths_0 = ([self.depths[0][i] for i in range(self.no_global_crises) if self.first_countries[i] == 0],
                         [self.depths[1][i] for i in range(self.no_global_crises) if self.first_countries[i] == 0])
        self.depths_1 = ([self.depths[0][i] for i in range(self.no_global_crises) if self.first_countries[i] == 1],
                         [self.depths[1][i] for i in range(self.no_global_crises) if self.first_countries[i] == 1])
        self.lengths_0 = ([self.lengths[0][i] for i in range(self.no_global_crises) if self.first_countries[i] == 0],
                          [self.lengths[1][i] for i in range(self.no_global_crises) if self.first_countries[i] == 0])
        self.lengths_1 = ([self.lengths[0][i] for i in range(self.no_global_crises) if self.first_countries[i] == 1],
                          [self.lengths[1][i] for i in range(self.no_global_crises) if self.first_countries[i] == 1])
    
    def show(self):
        attrs = { 
            "first_cc": self.first_countries,
            "union_periods": self.union_periods,
            "union_lengths": self.union_lengths,
            #"": self.intersection_periods,
            "intersection_lengths": self.intersection_lengths,
            "depths": self.depths,
            "lengths": self.lengths,
            "no_of_global_crises": self.no_global_crises,
            "no_of_contained_crises": self.contained_crises
        }
        return attrs
        

def cut_2(series, starts, ends, period_data = False):
    from copy import deepcopy
    new_s = deepcopy(series)
    if not period_data:        # simply subsetting from a list of series
        no_c = len(series)      # no of countries
        for i in range(no_c):
            for st, en in zip(starts[i], ends[i]):
                if en is None:
                    en = len(series[i])
                try:
                    new_s[i][st:en] = [None]*(en-st)
                except:
                    new_s = [list(ss) for ss in new_s]
                    new_s[i][st:en] = [None]*(en-st)
    else:             # subsetting from pairs or more
        no_c = len(series[0])      # no of countries
        #no_v = len(series[0][0])   # no of statistics in series
        if isinstance(new_s[0][0], np.ndarray):
            for per, junk in enumerate(new_s):
                new_s[per] = list(new_s[per])
                for ii, jj in enumerate(junk):
                    new_s[per][ii] = list(new_s[per][ii])
        for i in range(no_c):
            if isinstance(new_s[0][i], list): #or isinstance(new_s[0][i], np.ndarray):
                for st, en in zip(starts[i], ends[i]): 
                    for j, period_point in enumerate(new_s[st:en]):
                        new_s[st:en][j][i] = [None]*len(period_point[i]) 
            else:
                for st, en in zip(starts[i], ends[i]): 
                    for j, period_point in enumerate(new_s[st:en]):
                        new_s[st:en][j][i] = None
                    
    return new_s


def cut_dict_2(*data_dicts, starts, ends, crises = True, variables = "all"):
    """Subsets either stability or crises periods from chosen time series in each data dictionary."""
    from copy import deepcopy
    result = []
    for i, data_dict in enumerate(data_dicts):
        if crises:
            curr_starts = [[0] + ee for ee in ends[i]]
            curr_ends = [st + [None] for st in starts[i]]
        else:
            curr_starts = starts[i]
            curr_ends = ends[i]
        new_dict = {}
        if variables == "all":
            variables = list(data_dict.keys())
        for key in variables:
            if key == "bank_bankruptcies":
                new_dict[key] = deepcopy(data_dict[key])
                continue
            #print(key)
            if key[-2:] == "_y":             # for yearly data
                try:
                    x = data_dict[key].data  # testing if it has data attribute
                    new_dict[key] = deepcopy(data_dict[key])
                    now_starts = [int(st/12) for st in curr_starts]
                    now_ends = [int(en/12) for en in curr_ends if en is not None] + [None]
                    new_dict[key].data = cut_2(new_dict[key].data, now_starts, now_ends, period_data = 1)
                except:
                    now_starts = [[int(st/12) for st in substarts] for substarts in curr_starts]
                    now_ends = [[int(en/12) for en in subends if en is not None] + [None] for subends in curr_ends]
                    new_dict[key] = cut_2(data_dict[key], now_starts, now_ends, period_data = 0)
            
            else:                           # for the rest, ie monthly data
                try:
                    x = data_dict[key].data  # testing if it has data attribute
                    new_dict[key] = deepcopy(data_dict[key])
                    new_dict[key].data = cut_2(new_dict[key].data, curr_starts, curr_ends, period_data = 1)
                except:
                    new_dict[key] = cut_2(data_dict[key], curr_starts, curr_ends, period_data = 0)
        result.append(new_dict)
    return result




def concat_lat(lats, descrpits, measure = None, country = None, kind = 0):
    lat = lats[0]
    if kind == 0:                          # for averages data
        final = lat[:lat.find("country 0")]
    elif kind == 1:                                  # for recessions data
        final = lat[:lat.find(str(measure) + " C" + str(country))]
    else:
        final = lat[:lat.find(str(measure))]
    for lat, des in zip(lats, descrpits):
        ii = final.find("end{tabular}") - 1
        if ii > 0:
            final = final[:ii]
        if kind == 0:
            final += des + " & & & & & & \\\\\n "
        else:
            final += des + " & & & & & \\\\\n "
        
        jj = lat.find("\midrule")
        final += lat[jj:]
    return final

def add_label(table, label):
    ii = table.find("\\end{table}")
    label = label.replace("\\", " ")
    label = label.replace("_", " ")
    final = table[:ii] + "\label{tab:" + label + "}\n" + table[ii:]
    return final

