import pandas as pd
from pathlib import Path
data_4= Path("./Data")

#Listing
df_listing= pd.read_csv(data_4 / "Listing_Combined.csv", low_memory=False)
print(f"Number of rows,columns{df_listing.shape}")
df_cleaned = df_listing.copy()

#Dropping >90% missing values for Listing
missing_count_l= df_cleaned.isnull().sum()
missing_percentage_l=(missing_count_l/len(df_cleaned))*100
df_missing_l= pd.DataFrame({
    'Missing Count': missing_count_l,
    'Percentage(%)': missing_percentage_l
})

high_missing_l= df_missing_l[df_missing_l["Percentage(%)"]>90]
columns_to_drop = high_missing_l.index.tolist()
df_cleaned = df_cleaned.drop(columns=columns_to_drop)
print(f"Dropped {len(columns_to_drop)} columns (Listing): {columns_to_drop}")

#Converting the dates for Listing
date_columns=["CloseDate","PurchaseContractDate","ListingContractDate","ContractStatusChangeDate"]
print("Before conversion (Listing), data types:")
print(df_listing[date_columns].dtypes)
for col in date_columns:
    df_cleaned[col]=pd.to_datetime(df_cleaned[col],errors="coerce")
print("After conversion (Listing), data types:")
print(df_cleaned[date_columns].dtypes)

#Flagging Date Inconsistency columns for Listing
df_cleaned["listing_after_close"] = df_cleaned["ListingContractDate"] > df_cleaned["CloseDate"]
df_cleaned["purchase_after_close"] = df_cleaned["PurchaseContractDate"] > df_cleaned["CloseDate"]
df_cleaned["purchase_after_listing"] = df_cleaned["ListingContractDate"] > df_cleaned["PurchaseContractDate"]
print(f"Listing after close (Listing): {df_cleaned['listing_after_close'].sum()}")
print(f"Purchase after close (Listing): {df_cleaned['purchase_after_close'].sum()}")
print(f"Purchase after listing (Listing): {df_cleaned['purchase_after_listing'].sum()}")

#Flagging Invalid Numeric Values(Close Price, Living Area and Days On Market) for Listing
df_cleaned["close_price_invalid"] = df_cleaned["ClosePrice"] <= 0
df_cleaned["living_area_invalid"] = df_cleaned["LivingArea"] <= 0
df_cleaned["dom_invalid"] = df_cleaned["DaysOnMarket"] < 0
df_cleaned["bedroom_and_bathroom_invalid"] = (df_cleaned["BedroomsTotal"] < 0) | (df_cleaned["BathroomsTotalInteger"] < 0)

print(f"Number of rows with invalid Close Price (<= 0) (Listing): {df_cleaned['close_price_invalid'].sum()}")
print(f"Number of rows with invalid Living Area (<= 0) (Listing): {df_cleaned['living_area_invalid'].sum()} ")
print(f"Number of rows with invalid Days on Market (< 0) (Listing): {df_cleaned['dom_invalid'].sum()}")
print(f"Number of rows with invalid Bedroom and Bathroom (< 0) (Listing): {df_cleaned['bedroom_and_bathroom_invalid'].sum()}")

#Geographic Data Check for Listing
df_cleaned["coords_empty"] = df_cleaned["Latitude"].isna() | df_cleaned["Longitude"].isna()
df_cleaned["coords_zero"] = (df_cleaned["Latitude"] == 0) | (df_cleaned["Longitude"] == 0)
df_cleaned["longitude_outside_california"] = df_cleaned["Longitude"] > 0
df_cleaned["coords_implausible"] = (df_cleaned["Latitude"] < 32.5) | (df_cleaned["Latitude"] > 42.0) | (df_cleaned["Longitude"] < -124.5) | (df_cleaned["Longitude"] > -114.0)

print(f"Coordinates with empty values (Listing): {df_cleaned['coords_empty'].sum()}")
print(f"Zero Coordinates (Listing): {df_cleaned['coords_zero'].sum()}")
print(f"Positive Longitude/outside california (Listing): {df_cleaned['longitude_outside_california'].sum()}")
print(f"Implausible/Out of State Coordinates (Listing): {df_cleaned['coords_implausible'].sum()}")

#Sold
df_sold= pd.read_csv(data_4 / "Sold_Combined.csv", low_memory=False)
print(f"Number of rows,columns{df_sold.shape}")
df_cleaned_s = df_sold.copy()

#Dropping >90% missing values for Listing
missing_count_s= df_cleaned_s.isnull().sum()
missing_percentage_s=(missing_count_s/len(df_cleaned_s))*100
df_missing_s= pd.DataFrame({
    'Missing Count': missing_count_s,
    'Percentage(%)': missing_percentage_s
})

high_missing_s= df_missing_s[df_missing_s["Percentage(%)"]>90]
columns_to_drop = high_missing_s.index.tolist()
df_cleaned_s = df_cleaned_s.drop(columns=columns_to_drop)
print(f"Dropped {len(columns_to_drop)} columns (Sold): {columns_to_drop}")

# Converting the dates for Sold
print("Before conversion, data types (Sold):")
print(df_sold[date_columns].dtypes)
for col in date_columns:
    df_cleaned_s[col] = pd.to_datetime(df_cleaned_s[col], errors="coerce")
print("After conversion, data types (Sold):")
print(df_cleaned_s[date_columns].dtypes)

