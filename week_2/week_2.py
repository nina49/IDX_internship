import pandas as pd
from pathlib import Path

current_dir = Path(__file__).resolve().parent
data_d = current_dir.parent.parent / "Data"

# Load the Cleaned Dataset from Week 1
df_listings = pd.read_csv(data_d / "Listing_Combined.csv", low_memory=False)
df_sold= pd.read_csv(data_d / "Sold_Combined.csv", low_memory=False)
print(f"Listing Dataset Rows,Columns: {df_listings.shape}")
print(f"Sold Dataset Rows,Columns: {df_sold.shape}")

# Missing Value for Listing
# Calculate missing counts and percentages per column
missing_counts_l = df_listings.isnull().sum()
missing_percentages_l = (missing_counts_l / len(df_listings)) * 100

df_missing_l = pd.DataFrame({
    'Missing Count': missing_counts_l,
    'Percentage (%)': missing_percentages_l
})

print("\n--- Missing Value Profile ---")
print(df_missing_l.sort_values(by='Percentage (%)', ascending=False).head(20))

# Missing Value for Sold
# Calculate missing counts and percentages per column
missing_counts_s = df_sold.isnull().sum()
missing_percentages_s = (missing_counts_s / len(df_sold)) * 100

df_missing_s= pd.DataFrame({
    'Missing Count': missing_counts_s,
    'Percentage (%)': missing_percentages_s
})

print("\n--- Missing Value Profile ---")
print(df_missing_s.sort_values(by='Percentage (%)', ascending=False).head(20))

# Columns with >90% missing values for listing
high_missing_l = df_missing_l[df_missing_l['Percentage (%)'] > 90].index.tolist()
print(f"\nColumns with >90% missing values ({len(high_missing_l )} total):")
print(high_missing_l)

# Columns with >90% missing values for sold
high_missing_s = df_missing_s[df_missing_s['Percentage (%)'] > 90].index.tolist()
print(f"\nColumns with >90% missing values ({len(high_missing_s )} total):")
print(high_missing_s)

print(df_listings.columns.tolist())


# Numeric Distribution for Listing
target_numeric_fields = [
    'ListPrice', 'OriginalListPrice', 'LivingArea', 
    'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 
    'DaysOnMarket', 'YearBuilt'
]

# Generate the comprehensive distribution summary table
distribution_summary_l = df_listings[target_numeric_fields].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
print("\n Numeric Distribution Summary for Listing Dataset")
print(distribution_summary_l)

distribution_summary_s = df_sold[target_numeric_fields].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
print("\n Numeric Distribution Summary for Sold Dataset")
print(distribution_summary_s)


## Listing: Dataset Rows,Columns: (480383, 81)

## Sold: Dataset Rows,Columns: (438115, 79)

##Concern : 100% empty Listing columns:ElementarySchoolDistrict,TaxAmount, TaxYear, 
# MiddleorJuniorSchoolDistrict, BusinessType, CoveredSpaces,AboveGradeFinishedArea,FireplacesTotal 
##100% empty Listing columns: TaxYear, MiddleOrJuniorSchoolDistrict, FireplacesTotal,
#AboveGradeFinishedArea,TaxAnnualAmount,CoveredSpaces,BusinessType, ElementarySchoolDistrict 

## >90% missing vals list: FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 
# 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 
# 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 
# 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict
#(13 total)

##>90% missing vals sold: WaterfrontYN', 'BasementYN', 'FireplacesTotal', 
# 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 
# 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 
# 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions',
#  'MiddleOrJuniorSchoolDistrict'
#(15 total)

##Drop: 8 100% missing columns for both
#LotSizeDimensions bc presence of LotSizeArea (adds little value), CoBuyerAgentFirstName:first names and doesn't help analyze real estate trends
##Keep: BuildingAreaTotal, BelowGradeFinishedArea important prectictor for house prices(add value to the property
#BuilderName:premium builders charge higher prices, maybe encode unknown for missing values

##Sold
# Keep: BuildingAreaTotal, BelowGradeFinishedArea, BuilderName, BasementYN, WaterfrontYN,



