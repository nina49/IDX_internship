import pandas as pd
from pathlib import Path
data_4= Path("./Data")

#Listing
df_listing= pd.read_csv(data_4 / "CRMLSListing_MortgageR.csv", low_memory=False)
print(f"Number of rows,columns{df_listing.shape}")

df_cleaned = df_listing.copy()

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

#Dropping Columns 
print(f"Number of rows,column before column drop{df_cleaned.shape}")


# Identifying >90% missing values for Listing
missing_count_l= df_cleaned.isnull().sum()
missing_percentage_l=(missing_count_l/len(df_cleaned))*100
df_missing_l= pd.DataFrame({
    'Missing Count': missing_count_l,
    'Percentage(%)': missing_percentage_l
})

high_missing_l= df_missing_l[df_missing_l["Percentage(%)"]>90]
missing_vals_l = high_missing_l.index.tolist()
print(f"Dropped {len(missing_vals_l)} columns (Listing):{missing_vals_l}")

#Listing out all the columns in Listing CSV
df_cleaned.columns.tolist()

#Identifying merging duplicates with .1 at the end of the column names
merge_duplicates = [col for col in df_cleaned.columns if col.endswith('.1')]
print(f"Dropped {len(merge_duplicates)} columns(Listing): {merge_duplicates}")

#Dropping >90% Missing Values + Merge Duplicates
df_cleaned=df_cleaned.drop(columns=merge_duplicates + missing_vals_l ,errors='ignore')

#Categorizing the columns based on analytical value

#Fully retain: essential for analysis
key_columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "rate_30yr_fixed",
]
#Fully retain for now: drop later
flag_columns = [
    "listing_after_close",
    "purchase_after_close",
    "purchase_after_listing",
    "close_price_invalid",
    "living_area_invalid",
    "dom_invalid",
    "bedroom_and_bathroom_invalid",
    "coords_empty",
    "coords_zero",
    "longitude_outside_california",
    "coords_implausible",
]
#Fully retain: essential for analysis
columns_date = [
    "year_month",
    "ListingContractDate",
    "PurchaseContractDate",
    "CloseDate",
    "ContractStatusChangeDate",
]
#Mostly retain
location_columns = [
    "City",
    "PostalCode",
    "CountyOrParish",
    "StateOrProvince",
    "Latitude",
    "Longitude",
    "UnparsedAddress",
    "MLSAreaMajor",
    "SubdivisionName",
]
#Dropping candidate
#Too many unique value + high missing values: SubdivisionName,UnparsedAddress,MLSAreaMajor

#Mostly retain
property_details = [
    "PropertyType",
    "PropertySubType",
    "MlsStatus",
    "LotSizeSquareFeet",
    "LotSizeArea",
    "MainLevelBedrooms",
    "GarageSpaces",
    "ParkingTotal",
    "Stories",
    "Levels",
    "AttachedGarageYN",
    "FireplaceYN",
    "NewConstructionYN",
    "AssociationFee",
    "AssociationFeeFrequency",
]
#Droping Candidate: 
#Similar columns exists: AttachedGarageYN, LotSizeArea
#Redudant columns: AssociationFee, AssociationFeeFrequency, FireplaceYN, Levels, Stories, GarageSpaces

# Mostly Drop
agent_and_office_columns = [
    "ListAgentEmail",
    "ListAgentFirstName",
    "ListAgentLastName",
    "ListAgentFullName",
    "CoListAgentFirstName",
    "CoListAgentLastName",
    "BuyerAgentMlsId",
    "BuyerAgentFirstName",
    "BuyerAgentLastName",
    "ListOfficeName",
    "BuyerOfficeName",
    "CoListOfficeName",
    "BuyerOfficeAOR",
    "BuyerAgencyCompensation",
    "BuyerAgencyCompensationType",
]
#Dropping Candidate:
# Redudant Information: ListAgentEmail,ListAgentFirstName,ListAgentLastName,CoListAgentFirstName
#CoListAgentLastName, CoListOfficeName
# BuyerAgencyCompensation, BuyerAgencyCompensationType: redundancy + (86% missing)
# Too many unique value + similar columns exist: BuyerAgentMlsId,BuyerAgentFirstName, BuyerAgentLastName

