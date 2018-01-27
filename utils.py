import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import definitions as dfn

# ********** Getting date-specific entries from data series **********

# Find indices in date column that fall within the specified time range.
def find_dates_in_range(date_col, start_date, end_date):
    if str(type(date_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with dates, got " + str(type(date_col)) + ".")
    dates_in_range = date_col.apply(lambda x : x >= start_date and x <= end_date)
    if not dates_in_range.any():
        raise ValueError("No dates found in range")
    return np.where(dates_in_range)

# Mean of a data series across a specified date range.
def mean_in_date_range(data_col, date_col, start_date, end_date):
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with data, got  " + str(type(data_col)) + ".")
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with date, got  " + str(type(date_col)) + ".")
    data_in_range = data_col.iloc[find_dates_in_range(date_col, start_date, end_date)].dropna()
    return data_in_range.mean()

def mean_year_month(data_col, date_col, start_year, start_month, end_year, end_month):
    # Create a dictionary of mean values sorted by year and month.
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with data, got  " + str(type(data_col)) + ".")
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with date, got  " + str(type(date_col)) + ".")
    dict = {}
    for d in range(0, len(date_col)):
        date = date_col[d];
        if not dict.has_key(date.year):
            dict[date.year] = {}
        if not dict[date.year].has_key(date.month):
            dict[date.year][date.month] = []
        # Put data entry in the bucket for current year and month.
        if not math.isnan(data_col[d]):
            dict[date.year][date.month].append(data_col[d])
    
    # Output is the mean of each bucket in the requested range.
    output = [];
    for y in range(start_year, end_year + 1):
        if y > start_year:
            start_month_for_year = 1
        else:
            start_month_for_year = start_month
        if y < end_year:
            end_month_for_year = 12;
        else:
            end_month_for_year = end_month;
        for m in range(start_month_for_year, end_month_for_year + 1):
            if (not dict.has_key(y)) or (not dict[y].has_key(m)):
                raise ValueError("No data for year %s, month %s." % (y, m))
            output.append(np.mean(dict[y][m]))
    return output

def mean_year_quarter(data_col, date_col, start_year, start_quarter, end_year, end_quarter):
    # Create a dictionary of mean values sorted by year and quarter.
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with data, got  " + str(type(data_col)) + ".")
    if str(type(data_col)).find("Series") < 0:
        raise ValueError("Expecting a pandas series with date, got  " + str(type(date_col)) + ".")
    dict = {}
    for d in range(0, len(date_col)):
        date = date_col[d];
        quarter = (date.month -1) / 3 + 1
        if not dict.has_key(date.year):
            dict[date.year] = {}
        if not dict[date.year].has_key(quarter):
            dict[date.year][quarter] = []
        # Put data entry in the bucket for current year and quarter.
        if not math.isnan(data_col[d]):
            dict[date.year][quarter].append(data_col[d])
    
    # Output is the mean of each bucket in the requested range.
    output = [];
    for y in range(start_year, end_year + 1):
        if y > start_year:
            start_quarter_for_year = 1
        else:
            start_quarter_for_year = start_quarter
        if y < end_year:
            end_quarter_for_year = 4;
        else:
            end_quarter_for_year = end_quarter;
        for q in range(start_quarter_for_year, end_quarter_for_year + 1):
            if (not dict.has_key(y)) or (not dict[y].has_key(q)):
                raise ValueError("No data for year %s, quarter %s." % (y, q))
            output.append(np.mean(dict[y][q]))
    return output


# ********** Helpers for parsing months, quarters etc. **********

def get_stock_monthly_data(stock_file, start_year, start_month, end_year, end_month):
    try:
        stock = pd.read_csv("data/stocks/" + stock_file + ".us.txt")
        stock_close = pd.to_numeric(stock.Close, errors = "coerce")
        stock_date = pd.to_datetime(stock.Date)
        stock_monthly_data = mean_year_month(stock_close, stock_date, start_year, \
                start_month, end_year, end_month)
    except:
        raise StandardError("Problem getting monthly data for stock %s" % stock_file)
    return stock_monthly_data

def get_stock_quarterly_data(stock_file, start_year, start_quarter, end_year, end_quarter):
    try:
        stock = pd.read_csv("data/stocks/" + stock_file + ".us.txt")
        stock_close = pd.to_numeric(stock.Close, errors = "coerce")
        stock_date = pd.to_datetime(stock.Date)
        stock_quarterly_data = mean_year_quarter(stock_close, stock_date, start_year, \
                start_quarter, end_year, end_quarter)
    except:
        raise StandardError("Problem getting quarterly data for stock %s" % stock_file)
    return stock_quarterly_data

# Figure out time ranges based on lag specified in months.
# Start year is assumed to start in January.
# End year is assumed to end in December.
# diff indicates whether we are looking at the difference from previous month.
def apply_lag_in_months(start_year, end_year, lag, diff = False):
    start_year = start_year + (lag - diff) / 12
    start_month = 1 + (lag - diff) % 12
    end_year = end_year + 1 + (lag - 1) / 12
    end_month = 1 + ((12 + lag - 1) % 12)
    return start_year, start_month, end_year, end_month

def apply_lag_in_quarters(start_year, end_year, lag, diff = False):
    start_year = start_year + (lag - diff) / 4
    start_quarter = 1 + (lag - diff) % 4
    end_year = end_year + 1 + (lag - 1) / 4
    end_quarter = 1 + ((4 + lag - 1) % 4)
    return start_year, start_quarter, end_year, end_quarter

# Get date range for each month.
def num_days_in_month(month, year):
    if month < 1 or month > 12:
        raise ValueError("Month should be between 1 and 12.")
    days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, \
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if (month == 2) and (year % 4 == 0) and (year != 2000):
        # Leap year.
        return 29
    else:
        return days[month]

def months_in_quarter(quarter):
    if quarter < 1 or quarter > 4:
        raise ValueError("Quarter should be between 1 and 4.")
    return range(3 * quarter - 2, 3 * quarter + 1)

def range_days_in_quarter(year, quarter):
    months = months_in_quarter(quarter)
    start_date = pd.datetime(year, months[0], 1)
    end_date = pd.datetime(year, months[2], num_days_in_month(months[2]))
    return start_date, end_date


# ********** Helpers for plots **********
    
def plot_stock_data(stock_files, lag, scaled = False, axes_object = ""):
    # Plot stock data vs. time in months.
    # stock_files is a string or a list of strings representing a ticker symbol.
    # lag is time lag in months relative to the time frame defined in definitions.py.
    # Optionally, scale data by the mean of each stock for better visibility.

    if type(stock_files) is str:
        stock_files = [stock_files]

    if axes_object == "":
        fig, ax = plt.subplots(1, 1)
    else:
        ax = axes_object

    sy, sm, ey, em = apply_lag_in_months(dfn.start_year, dfn.end_year, lag)
    plot_data = []
    for stock_file in stock_files:
        st = get_stock_monthly_data(stock_file, sy, sm, ey, em)
        if scaled:
            st = (st / np.mean(st)).tolist()
        plot_data.append(st)
    plot_monthly_data(plot_data, sy, sm, ey, em, axes_object = ax, \
            ylabel = ("scaled " * scaled) + "stock price")
    
# Get x-axis for plots of monthly data.
def get_x_axis_monthly(start_year, start_month, end_year, end_month):
    answer = []
    for m in range(start_month, 13):
        answer.append("%s/%s" % (str(start_year), str(m)))
    for y in range(start_year + 1, end_year):
        for m in range(1, 13):
            answer.append("%s/%s" % (str(y), str(m)))
    for m in range(1, end_month + 1):
        answer.append("%s/%s" % (str(end_year), str(m)))
    return answer

# Get x-axis for plots of quarterly data.
def get_x_axis_quarterly(start_year, start_quarter, end_year, end_quarter):
    answer = []
    for q in range(start_quarter, 5):
        answer.append("%s/%s" % (str(start_year), str(q)))
    for y in range(start_year + 1, end_year):
        for q in range(1, 5):
            answer.append("%s/%s" % (str(y), str(q)))
    for q in range(1, end_quarter + 1):
        answer.append("%s/%s" % (str(end_year), str(q)))
    return answer

def plot_monthly_data(data, start_year, start_month, end_year, end_month, \
            axes_object = "", title = "", xlabel = "Month", ylabel = ""):
    # Convert data to list of lists, so several lines could be plotted.
    if not type(data[0]) is list:
        data = [data]

    if axes_object == "":
        fig, ax = plt.subplots(1, 1)
    else:
        ax = axes_object

    # plot data.
    for data_line in data:
        ax.plot(data_line)

    # Set text on plot.
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    x_axis = get_x_axis_monthly(start_year, start_month, end_year, end_month)
    x_axis_tick_labels = [0] + [x_axis[i] for i in ax.get_xticks()[1:-1].astype(int).tolist()]
    ax.xaxis.set_ticklabels(x_axis_tick_labels)
    return ax
    
def plot_quarterly_data(data, start_year, start_quarter, end_year, end_quarter, \
            axes_object = "", title = "", xlabel = "Quarter", ylabel = ""):
    if not type(data[0]) is list:
        data = [data]
    if axes_object == "":
        fig, ax = plt.subplots(1, 1)
    else:
        ax = axes_object
    for data_line in data:
        ax.plot(data_line)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    x_axis = get_x_axis_quarterly(start_year, 1, end_year, 4)
    x_axis_tick_labels = [0] + [x_axis[i] for i in ax.get_xticks()[1:-1].astype(int).tolist()]
    ax.xaxis.set_ticklabels(x_axis_tick_labels)
    return ax