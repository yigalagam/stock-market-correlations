import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import utils as u
import definitions as dfn


# ********** Prepare monthly or quarterly indicator data **********

def get_indicator_data(indicator_dict):
    df = pd.read_csv("data/indicators/%s" % indicator_dict["file"])
    data = pd.to_numeric(df[indicator_dict["raw column"]], errors = "coerce")
    date = pd.to_datetime(df["DATE"])
    if indicator_dict["time"] == "quarter":
        if indicator_dict.has_key("diff") and indicator_dict["diff"] == True:
            return np.diff(u.mean_year_quarter(data, date, dfn.start_year - 1, 4, dfn.end_year, 4)).tolist()
        else:
            return u.mean_year_quarter(data, date, dfn.start_year, 1, dfn.end_year, 4)
    else:
        if indicator_dict.has_key("diff") and indicator_dict["diff"] == True:
            return np.diff(u.mean_year_month(data, date, dfn.start_year - 1, 12, dfn.end_year, 12)).tolist()
        else:
            return u.mean_year_month(data, date, dfn.start_year, 1, dfn.end_year, 12)
    
# ********** Plotting helpers **********

def plot_indicators(indicators_data_dict):
    indicator_names = indicators_data_dict.keys()
    n_indicators = len(indicator_names)
    fig = plt.figure()
    fig.set_size_inches(6, 1.5 * n_indicators)
    
    for i in range(0, n_indicators):
        ax = fig.add_subplot(n_indicators, 1, i + 1)

        indicator_dict = dfn.indicators[indicator_names[i]]
        if indicator_dict["time"] == "quarter":
            u.plot_quarterly_data(indicators_data_dict[indicator_names[i]], dfn.start_year, 1, dfn.end_year, 4, \
            axes_object = ax, title = indicator_dict["title"])
        else:
            u.plot_monthly_data(indicators_data_dict[indicator_names[i]], dfn.start_year, 1, dfn.end_year, 12, \
            axes_object = ax, title = indicator_dict["title"])
 
    plt.tight_layout()
    plt.show()

def plot_feature_histograms(df, n_bins = 50):
    n_plots = len(df.select_dtypes(include=['float64']).columns)
    fig = plt.figure()
    plot_index = 1
    
    for indk in dfn.indicators.keys():
        ind = dfn.indicators[indk]
        if ind["df column"] in df.columns:
            ax = fig.add_subplot(n_plots, 1, plot_index)
            ax.hist(df[ind["df column"]], bins = n_bins)
            ax.set_title(ind["title"])
            ax.set_xbound([-1, 1])
            plot_index = plot_index + 1
 
    fig.set_size_inches(6, 1.5 * n_plots)
    plt.tight_layout()
    plt.show()

def plot_feature_corr(df):
    corr_data = df.select_dtypes(include=['float64']).corr()
    mask = np.zeros_like(corr_data, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(data = corr_data, mask=mask, center=0)    

# ********** Functions to calculate correlation with indicator data **********

# Extract correlation features for S&P 500 companies.
# - indicator data: dictionary with indicator data extracted for
#   the range specified in definitions file.
# - diff: True if we are looking at the difference from last month's stock price
#   instead of raw price.
def get_correlations_sp_500(indicator_data, lag, diff = False):
    sp_df = pd.read_csv("data/S&P_stocks.csv")
    sp_stocks = sp_df.Name.tolist()
    df = pd.DataFrame()
    failures = []

    for st in sp_stocks:
        try:
            st = st.replace(".", "-")
            print "Processing stock %s" % st
            c = corr_indicators(st, indicator_data, lag, diff)
            if len(df.count()) == 0:
                df = pd.DataFrame(c, index=[0])
            else:
                df = df.append(c, ignore_index = True)
        except:
            print "Processing of stock %s failed" % st
            failures.append(st)
    # Reorder columns so name is on left.
    df = df[['Name'] + df.drop('Name', axis = 1).columns.tolist()]
    return df, failures


def corr_indicators(stock_file, indicator_data, lag, diff = False):
    stock_monthly_data = get_monthly_stock_data_for_correlation(stock_file, lag, diff)
    stock_quarterly_data = get_quarterly_stock_data_for_correlation(stock_file, lag, diff)
    stock_corr = {}
    stock_corr['Name'] = stock_file
    
    for indicator in indicator_data.keys():
        if dfn.indicators[indicator]["time"] == "quarter":
            stock_corr[dfn.indicators[indicator]["df column"]] = \
                    np.corrcoef(stock_quarterly_data, indicator_data[indicator])[0][1]
        else:
            stock_corr[dfn.indicators[indicator]["df column"]] = \
                    np.corrcoef(stock_monthly_data, indicator_data[indicator])[0][1]

    return stock_corr


def standardize_correlations(corr_df):
    from sklearn import preprocessing
    # Scale each numeric column to mean of 0 and std of 1.
    num_cols = corr_df.select_dtypes(include=["float64"])
    scaled_df = pd.DataFrame(preprocessing.StandardScaler().fit_transform(num_cols))
    scaled_df.columns = num_cols.columns
    # Join the scaled data back with the non-numeric columns.
    scaled_df = scaled_df.join(corr_df.select_dtypes(exclude=["float64"]))
    return scaled_df

# ********** Helper functions for stock prices / indicator correlations **********

def get_monthly_stock_data_for_correlation(stock_file, lag, diff = False):
    # lag: Lag (in cc1months) of stock data following indicator.
    # For example:q
    # a lag of 1 will meaaure correlation with the stock in the following month.
    # A lag of 0 will measure correlation with stock price in the same month.
    
    # Adjust dates for which to extract stock data based on correlation lag.
    # Start year for indicator data begins at month 1,
    # end year ends at month 12.
    stock_start_year, stock_start_month, stock_end_year, stock_end_month = \
            u.apply_lag_in_months(dfn.start_year, dfn.end_year, lag, diff)
    stock_monthly_data = u.get_stock_monthly_data(stock_file, stock_start_year, \
            stock_start_month, stock_end_year, stock_end_month)
    if diff:
        return np.diff(stock_monthly_data).tolist()
    else:
        return stock_monthly_data

def get_quarterly_stock_data_for_correlation(stock_file, lag, diff = False):
    # lag: Same as monthly data, adjusted to quarterly data.
    quarter_lag = lag / 3 + 1

    # Adjust dates for which to extract stock data based on correlation lag.
    # Start year for indicator data begins at quarter 1, 
    # end year ends at quarter 4.
    stock_start_year, stock_start_quarter, stock_end_year, stock_end_quarter = \
            u.apply_lag_in_quarters(dfn.start_year, dfn.end_year, quarter_lag, diff)
    stock_quarterly_data = u.get_stock_quarterly_data(stock_file, stock_start_year, \
            stock_start_quarter, stock_end_year, stock_end_quarter)
    if diff:
        return np.diff(stock_quarterly_data).tolist()
    else:
        return stock_quarterly_data






indicator_data = {}
for indicator in dfn.indicators.keys():
    indicator_data[indicator] = get_indicator_data(dfn.indicators[indicator])

# plot_indicators(indicator_data)
#c, f = get_correlations_sp_500(indicator_data, diff = False)
#plot_feature_histograms(c)
#c = corr_all_indicators('amzn', 1)
#u.plot_monthly_data(stock_data, dfn.start_year, 1, dfn.end_year, 12, \
#        title = "%s Stock Price (%s Month Lag)" % (stock, dfn.lag), xlabel = "Month")
#plt.show()

#c, f = get_correlations_sp_500()