#Mostly Drop
system_and_school_columns = [
    "ListingKey",
    "ListingKeyNumeric",
    "ListingId",
    "StreetNumberNumeric",
    "ElementarySchool",
    "MiddleOrJuniorSchool",
    "HighSchool",
    "HighSchoolDistrict",
]
#Drop Candidates:
#Similar columns exists: ListingKeyNumeric,StreetNumberNumeric, ListingID
#Redundant + High Missing Values (>85%):ElementarySchool,MiddleOrJuniorSchool,HighSchool,HighSchoolDistrict

#Column Check
df_count = len(df_cleaned.columns)

#Total columns in the categorized lists
categorized_lists_l = [key_columns, flag_columns, columns_date, location_columns, property_details, 
                     agent_and_office_columns,system_and_school_columns]

print(f"Total columns in DataFrame: {df_count}")
print(f"Total columns categorized:  {sum(len(lst) for lst in categorized_lists_l)}")

# List of redundant IDs, high-null school/hoa fields, and non-essential property attributes
cols_to_drop = [
    "ListingKeyNumeric",
    "StreetNumberNumeric",
    "ListingID",
    "ElementarySchool",
    "MiddleOrJuniorSchool",
    "HighSchool",
    "HighSchoolDistrict",
    "SubdivisionName",
    "UnparsedAddress",
    "AttachedGarageYN",
    "LotSizeArea",
    "AssociationFee",
    "AssociationFeeFrequency",
    "FireplaceYN",
    "Levels",
    "Stories",
    "GarageSpaces",
    "BuyerAgencyCompensation",
    "BuyerAgencyCompensationType",
    "ListAgentEmail",
    "ListAgentFirstName",
    "ListAgentLastName",
    "CoListAgentFirstName",
    "CoListAgentLastName",
    "CoListOfficeName",
    "BuyerAgentMlsId",
    "BuyerAgentFirstName",
    "BuyerAgentLastName",
]

# Drop columns from listing datasets (safely checking if column exists)
df_cleaned = df_cleaned.drop(columns=[col for col in cols_to_drop if col in df_cleaned.columns])
print(f"Dropped {len(cols_to_drop)} columns")
print(f"Total number of dropped listing columns: { len(cols_to_drop) + len(merge_duplicates)+ len(missing_vals_l)} columns")


#Sold
df_sold= pd.read_csv(data_4 / "Sold_Combined.csv", low_memory=False)
print(f"Number of rows,columns{df_sold.shape}")
df_cleaned_s = df_sold.copy()

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
df_cleaned_s["bedroom_and_bathroom_invalid"] = (df_cleaned_s["BedroomsTotal"] < 0) | (df_cleaned_s["BathroomsTotalInteger"] < 0)

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

#Dropping Columns >90% missing values for Listing
missing_count_s= df_cleaned_s.isnull().sum()
missing_percentage_s=(missing_count_s/len(df_cleaned_s))*100
df_missing_s= pd.DataFrame({
    'Missing Count': missing_count_s,
    'Percentage(%)': missing_percentage_s
})

high_missing_s= df_missing_s[df_missing_s["Percentage(%)"]>90]
missing_vals_s  = high_missing_s.index.tolist()
df_cleaned_s =df_cleaned_s.drop(columns= missing_vals_s ,errors='ignore')
print(f"Dropped {len(missing_vals_s )} columns (Sold): {missing_vals_s }")

#Listing out all the columns in Listing CSV
df_cleaned_s.columns.tolist()

