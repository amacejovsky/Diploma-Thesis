
class Visual:
    
    def plot(series, 
             marker = "-", size = (10,4),  
             x_label = "period", y_label = "value", 
             title = "Plot", legend = None,
             zipping = True,
            grid = True,
            path = None):
        """Plots multiple time series."""
        if zipping:
            ys = list(zip(*series))
        else:
            ys = series
        plt.rcParams["figure.figsize"] = size
        plt.plot(ys, marker) 
        plt.ylabel(y_label)
        plt.xlabel(x_label)         # months or years
        plt.title(title)
        if legend is None:
            legend = ["country " + str(i) for i in range(len(series))]
        plt.legend(legend)
        if grid:
            plt.grid()
        
        if path is not None:
            plt.savefig(path)
        plt.show()
        plt.close()


    def plot2(series,
              marker = "-", size = (10,4),
              x_label = "period", y_label = "value", y_lim = None, x_lim = None,
              title = "Plot", legend = None,
              series2 = None, y2_lim = None, y2_label = "value 2", legend2 = None, marker2 = "-",
              zipping = True, zipping2 = True,
              grid = True,
              path = None):
        """Plots multiple time series."""
        if zipping:
            ys = list(zip(*series))
        else:
            ys = series
        
        plt.rcParams["figure.figsize"] = size
        fig, ax = plt.subplots()
        plt.title(title)
        
        plots = ax.plot(ys, marker)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if legend is None:
            legend = ["country " + str(i) for i in range(len(series))]
        legend = legend[:len(plots)]
        if y_lim is not None:
            ax.set_ylim(y_lim)
        if x_lim is not None:
            ax.set_xlim(x_lim)
            
        if series2 is not None:
            ax2 = ax.twinx()
            ax2._get_lines.prop_cycler = ax._get_lines.prop_cycler
            if zipping2:
                ys2 = list(zip(*series2))
            else:
                ys2 = series2
            plots += ax2.plot(ys2, marker2)
            ax2.set_ylabel(y2_label)
            if legend2 is None:
                legend2 = ["country " + str(i) for i in range(len(series2))]
            legend += legend2
            #ax2.legend(legend2)
            if y2_lim is not None:
                ax2.set_ylim(y2_lim)
        
        ax.legend(plots, legend)        
        if grid:
            plt.grid()
            
        if path is not None:
            plt.savefig(path, bbox_inches = "tight")
        plt.show()
        plt.close()    
    
    
    def plot_circles(radii, spacing = 1, grid = None,  # actually diameters
                     no_rows = 3, no_cols = 3,
                     x_ticks = None, y_ticks = None,
                     x_label = None, y_label = None,
                     title = None, size = (10,10), background_grid = False,
                     path = None):
        plt.rcParams["figure.figsize"] = size
        figure, axes = plt.subplots()
        axes.set_aspect( 1 )
        if grid == None:
            grid = [[(spacing*j, spacing*i) for j in range(1,1+no_cols)] for i in range(1,1+no_rows)]
        for i, per_costs in enumerate(radii):
            for j, rad in enumerate(per_costs):
                Drawing_colored_circle = plt.Circle(( grid[i][j][0] , grid[i][j][1] ), rad/2 )
                axes.add_artist( Drawing_colored_circle )
        
        plt.xlim(0,spacing*(no_cols+1))
        plt.ylim(0,spacing*(no_rows+1))
        
        if x_ticks is None:
            x_ticks = ["low", "medium", "free trade"][0:no_cols]
        if y_ticks is None:
            y_ticks = ["high", "medium", "none"][0:no_rows]
        plt.xticks([row[0] for row in grid[0]], x_ticks)
        plt.yticks([row[0][1] for row in grid], y_ticks)
        
        if x_label is None:
            x_label = "trade quotas"
        if y_label is None:
            y_label = "trade costs"
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        if title is None:
            title = 'Mean Export Rates for base-base scenario'
        plt.title( title )
        if background_grid:
            plt.grid()
        if path is not None:
            plt.savefig(path, bbox_inches = "tight")  
        plt.show()
        plt.close()

        
    def curve(series1, series2, 
              marker = "o-", individually = True, 
              standard = True, size = (12,5), grid = True,
              title = "Phillips curve",
              x_label = "unemployment", y_label = "inflation",
              both_curves = False, x_lims = None, y_lims = None,
             path = None):
        """Plots 2-D plane of given series."""
        if both_curves:
            titles = ["Phillips curve", "Beveridge curve"]
            y_labels = y_label
            N = 2  # number of subplots
            M =  1      # number of rows                  int(str(N)+str(i//2+1)+str(i%2+1))
            fig = plt.figure(figsize = size)
            plots = [fig.add_subplot(M,2,i+1) for i in range(N)]
            for i, chart in enumerate(plots):
                if grid:
                    chart.grid()
                chart.set_title(titles[i])
                chart.set_xlabel(x_label)
                chart.set_ylabel(y_labels[i])
                chart.plot(series1[i], series2[i], marker)
                if standard:
                    chart.set_xlim([0, 0.3])            # x axis from 0 to .3
                    chart.set_ylim([-0.1, 0.3])            # y axis from 0 to .2
                if x_lims is not None:
                    chart.set_xlim(x_lims[i]) 
                if y_lims is not None:
                    chart.set_ylim(y_lims[i])
            fig.suptitle(title)
            fig.subplots_adjust(hspace = 0.7)
             
        elif not individually:
            plt.rcParams["figure.figsize"] = size
            xs = list(zip(*series1))
            ys = list(zip(*series2))
            if standard:                      # standard measures
                plt.xlim([0, 0.3])            # x axis from 0 to .3
                plt.ylim([-0.1, 0.3])            # y axis from 0 to .2
            plt.plot(xs, ys, marker) 
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.legend(["country " + str(i) for i in range(len(series1))])
            
        else:
            N = len(series1)   # number of subplots
            M =  (N+1)//2      # number of rows                  int(str(N)+str(i//2+1)+str(i%2+1))
            fig = plt.figure(figsize = size)
            plots = [fig.add_subplot(M,2,i+1) for i in range(N)]
            for i, chart in enumerate(plots):
                chart.set_title("country " + str(i))
                chart.set_xlabel(x_label)
                chart.set_ylabel(y_label)
                chart.plot(series1[i], series2[i], marker)
                if standard:
                    chart.set_xlim([0, 0.3])            # x axis from 0 to .3
                    chart.set_ylim([-0.1, 0.3])            # y axis from 0 to .2
            fig.suptitle(title)
            fig.subplots_adjust(hspace = 0.7)
        
        if path is not None:
            plt.savefig(path)
        plt.show()
        plt.close()
        
    def whiskers(series, x_labels = None, y_label = "value", title = "Plot", size = (12,5), path = None):
        """Creates boxplots of given time series."""
        if x_labels == None:
            labels = ["country " + str(i) for i in range(len(series))]
        else:
            labels = x_labels
            
        plt.rcParams["figure.figsize"] = size
        plt.boxplot(series, labels = labels)
        plt.title(title)
        plt.ylabel(y_label)
        
        if path is not None:
            plt.savefig(path)
        plt.show()
        plt.close()
        
    def histogram(series, x_label = "variable", y_label = "value", title = "Plot", legend = None, 
                  grid = False, size = (12,5),
                  path = None):
        """Creates histograms for given series."""
        plt.rcParams["figure.figsize"] = size
        plt.hist(series)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        if legend is None:
            legend = ["country " + str(i) for i in range(len(series))]
        plt.legend(legend)
        if grid:
            plt.grid()
        if path is not None:
            plt.savefig(path)
        plt.show()
        plt.close()
        
          
    def compare(*multiple_series,   
                dim = [2, 1],
                size = (10, 7),
                sharex = "col",
                sharey = "row",
                x_labels = None, 
                y_labels = None, 
                legend = None,
                titles = None,
                sup_title = "Comparison figure",
               grid = True,
               path = None):
        """Creates multiple aligned plots."""
        M, N = dim
        plt.rcParams["figure.figsize"] = size
        fig, axs = plt.subplots(M, N, sharex = sharex, sharey = sharey)
        fig.suptitle(sup_title) 
        L = M*N  
        if x_labels is None:
            x_labels = ["month"]*L
        if y_labels is None:
            y_labels = ["value"]*L
        if titles is None:
            titles = ["Plot"]*L
        for i in range(L):
            ys = list(zip(*multiple_series[i]))
            
            if M == 1 or N == 1:
                axs[i].set_xlabel(x_labels[i]) 
                axs[i].set_ylabel(y_labels[i]) 
                axs[i].title.set_text(titles[i])
                axs[i].plot(ys)
                if legend is None:
                    axs[i].legend(["country " + str(i) for i in range(len(multiple_series[i]))])
                elif legend != "No":
                    axs[i].legend(legend[i])
                if grid:
                    axs[i].grid()
            else:
                j = i//N
                k = i%N  
                axs[j, k].set_xlabel(x_labels[i]) 
                axs[j, k].set_ylabel(y_labels[i]) 
                axs[j, k].title.set_text(titles[i])
                axs[j, k].plot(ys)
                if legend is None:
                    axs[j, k].legend(["country " + str(i) for i in range(len(multiple_series[i]))])
                elif legend != "No":
                    axs[j, k].legend(legend[i])
                if grid:
                    axs[j, k].grid()    
            
        #for ax in fig.get_axes():
            #ax.label_outer()
        
        if path is not None:
            plt.savefig(path)
        plt.show()
        plt.close()    
        
    
    
    def panel(*data_dict, name = "main", countries = "all", csv = False, grid = True, path = None,
             sup_title = None, titles = None, x_labels = None, y_labels = None, 
             variables = None, yearly_prod = True, titl1 = True):
        """From given simulation datasets and for chosen countries shows chosen graphical panel."""
        no_sim = len(data_dict)      # number of simulations displayed
        if countries == "all":
            if csv:                  # if we use data from csv files
                countries = [range(len(sim["median_real_wage_m"].data)) for sim in data_dict]    # no of countries in individual simulations
            else:
                countries = [range(len(sim["median_real_wage_m"])) for sim in data_dict]
        
        def panel_structure(no_sim, no_rows, variables, 
                        countries, data_dict, 
                        y_labels, titles,
                        sup_title, x_lab = "month",
                        grid = True, path = None):   
            """Constructs panel for given variables."""
            
            def pull_out(variable, data):
                if variable[1] == "means":
                    return data[variable[0]].means()
                if variable[1] == "sums":
                    return data[variable[0]].sums()
                if variable[1] == "data":
                    if csv:
                        return data[variable[0]].data
                    else:
                        return data[variable[0]]
            
            def make_legend(countries, no_of_rows):
                """Contructs legends for subplots."""
                legend = []
                for sub in countries:
                    leg = ["country " + str(cc) for cc in sub]
                    legend.append(leg)
                    legend.append(leg)
                return legend*no_of_rows
            
            dims = [no_sim*no_rows, 2]
            plots = []
            for i in range(no_rows):
                items = []
                for var in variables[2*i:2*(i+1)]:
                    if var[0] == "income_distributions":
                        new_item = []
                        for j,sim in enumerate(data_dict):
                            if csv:
                                sub_item = [sim["profits_share_y"].data[l] for l in countries[j]]           
                                sub_item.extend([sim["wage_share_y"].data[l] for l in countries[j]])
                            else:
                                sub_item = [sim["profits_share_y"][l] for l in countries[j]]
                                sub_item.extend([sim["wage_share_y"][l] for l in countries[j]])
                            new_item.append(sub_item)
                        items.append(new_item)
                    else:
                        items.append([ [pull_out(var, sim)[l] for l in countries[j]] for j,sim in enumerate(data_dict)])
                [plots.extend([item1, item2]) for item1, item2 in zip(items[0], items[1])]
                
            legend = make_legend(countries, no_rows)
            if isinstance(x_lab, str):
                x_labels = [x_lab]*(no_rows*2*no_sim)
            else:
                x_labels = x_lab
            
            Visual.compare(*plots, dim = dims, size = (17, 3.5*no_rows*no_sim), 
                           sharey = False, sharex = True, legend = legend,
                           y_labels = y_labels, x_labels = x_labels, 
                           titles = titles, sup_title = sup_title, 
                           grid = grid, path = path)
        
        
        if name == "main": # main panel - mean offer prices, price levels, employment rates, total consumption volumes,
                                        # median real wages, mean sales volume
            variables = [("prices","means"), ("price_level_m","data"), ("employment","means"), 
                         ("cons","sums"), ("median_real_wage_m","data"), ("sales","means")]
            y_labels = ["offer price", "unit value of sales"]*no_sim + ["%", "volume"]*no_sim + ["wage", "volume"]*no_sim
            titles = ["mean prices", "price level"]*no_sim + \
            ["employment rate", "total consumption"]*no_sim + ["median real wages", "mean sales"]*no_sim
            sup_title = "Main Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "cons": # consumption panel - mean offer prices, hsh deposits, mean consumption values, hsh hoarding,
                                                # imports rates, forced savings rates 
            
            variables = [("prices","means"), ("hsh_deposits","sums"), ("cons","means"), 
                         ("hoarding_m","data"), ("total_import_rates_m","data"), ("forced_savings","means")]
            y_labels = ["offer price", "value"]*no_sim + ["volume", "% of income"]*no_sim + ["% of consumption", "value"]*no_sim
            titles = ["mean prices", "HSHs' deposits"]*no_sim + ["mean consumption", "HSHs' hoarding of deposits"]*no_sim +\
            ["imports to consumption rate", "HSHs' mean forced savings rate"]*no_sim
            sup_title = "Consumption Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "sentiments": # sentiments panel - hshs sentiment, firms sentiment, employment rate, self-financing rate,
                                                      # hshs hoarding rate, firms dividends
            variables = [("hsh_sentiment","means"), ("firm_sentiment","means"), ("employment","means"), 
                         ("self_financing_ratio_m","data"), ("hoarding_m","data"), ("firm_dividends","means")]
            y_labels = ["% of optimists", "% of optimists"]*no_sim + ["%", "%"]*no_sim + ["% of income", "value"]*no_sim
            titles = ["HSHs' sentiments", "firms' sentiments"]*no_sim + ["employment rate", "self-financing ratio"]*no_sim +\
            ["HSHs' hoarding of deposits", "firms' mean dividends"]*no_sim
            sup_title = "Sentiments Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "profits": # profits panel - mean real profits, profit shares on incomes, mark-ups, capacity utilization,
                                                # firms dividends, bankruptcies
                
            variables = [("mean_real_profits_m","data"), ("profits_share_m","data"), ("mark_ups_m","data"), 
                         ("capacity_utilization_m","data"), ("firm_dividends","means"), ("bankruptcies","sums")]
            y_labels = ["value", "% of total income"]*no_sim + ["ratio", "%"]*no_sim + ["value", "amount"]*no_sim
            titles = ["mean real profits", "profit share"]*no_sim + ["mark-ups", "capacity utilization"]*no_sim + \
            ["firms' mean dividends", "bankruptcies"]*no_sim
            sup_title = "Profits Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "money": # money panel - deposits, loans, inflation, doubtful ratios, money velocities, bank dividends,
                                            # adequacy ratios, banks' own deposits, wto bank accounts, banks' capitals
            
            if csv:
                var9 = "bank_accounts"
            else:
                var9 = "spec_bank_accounts"
            
            variables = [("deposits","sums"), ("loans","sums"), ("inflation_y","data"), 
                         ("doubtful_ratio","sums"), ("money_velocity_y","data"), ("bank_dividend","sums"),
                        ("capital_adequacy_ratio_m","data"), ("bank_deposit","sums"), (var9,"sums"), ("bank_capital","sums"),]
            y_labels = ["value", "value"]*no_sim + ["rate", "rate"]*no_sim + ["frequency", "value"]*no_sim + \
            ["%", "value"]*no_sim + ["value", "value"]*no_sim
            titles = ["total deposits", "loans"]*no_sim + ["yearly inflation", "doubtful loans ratio"]*no_sim + \
            ["yearly money velocity", "banks' dividends"]*no_sim + ["capital adequacy ratios", "banks' own deposits "]*no_sim +\
            ["foreign balances", "banks' capital"]*no_sim
            sup_title = "Money Panel"
            
            panel_structure(no_sim, 5, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "int_trade": # international trade panel - export rates, import rates, detailed exports, detailed imports
                                                              # for country 0, exchange rates, trade balances
            
            if csv:
                var3, var4, var5 = "export_details", "import_details", "exch_rates" 
            else:
                var3, var4, var5 = "spec_export_details", "spec_import_details", "spec_exch_rates"
            
            variables = [("total_export_rates_m","data"), ("total_import_rates_m","data"), (var3,"sums"), 
                         (var4,"sums"), (var5,"sums"), ("total_trade_balances_m","data")]
            y_labels = ["% of sales", "% of consumption"]*no_sim + ["volume", "volume"]*no_sim + ["rate", "volume"]*no_sim
            titles = ["total exports to sales ratios", "total imports to consumption ratio"]*no_sim + \
            ["export details for country 0", "import details for country 0"]*no_sim + \
            ["exchange rates for country 0", "total trade balances"]*no_sim
            sup_title = "International Trade Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "industry": # industry panel - production, loans, inventories, self-financing, prices, wages
        
            
            variables = [("production","sums"), ("loans","sums"), ("inventories","sums"), 
                         ("self_financing_ratio_m","data"), ("prices","means"), ("working_wages","means")]
            y_labels = ["volume", "value"]*no_sim + ["volume", "%"]*no_sim + ["value", "value"]*no_sim
            titles = ["production", "loans"]*no_sim + ["inventories", "self-financing ratio"]*no_sim + \
            ["mean offer prices", "mean wages"]*no_sim
            sup_title = "Industry Panel"
            
            panel_structure(no_sim, 3, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
        
        elif name == "labor": # labor panel - unemployment rates, mean real wages, vacancies, vacancy rates, mean unemployment 
                                             # durations, voluntary unemployed rates, labor demands, wage shares,
        
            variables = [("unemployment_m","data"), ("mean_real_wage_m","data"), ("vacancies","means"), 
                         ("vacancy_rates_m","data"), ("unemployed_months_u","means"), ("vol_unemployed_rate_m","data"),
                        ("labor_demand","means"), ("wage_share_m","data")]
            y_labels = ["%", "value"]*no_sim + ["amount", "%"]*no_sim + ["amount", "%"]*no_sim + ["amount", "% of income"]*no_sim
            titles = ["unemployment rates", "mean real wages"]*no_sim + ["mean vacancies", "mean vacancy rates"]*no_sim + \
            ["mean length of unemployment", "rate of voluntary unemployment"]*no_sim + ["mean targeted labor", "wage shares"]*no_sim
            sup_title = "Labor Panel"
            
            panel_structure(no_sim, 4, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "cycles": # cycles panel - prices, offered wages, sales, employment, bankruptcies, number of firms, excessive debt,
                                              # targeted debt
            if csv:
                var6 = "no_of_firms"
            else:
                var6 = "spec_no_of_firms"
        
            variables = [("prices","means"), ("offered_wages","means"), ("sales","means"), 
                         ("employment","means"), ("bankruptcies","sums"), (var6,"sums"),
                        ("excessive_debt_rate_m","data"), ("targeted_debt_m","data")]
            y_labels = ["value", "value"]*no_sim + ["volume", "%"]*no_sim + ["amount", "amount"]*no_sim + ["ratio", "value"]*no_sim
            titles = ["mean prices", "mean offered wages"]*no_sim + ["mean sales", "employment rates"]*no_sim + \
            ["bankruptcies", "number of firms"]*no_sim + ["debt to targeted debt ratio", "targeted debt"]*no_sim
            sup_title = "Business Cycles Panel"
            
            panel_structure(no_sim, 4, variables, countries, data_dict, y_labels, titles, sup_title, grid = grid, path = path)
            
        elif name == "yearly": # yearly data panel - production, income distribution, consumption, mark-ups, inventories, 
                                                   # capacity utilization, bankruptcy rates, unemployment rates, money velocity,
                                                   # vacancies rates, trade balances, inflation
        
            for sim in data_dict:                                                                                  ####
                if csv:
                    ts = Special_TS("production_y")
                    ts.data = periodize(sim["production"].sums())
                    sim["production_y"] = ts
                else:
                    sim["production_y"] = periodize(sim["production"].sums())
        
            variables = [("production_y","data"), ("income_distributions","data"), ("cons_y","data"), 
                         ("mark_ups_y","data"), ("inventories_y","data"), ("capacity_utilization_y","data"),
                        ("bankruptcy_rate_y","data"), ("unemployment_y","data"), ("money_velocity_y","data"), 
                         ("vacancy_rates_y","data"), ("total_trade_balances_y","data"), ("inflation_y","data")]
            y_labels = ["volume", "%"]*no_sim + ["volume", "%"]*no_sim + ["volume", "%"]*no_sim + ["%", "%"]*no_sim\
             + ["frequency", "%"]*no_sim + ["volume", "%"]*no_sim
            titles = ["production", "income distribution"]*no_sim + ["consumption", "mark-ups"]*no_sim + \
            ["inventories", "capacity utilization"]*no_sim + ["bankruptcy rates", "unemployment rates"]*no_sim \
            + ["money velocity", "vacancy rates"]*no_sim + ["trade balances", "inflation"]*no_sim 
            sup_title = "Yearly Time Series Panel"
            
            panel_structure(no_sim, 6, variables, countries, data_dict, y_labels, titles, sup_title, x_lab = "year", 
                            grid = grid, path = path)
            
        
        elif name == "ill": 
            if yearly_prod:
                for sim in data_dict:
                    sim["production_y_to_m"] = y_to_m(sim["production_y"])
                var1 = ("production_y_to_m","data")
                if titl1:
                    titl1 = "Production (yearly, linearly interpolated)"
                else:
                    titl1 = "Production (yearly)"
            else:
                var1 = ("production","sums")
                titl1 = "Production"
            variables = [
                var1, ("employment","means"), 
                ("prices","means"), ("mean_real_wage_m","data"), 
                ("firm_sentiment","means"), ("hsh_sentiment","means"),
                ("firm_dividends","means"), ("vacancies","means") 
            ]
            if y_labels is None:
                y_labels = ["volume", "rate"]*no_sim \
                + ["price", "wage"]*no_sim \
                + ["optimism rate", "optimism rate"]*no_sim \
                + ["dividend", "vacancies"]*no_sim
            
            if titles is None:
                titles = [titl1, "Employment Rates"]*no_sim \
                + ["Mean Prices", "Mean Real Wages"]*no_sim \
                + ["Firms' Sentiments", "Households' Sentiments"]*no_sim \
                + ["Mean Firm Dividends", "Mean Vacancies per Firm"]*no_sim 
            
            if sup_title is None:
                sup_title = "Illustrative Panel"
            if x_labels is None:
                x_labels = "month"
            
            panel_structure(no_sim, 4, variables, countries, data_dict, y_labels, titles, sup_title, x_lab = x_labels, 
                            grid = grid, path = path)
        
        elif name == "customized":
            no_vars = len(variables)
            no_rows = int(no_vars/2) + no_vars%2
            odd_variables = True if no_vars%2 != 0 else False
            
            if y_labels is None:
                final_y_labels = ["value"]*no_sim*no_vars
            else:
                final_y_labels = []
                for labels in zip(y_labels[::2], y_labels[1::2]):
                    final_y_labels.extend(list(labels)*no_sim)
                if odd_variables:
                    final_y_labels.extend(y_labels[-1]*no_sim)
            
            if titles is None:
                titles = [var[0] for var in variables]
            
            final_titles = []
            for tls in zip(titles[::2], titles[1::2]):
                final_titles.extend(list(tls)*no_sim)
            if odd_variables:
                final_titles.extend(titles[-1]*no_sim)
            
            if sup_title is None:
                sup_title = "Customized Panel"
            
            if x_labels is None:
                x_labels = "month"
                
            panel_structure(no_sim, no_rows, variables, countries, data_dict, 
                            final_y_labels, final_titles, sup_title, x_lab = x_labels, 
                            grid = grid, path = path)



plot = Visual.plot
plot2 = Visual.plot2
curve = Visual.curve
whiskers = Visual.whiskers
histogram = Visual.histogram
compare = Visual.compare
panel = Visual.panel
