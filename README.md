# IDX_internship
Data Analyst Internship Project: Real Estate Market Analysis
#Week 0
Download all CRMLSListingYYYYMM.csv and CRMLSSoldYYYYMM.csv files from the FTP server for dates ranging from 202401 to 202605.
Run the extraction script for any missing months.

#Week 1
Load CRMLSListing CSV and CRMLSSold CSV.
Concatenate the files into one Listings dataset and one Sold datasets respectively.
Filter both datasets to PropertyType == "Residential".
Save the final datasets as new CSV files.

#Week 2-3
Part 1: Understanding the Data
Check the dataset rows and columns
Find the Residential Percentage over other property type share
Find missing values and identify columns with more than 90% missing data.
Analysis on key columns: ClosePrice, ListPrice, LivingArea, DaysOnMarket, BedroomsTotal,BathroomsTotalIntege
- Percentile Summary (min,mean,max,std,0.1,0.25,0.5,0.75,0.9)
- Total Outlier Percentage using IQR
- Histograms and Boxplots
Median and Average of Close Price
Check for data consistency issues (Close Date before Listing Contract Date)
Percentage of Homes Sold above vs below list price
Counties with the Highest Median Closing Prices

Part 2: Mortgage Rate Enrichment
Download the 30-year mortgage rate from the FRED database.
Convert weekly mortgage rates into monthly averages.
Create a year_month column in both Listings and Sold datasets.
Merge the monthly mortgage rates into both datasets and check for missing rows.
Save the merged Listings and Sold datasets as new CSV files.
