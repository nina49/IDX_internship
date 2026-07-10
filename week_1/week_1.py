import pandas as pd
from pathlib import Path
#Stores Listing CSV files in a sorted listed
data = Path("./Data")
listing_csv = sorted(data.glob("CRMLSListing*.csv"))
# Number of listing files
num_listing_csv = len(listing_csv)
print(f"Number of listing files: {num_listing_csv}")
# All the Listing CSV files combined into a pandas DataFrame
listing_dataFrames= [
    pd.read_csv(file, encoding="latin-1", low_memory=False)
    for file in listing_csv
]
#Number of rows before Listing concat
rows_before_concat_l = sum(len(df) for df in listing_dataFrames)
print(f"Number of rows before concatenation: {rows_before_concat_l}")
# Concat:combines all the monthly Listing DataFrames
df_listing_concat= pd.concat(listing_dataFrames, ignore_index=True)
# Number of rows after listing concat
rows_after_concat_l = len(df_listing_concat)
print(f"Number of rows after concatenation: {rows_after_concat_l}")

#Number of rows before Resedential filter
rows_before_filter_l = len(df_listing_concat)
print(f"Number of rows before Residential filter: {rows_before_filter_l}")
#Filters for "Residential" Property Type 
df_listing= df_listing_concat[df_listing_concat["PropertyType"] == "Residential"]
# Number of rows after Residential filter
rows_after_filter_l =len(df_listing)
print(f"Number of rows after Residential filter: {rows_after_filter_l}")

#Saves Filtered Listing DataFrame as a new CVS file
df_listing.to_csv("./Data/Listing_Combined.csv", index=False)
df_listing_concat.to_csv("./Data/Listing_Combined_2.csv", index=False)

#Stores Sold CSV files in a sorted listed
sold_csv = sorted(data.glob("CRMLSSold*.csv"))
# Number of sold files
num_sold_csv= len(sold_csv)
print(f"Number of rows sold: {num_sold_csv}")
# All the Sold CSV files combined into a pandas DataFrame
sold_dataFrames = [
    pd.read_csv(file, encoding="latin-1", low_memory=False)
    for file in sold_csv
]

# Number of rows before Sold concat
rows_before_concat_s = sum(len(df) for df in sold_dataFrames)
print(f"Number of rows before Sold concatenation: {rows_before_concat_s}")
# Concat:combines all the monthly Sold DataFrames
df_sold_concat= pd.concat(sold_dataFrames, ignore_index=True)
# Number of rows after listing concat
rows_after_concat_s = len(df_sold_concat)
print(f"Number of rows after Sold concatenation: {rows_after_concat_s}")

#Number of rows before Resedential filter
rows_before_filter_s = len(df_sold_concat)
print(f"Number of rows before Residential filter (Sold): {rows_before_filter_s}")
#Filters for "Residential" Property Type 
df_sold=df_sold_concat[df_sold_concat["PropertyType"] == "Residential"]
# Number of rows after Residential filter
rows_after_filter_s = len(df_sold)
print(f"Number of rows after Residential filter (Sold): {rows_after_filter_s}")

#Saves Filtered Sold DataFrame as a new CVS file
df_sold.to_csv("./Data/Sold_Combined.csv", index=False)
df_sold_concat.to_csv("./Data/Sold_Combined_2.csv",index=False)

#Results
#CRMLS_Listing
#Number of files: 29X4
#Number of rows before concatenation: 887859
#Number of rows after concatenation: 887859
#Number of rows before Residential filter: 887859
#Number of rows after Residential filter: 564289

#CRMLS_Sold
#Number of files: 29
#Number of rows before concantenation: 634870
#Number of rows after concatenation: 634870
#Number of rows before Residential filter: 634870
#Number of rows after Residential filter: 426372