import pandas as pd
from pathlib import Path

data_3= Path("./Data")
df_listing= pd.read_csv(data_3 / "Listing_Combined.csv", low_memory=False)
df_sold=pd.read_csv(data_3/"Sold_Combined.csv",low_memory=False)

#Mortgage rate from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

#Converting to Monthly Averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index())

#Creating Join Keys
df_sold['year_month'] = pd.to_datetime(df_sold['CloseDate']).dt.to_period('M')
df_listing['year_month'] = pd.to_datetime(df_listing['ListingContractDate']).dt.to_period('M')

#Merging onto MLS
sold_new= df_sold.merge(mortgage_monthly, on='year_month', how='left')
listing_new = df_listing.merge(mortgage_monthly, on='year_month', how='left')

#Validation Check
null_sold = sold_new['rate_30yr_fixed'].isnull().sum()
null_listings = listing_new['rate_30yr_fixed'].isnull().sum()

print(f"Rows that are unmatched in your Sold dataset: {null_sold}")
print(f"Rows that are unmatched in your Listings dataset: {null_listings}")

print(sold_new[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())
print(listing_new[['ListingContractDate', 'year_month', 'ListPrice', 'rate_30yr_fixed']].head())

#Saving Dataset into CSV
sold_new.to_csv("./Data/CRMLSSold_MortgageR.csv", index=False)
listing_new.to_csv("./Data/CRMLSListing__MortgageR.csv", index=False)


#No unmatched values (null) in merged

#                        Sold Rates
#   CloseDate year_month  ClosePrice  rate_30yr_fixed
#0  2024-01-26    2024-01    240000.0           6.6425
#1  2024-01-05    2024-01    815000.0           6.6425
#2  2024-01-05    2024-01    810000.0           6.6425
#3  2024-01-30    2024-01    858000.0           6.6425
#4  2024-01-29    2024-01   1890500.0           6.6425

#                      Listing Rates
# ListingContractDate year_month   ListPrice  rate_30yr_fixed
#0          2024-01-01    2024-01   1340000.0           6.6425
#1          2024-01-24    2024-01   2500000.0           6.6425
#2          2024-01-12    2024-01   3150000.0           6.6425
#3          2024-01-20    2024-01   3090000.0           6.6425
#4          2024-01-12    2024-01  12725000.0           6.6425