# Flagging Date Inconsistency columns for Sold
df_cleaned_s["listing_after_close"] = df_cleaned_s["ListingContractDate"] > df_cleaned_s["CloseDate"]
df_cleaned_s["purchase_after_close"] = df_cleaned_s["PurchaseContractDate"] > df_cleaned_s["CloseDate"]
df_cleaned_s["purchase_after_listing"] = df_cleaned_s["ListingContractDate"] > df_cleaned_s["PurchaseContractDate"]

print(f"Listing after close (Sold): {df_cleaned_s['listing_after_close'].sum()}")
print(f"Purchase after close (Sold): {df_cleaned_s['purchase_after_close'].sum()}")
print(f"Purchase after listing (Sold): {df_cleaned_s['purchase_after_listing'].sum()}")

# Flagging Invalid Numeric Values (Close Price, Living Area and Days On Market) for Sold
df_cleaned_s["close_price_invalid"] = df_cleaned_s["ClosePrice"] <= 0
df_cleaned_s["living_area_invalid"] = df_cleaned_s["LivingArea"] <= 0
df_cleaned_s["dom_invalid"] = df_cleaned_s["DaysOnMarket"] < 0
df_cleaned_s["bedroom_or_bathroom_invalid"] = (df_cleaned_s["BedroomsTotal"] < 0) | (df_cleaned_s["BathroomsTotalInteger"] < 0)

print(f"Number of rows with invalid Close Price (<= 0) (Sold): {df_cleaned_s['close_price_invalid'].sum()}")
print(f"Number of rows with invalid Living Area (<= 0) (Sold): {df_cleaned_s['living_area_invalid'].sum()}")
print(f"Number of rows with invalid Days on Market (< 0) (Sold): {df_cleaned_s['dom_invalid'].sum()}")
print(f"Number of rows with invalid Bedroom or Bathroom (< 0) (Sold): {df_cleaned_s['bedroom_or_bathroom_invalid'].sum()}")

# Geographic Data Check for Sold
df_cleaned_s["coords_empty"] = df_cleaned_s["Latitude"].isna() | df_cleaned_s["Longitude"].isna()
df_cleaned_s["coords_zero"] = (df_cleaned_s["Latitude"] == 0) | (df_cleaned_s["Longitude"] == 0)
df_cleaned_s["longitude_outside_california"] = df_cleaned_s["Longitude"] > 0
df_cleaned_s["coords_implausible"] = (df_cleaned_s["Latitude"] < 32.5) | (df_cleaned_s["Latitude"] > 42.0) | (df_cleaned_s["Longitude"] < -124.5) | (df_cleaned_s["Longitude"] > -114.0)

print(f"Coordinates with empty values (Sold): {df_cleaned_s['coords_empty'].sum()}")
print(f"Zero Coordinates (Sold): {df_cleaned_s['coords_zero'].sum()}")
print(f"Positive Longitude/outside california (Sold): {df_cleaned_s['longitude_outside_california'].sum()}")
print(f"Implausible/Out of State Coordinates (Sold): {df_cleaned_s['coords_implausible'].sum()}")


#Results

#                                                  Listing
# Starting: Rows, Columns: (564289, 84)
#Dropped 13 columns >90% Missing: 
# ['FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', '
# BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 
# 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict']

#Before conversion  data types:         
#CloseDate                   object
#PurchaseContractDate        object
#ListingContractDate         object
#ContractStatusChangeDate    object

#After conversion, data types:
#CloseDate                   datetime64[ns]
#PurchaseContractDate        datetime64[ns]
#ListingContractDate         datetime64[ns]
#ContractStatusChangeDate    datetime64[ns]

#Number of rows with Date Inconsistency
#Listing after close : 75
#Purchase after close : 262
#Purchase after listing : 281

# Number of rows with nvalid Values 
#Close Price (<= 0) (Listing): 0
#Living Area (<= 0) (Listing): 370 
#Days on Market (< 0) (Listing): 27
#Bedroom and Bathroom (< 0) (Listing): 0

#Geographic Data Check
#Coordinates with empty values: 80408
#Zero Coordinates: 69
#Positive Longitude/outside california: 76
#Implausible/Out of State Coordinates: 323

#                                                Sold
#Starting: Rows,Columns : 426372, 82
#Dropped 15 columns (Sold): ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea',
# 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 
# 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict']
#Before conversion, data types (Sold):
#CloseDate                   object
#PurchaseContractDate        object
#ListingContractDate         object
#ContractStatusChangeDate    object

#After conversion, data types (Sold):
#CloseDate                   datetime64[ns]
#PurchaseContractDate        datetime64[ns]
#ListingContractDate         datetime64[ns]
#ContractStatusChangeDate    datetime64[ns]

#Number of rows with Date Inconsistency
#Listing after close : 63
#Purchase after close : 240
#Purchase after listing : 277

#Number of rows with Invalid values
#Number of rows with invalid Close Price (<= 0) : 1
#Number of rows with invalid Living Area (<= 0) : 155
#Number of rows with invalid Days on Market (< 0): 48
#Number of rows with invalid Bedroom or Bathroom (< 0): 0

#Geographic Data Check
#Coordinates with empty values: 16041
#Zero Coordinates: 30
#Positive Longitude/outside california: 32
#Implausible/Out of State Coordinates: 94
