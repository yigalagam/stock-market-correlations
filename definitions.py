# Start year for collecting indicator data (starts in January)
start_year = 2010
# End year for collecting indicator data (ends in December)
end_year = 2016

# Information on all the indicators. Each indicator key is associated with a dictionary:
# - title: Title for plots.
# - file: Raw data file.
# - raw column: Name of column in raw data file.
# - df column: Name ot use for column in dataframe.
# - time: Time resolution of raw data (day, month or quarter).
# - diff (optional): Use the difference of the timeseries.

indicators = {
    "BOND_RATE" : {"title": "10 year bond rate", "file" : "10_year_treasury_rate.csv",
            "raw column" : "DGS10", "df column" : "Bond_rate" , "time" : "day"},
    "GOLD" : {"title" : "Price of gold", "file" : "gold_PM_USD.csv",
            "raw column" : "GOLDPMGBD228NLBM", "df column" : " Gold", "time" : "day"},
    "CRUDE" : {"title" : "Price of crude oil", "file" : "oil_Brent_WPI.csv",
            "raw column" : "bw", "df column" : "Oil", "time" : "day"}, 
    "EXCHANGE_RATE" : {"title" : "USD exchange rate", "file" : "Broad_USD_exchange_rate_index.csv",
            "raw column" : "DTWEXB", "df column" : "Exchange_rate", "time" : "day"}, 
    "CONS_PRICE_INDEX" : {"title" : "Median consumer price index", "file" : "median_consumer_price_index.csv",
            "raw column" : "MEDCPIM094SFRBCLE", "df column" : "Cons_price_index", "time" : "month",
            "diff" : False}, 
    "PROD_PRICE_INDEX" : {"title" : "Producer price index (all commodities)", "file" : "producer_price_index.csv",
            "raw column" : "PPIACO", "df column" : "Prod_price_index", "time" : "month"}, 
    "UNEMPLOYMENT" : {"title" : "US natural unemployment rate", "file" : "natural_unemployment_rate.csv",
            "raw column" : "NROU", "df column" : "Unemployment", "time" : "quarter",
            "diff" : False}, 
    "GDP" : {"title" : "GDP per capita", "file" : "GDP_per_capita.csv",
            "raw column" : "A939RX0Q048SBEA", "df column" : "GDP", "time" : "quarter",
            "diff" : False}, 
    "DEBT" : {"title" : "Debt (% of GDP)", "file" : "US_debt_percent_of_GDP.csv",
            "raw column" : "GFDEGDQ188S", "df column" : "Debt", "time" : "quarter",
            "diff" : False}, 
    "HOUSING_STARTS" : {"title" : "US Housing starts", "file" : "housing_starts.csv",
            "raw column" : "HOUST", "df column" : "Housing_starts", "time" : "month"},
    "CONSTRUCTION" : {"title" : "Total construction spending", "file" : "construction_spending.csv",
            "raw column" : "TTLCONS", "df column" : "Construction_spending", "time" : "month"}, 
    "CASE_SHILLER" : {"title" : "US Case-Shiller index", "file" : "Case-Shiller.csv",
            "raw column" : "CSUSHPINSA", "df column" : "Case_shiller", "time" : "month"}, 
    "INDUSTRIAL PRODUCTION" : {"title" : "Industrial production index", "file" : "industrial_production_index.csv",
            "raw column" : "INDPRO", "df column" : "Ind_production", "time" : "month"}, 
    "CORPORATE_PROFITS" : {"title" : "Corporate profits after tax", "file" : "corporate_profits_after_tax.csv",
            "raw column" : "CP", "df column" : "Corp_profits", "time" : "quarter"}, 
    "INFLATION" : {"title" : "10 year breakeven inflation rate", "file" : "breakeven_inflation_rate.csv",
            "raw column" : "T10YIEM", "df column" : "Breakeven_Inflation", "time" : "month"}, 
}