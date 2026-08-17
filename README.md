# IDX_internship
Data Analyst Internship Project: Real Estate Market Analysis

 ## Week 0

- Download all CRMLSListingYYYYMM.csv and CRMLSSoldYYYYMM.csv files from the FTP server for dates ranging from 202401 to 202605.
- Run the extraction script for any missing months.

## Week 1

- Load CRMLSListing CSV and CRMLSSold CSV.
- Concatenate the files into one Listings dataset and one Sold datasets respectively.
- Filter both datasets to PropertyType == "Residential".
- Save the final datasets as new CSV files.

## Week 2-3

### Part 1: Understanding the Data
- Check the dataset rows and columns
- Find the Residential Percentage over other property type share
- Find missing values and identify columns with more than 90% missing data.
- Analysis on key columns: ClosePrice, ListPrice, LivingArea, DaysOnMarket, BedroomsTotal,BathroomsTotalIntege
  - Percentile Summary (min, mean, max, std, 0.1, 0.25, 0.5, 0.75, 0.9)
  - Total Outlier Percentage using IQR
  - Histograms and Boxplots
- Median and Average of Close Price
- Check for data consistency issues (Close Date before Listing Contract Date)
- Percentage of Homes Sold above vs below list price
- Counties with the Highest Median Closing Prices

### Part 2: Mortgage Rate Enrichment
- Download the 30-year mortgage rate from the FRED database.
- Convert weekly mortgage rates into monthly averages.
- Create a year_month column in both Listings and Sold datasets.
- Merge the monthly mortgage rates into both datasets and check for missing rows.
- Save the merged Listings and Sold datasets as new CSV files.

## Week 4-5

### Part 1: Data Cleaning and Preparation
- Convert date columns to datetime format:
  - CloseDate
  - PurchaseContractDate
  - ListingContractDate
  - ContractStatusChangeDate
- Remove unnecessary or redundant columns.
- Handle missing values appropriately.
- Convert numeric columns to the correct data types.
- Identify and flag invalid numeric values:
  - ClosePrice <= 0
  - LivingArea <= 0
  - DaysOnMarket < 0
  - Negative Bedrooms or Bathrooms

### Part 2: Date Consistency Checks
- Check that ListingContractDate comes before PurchaseContractDate.
- Check that PurchaseContractDate comes before CloseDate.
- Create flags for records with inconsistent dates:
   - listing_after_close_flag
   - purchase_after_close_flag
   - negative_timeline_flag

### Part 3:Geographic Data Checks
- Check for missing Latitude and Longitude values.
- Identify Latitude = 0 or Longitude = 0 values.
- Check for incorrect positive Longitude values since California coordinates should be negative.
- Identify out-of-state or otherwise implausible coordinates.
- Create a summary of geographic data quality issues.

## Week 6
### Part 1: Feature Engineering and Market Metrics
- Create new variables to measure housing market performance.
- Calculate the following metrics:
  - Price Ratio: ClosePrice / OriginalListPrice
  - Price Per Sq Ft: ClosePrice / LivingArea
  - Days on Market: DaysOnMarket
  - Year: Derived from CloseDate
  - Month: Derived from CloseDate
  - YrMo: Year-month combination for time-series analysis
  - Close to Original List Ratio: ClosePrice / OriginalListPrice
  - Listing to Contract Days: PurchaseContractDate - ListingContractDate
  - Contract to Close Days: CloseDate - PurchaseContractDate

### Part 2: Segment Analysis
- Analyze market metrics across different property segments.
- Group data by (using groupby):
  - PropertyType
  - PropertySubType
  - CountyOrParish
  - MLSAreaMajor
  - ListOfficeName
  - BuyerOfficeName
- Generate summary statistics for each segment.
- Compare housing market performance across counties and property types.

## Week 7

### Part 1: Outlier Detection and Data Quality
- Identify extreme values that may distort market analysis.
- Use the Interquartile Range (IQR) method to detect outliers.
- Calculate Q1, Q3, and IQR for key numeric fields.
- Determine lower and upper bounds using:
  - Lower Bound = Q1 - 1.5 × IQR
  - Upper Bound = Q3 + 1.5 × IQR
- Apply outlier detection to:
  - ClosePrice
  - LivingArea
  - DaysOnMarket

### Part 2: Outlier Handling
- Create outlier flag columns instead of immediately deleting records.
- Preserve the original dataset with all records.
- Create a separate clean dataset with outliers filtered out.
- Compare the dataset before and after filtering.
- Compare median values before and after removing outliers.

## Week 8-10: Tableau Dashboard Development
- Import the cleaned and Residential-filtered datasets into Tableau.
- Connect the engineered market metrics to Tableau.

### Part 1:Market Analysis Dashboard
- Create monthly trends from January 2024 through the latest available month.
- Create visualizations for:
  - Monthly median close price
  - Average days on market
  - Average close-to-original-list price ratio
  - New listings
  - Closed sales
Add filters for: City,County, Zip Code/Postal Code, PropertySubType
And additional market analysis

