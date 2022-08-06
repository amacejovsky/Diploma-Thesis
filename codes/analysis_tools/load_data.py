
def load_hdf(path, condition = None, ret_parameters = True, limit = None, variables = "all"):
    """From given path loads every h5 file and returns dictionary of time series and TS objects."""
    import glob
    import pandas as pd
    
    def assign_TS(df, col):
        """Stores data in either TS or Spec_TS objects."""
        if col[:5] == "spec_":
            ts = Special_TS(col)                                                                                 #####
            ts.variable = col[5:]                          ## remove "spec_" from name so sums() method works properly
            ts.data = list(df[col])
            return ts
        ts = TS("someone", col, True)
        ts.name = col
        ts.data = list(df[col])
        return ts
    
    files = glob.glob(path)
    if condition is not None:         # dont load files which fulfill condition
        files_to_remove = []
        for item in files:
            if condition(item):
                files_to_remove.append(item)
        [files.remove(item) for item in files_to_remove]
    
    files = files[:limit]
    data = []
    parameters = []
    for index, file in enumerate(files):
        store = pd.HDFStore(file)
        dataset1 = store["data"] 
        dataset2 = store["add"]
        if ret_parameters:
            pars = store["pars"]
            parameters.append({col: list(pars[col]) for col in pars.columns})
        store.close()
        if variables == "all":
            variables1 = dataset1.columns
            variables2 = dataset2.columns
        else:
            variables1 = [var for var in variables if var in dataset1.columns] + ["employment"]
            variables2 = [var for var in variables if var in dataset2.columns] + ["bank_bankruptcies"]
        TSs = [assign_TS(dataset1, col) for col in variables1]      # makes time series objects
        data_dict1 = {ts.name: ts for ts in TSs}
        data_dict2 = {col: list(dataset2[col]) for col in variables2}
        try:
            data_dict2["production_y"] = periodize(data_dict1["production"].sums())
        except:
            pass
        data.append({**data_dict1, **data_dict2})               # return data in dictionary format
        
    if ret_parameters:
        return data, files, parameters
    else:
        return data, files

# load_data function


def load_data(path, condition = None, ret_parameters = False):
    """From given path loads every csv data file and returns lists of time series objects."""
    import glob
    import os
    import pandas as pd
    import json
    import re
    import ast
    
    
    def adjust_nans(cell):
        """Adjust NaNs so they are readable by json.loads."""
        return re.sub(r'\bnan\b', 'NaN', cell)

    def get_rid_of_inf(cell):
        """Deals with numpy "inf"."""
        ee = re.sub('inf','0 ',cell)
        return json.loads(ee)
    
    def adjust_arrays(cell):
        """Converts strings of numpy arrays to lists."""
        rr = re.sub('array\(',' ',cell)
        return json.loads(re.sub('\)',' ',rr))
    
    def adjust_more1(cell):
        """Replaces blank spaces with commas, coverts string to list."""
        ee = re.sub('\s+',', ',cell) 
        return ast.literal_eval(re.sub("\[,", "[", ee))
    
    def adjust_more2(cell):
        """Replaces blank spaces with commas while keeping correct list syntax."""
        ee = re.sub('\s+',', ',cell) 
        ee = re.sub(', ]',']',ee) 
        return ast.literal_eval(ee)
    
    def assign_TS2(df, col):
        """Stores data in either TS or Spec_TS objects."""
        if col[:5] == "spec_":
            ts = Special_TS(col[5:])               ## remove "spec_" from name so sums() method works properly
            ts.data = list(df[col])
            return ts
        ts = TS("someone", col, True)
        ts.name = col
        ts.data = list(df[col])
        return ts
    
    files = glob.glob(path)
    
    if condition is not None:         # dont load files which fulfill condition
        files_to_remove = []
        for item in files:
            if condition(item):
                files_to_remove.append(item)
        [files.remove(item) for item in files_to_remove]
    par_files_paths = [file[:-4] + "_pars.csv" for file in files]  
    par_files = [glob.glob(par_path) for par_path in par_files_paths]         # files with parameters
    
    data = []
    bad_columns = [[] for file in files]
    for index, file in enumerate(files):        
        df = pd.read_csv(file)           
        df.drop(df.columns[0], axis=1, inplace=True)  # first column are just periods
        df = df.applymap(adjust_nans)                 # makes NaNs readable
        try:
            df = df.applymap(json.loads)     # converts "stringed" lists back to lists
        except:
            for col in df.columns:
                if col == "excessive_debt_rate_m":
                    df[col] = df[col].apply(get_rid_of_inf)
                elif col == "spec_export_details":
                    df[col] = df[col].apply(adjust_more1)
                elif col in ("spec_import_details", "spec_trade_balances"):
                    df[col] = df[col].apply(adjust_arrays)
                else:
                    try:
                        df[col] = df[col].apply(json.loads)
                    except:
                        try:
                            df[col] = df[col].apply(adjust_more2)
                        except:
                            bad_columns[index].append(col)
        TSs = [assign_TS2(df, col) for col in df.columns]      # makes time series objects
        data.append({ts.name: ts for ts in TSs})               # return data in dictionary format
    if bad_columns != [[] for file in files]:
        print("There are bad columns!")
    
    if ret_parameters:
        parameters = []
        for file in par_files:
            if file == []:
                continue
            pars = pd.read_csv(file[0]) 
            pars.drop(pars.columns[0], axis=1, inplace=True)  # first column is nonsense
            parameters.append({col: list(pars[col]) for col in pars.columns})
        return data, bad_columns, files, parameters
    return data, bad_columns, files