#Difference between columns Listing and Sold
list1 = [col for sublist in categorized_lists_l for col in sublist]
list2 = ['BuyerAgentAOR',
 'ListAgentAOR',
 'Flooring',
 'ViewYN',
 'PoolPrivateYN',
 'OriginalListPrice',
 'ListingKey',
 'ListAgentEmail',
 'CloseDate',
 'ClosePrice',
 'ListAgentFirstName',
 'ListAgentLastName',
 'Latitude',
 'Longitude',
 'UnparsedAddress',
 'PropertyType',
 'LivingArea',
 'ListPrice',
 'DaysOnMarket',
 'ListOfficeName',
 'BuyerOfficeName',
 'CoListOfficeName',
 'ListAgentFullName',
 'CoListAgentFirstName',
 'CoListAgentLastName',
 'BuyerAgentMlsId',
 'BuyerAgentFirstName',
 'BuyerAgentLastName',
 'AssociationFeeFrequency',
 'ListingKeyNumeric',
 'MLSAreaMajor',
 'CountyOrParish',
 'MlsStatus',
 'ElementarySchool',
 'AttachedGarageYN',
 'ParkingTotal',
 'PropertySubType',
 'LotSizeAcres',
 'SubdivisionName',
 'BuyerOfficeAOR',
 'YearBuilt',
 'StreetNumberNumeric',
 'ListingId',
 'BathroomsTotalInteger',
 'City',
 'BedroomsTotal',
 'ContractStatusChangeDate',
 'PurchaseContractDate',
 'ListingContractDate',
 'StateOrProvince',
 'MiddleOrJuniorSchool',
 'FireplaceYN',
 'Stories',
 'HighSchool',
 'Levels',
 'LotSizeArea',
 'MainLevelBedrooms',
 'NewConstructionYN',
 'GarageSpaces',
 'HighSchoolDistrict',
 'PostalCode',
 'AssociationFee',
 'LotSizeSquareFeet',
 'OriginatingSystemName',
 'OriginatingSystemSubName',
 'BuyerAgencyCompensationType',
 'BuyerAgencyCompensation',
 'listing_after_close',
 'purchase_after_close',
 'purchase_after_listing',
 'close_price_invalid',
 'living_area_invalid',
 'dom_invalid',
 'bedroom_and_bathroom_invalid',
 'coords_empty',
 'coords_zero',
 'longitude_outside_california',
 'coords_implausible']

# Convert lists to sets
set1, set2 = set(list1), set(list2)
only_in_list1 = list(set1 - set2)
only_in_list2 = list(set2 - set1)

print(f"Columns only in List 1(Listing) ({len(only_in_list1)}): {only_in_list1}")
print(f"Columns only in List 2(Sold) ({len(only_in_list2)}): {only_in_list2}")

#Unique List Columns: rate_30yr_fixed, year_month (not part of drop column for listing)
#Unique Sold Columns
#'PoolPrivateYN', 'OriginatingSystemSubName','BuyerAgentAOR', 'ViewYN', 
#'Flooring', 'OriginatingSystemName', 'ListAgentAOR'

#Drop:
#OriginatingSystemSubName,OriginatingSystemName: no predictive value

cols_to_drop_s= cols_to_drop +["OriginatingSystemSubName", "OriginatingSystemName"]

# Drop columns from solddatasets (safely checking if column exists)
df_cleaned_s = df_cleaned_s.drop(columns=[col for col in cols_to_drop_s if col in df_cleaned_s.columns])
print(f"Dropped {len(cols_to_drop_s)} columns")
print(f"Total number of dropped sold columns: { len(cols_to_drop_s) + len(missing_vals_s)} columns")

#Cleaned Datasets into CSVs
df_cleaned.to_csv("./Data/Cleaned_Listing.csv", index=False)
df_cleaned_s.to_csv("./Data/Cleaned_Sold.csv", index=False)







#Results

#                                                  Listing
# Starting: Rows, Columns: (564289, 86)
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
