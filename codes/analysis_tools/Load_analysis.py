
class Load_analysis:
    def __init__(self, no_countries, name, last, first = 1, cut_start = 120, cut_end = None,
                scenario_names = None, limit = None, variables = "all"):
        """name, scenario_names as string; others as integers"""
        
        nn = name.split("_")
        nn.remove("final")
        self.name = " ".join(nn)
        self.first = first
        self.last = last
        self.cut_start = cut_start
        self.cut_end = cut_end
                
        self.data_list = []
        self.pars_list = []
        self.files_list = []
        for s in range(first, last):
            path = str(no_countries) + "*" + name + str(s) + '.h5'
            dat, fil, par = load_hdf(path, condition = None,  ret_parameters = True, limit = limit, variables = variables)
            for sim in dat:
                try:
                    sim["real_trade_fees"] = ratios(sim["spec_trade_fees"].sums(), sim["price_level_m"])  # add real trade fees
                except:
                    pass
            self.data_list.append(cut_dict(*dat, start = cut_start, end = cut_end))
            self.pars_list.append(par)
            self.files_list.append(fil)
            
        try:
            self.firsts = [scenario[0] for scenario in self.data_list]
        except:   # when creating empty load object
            self.firsts = []
        self.no_scens = len(self.data_list)
        self.no_countries = [no_countries]*self.no_scens
        if scenario_names is None:
            self.scenario_names = [str(i) for i in range(self.no_scens)]
        else:
            self.scenario_names = scenario_names
