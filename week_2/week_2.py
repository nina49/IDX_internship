import pandas as pd
from pathlib import Path

data_d= Path("./Data")

# Load the Cleaned Dataset from Week 1
df_listing= pd.read_csv(data_d / "Listing_Combined_2.csv", low_memory=False)
print(f"Listing Dataset Rows,Columns: {df_listing.shape}")

property_types= df_listing["PropertyType"].unique()
print(f"Unique property types in Listing Dataset:{property_types}")

# Missing Value Count and Percentage for Listing
missing_count_l= df_listing.isnull().sum()
missing_percentage_l=(missing_count_l/len(df_listing))*100
df_missing_l= pd.DataFrame({
    'Missing Count': missing_count_l,
    'Percentage(%)': missing_percentage_l
})
print("Missing Values of Lisitings")
print(df_missing_l.sort_values(by="Percentage(%)",ascending=False).head(15))

#Flag >90% missing values for listing
high_missing_l= df_missing_l[df_missing_l["Percentage(%)"]>90]
print(f"There are {len(high_missing_l)} columns with >90% missing values and include:")
for col in high_missing_l.index:
    per= round(high_missing_l.loc[col,"Percentage(%)"],2)
    print(f"-{col} : {per}")

# Check Datatypes of Key Numerical Fields
key_columns=['ClosePrice','ListPrice','OriginalListPrice','LivingArea','LotSizeAcres',
             'BedroomsTotal','BathroomsTotalInteger','DaysOnMarket','YearBuilt']
print("Data Types of key numeric fields:")
print(df_listing[key_columns].dtypes)

# Percentile Summary for Listing
percentile_summary_l= df_listing[key_columns].describe(percentiles= [0.1, 0.25, 0.5, 0.75, 0.9])
print("Percentile Summary for Listing")
print(percentile_summary_l)

#Outliers using IQR
Q1= df_listing[key_columns].quantile(0.25)
Q3= df_listing[key_columns].quantile(0.75)
IQR=Q3-Q1
lower_bound= Q1-1.5 * IQR
upper_bound= Q3+1.5 * IQR
lower_outlier_l= (df_listing[key_columns] < lower_bound).sum()
upper_outlier_l=(df_listing[key_columns]> upper_bound).sum()
total_outlier= lower_outlier_l + upper_outlier_l
outlier_percent= round((total_outlier/len(df_listing[key_columns]))*100,2)
print(f"Lower Outlier of Key Columns: \n{lower_outlier_l}")
print(f"Upper Outlier of Key Columns: \n{upper_outlier_l}")
print(f"Total outliers (%): \n{outlier_percent}")

#Visualization + Box Plot
import matplotlib.pyplot as plt
import seaborn as sns

for col in key_columns:
    column_data= df_listing[col]
    fig,axes = plt.subplots(2,1, figsize=(10,8))
    sns.histplot(data=column_data, kde=True, ax=axes[0], color='skyblue', bins=30)
    axes[0].set_title(f'{col} - Histogram Distribution for Listing')
    axes[0].set_xlabel(col)
    axes[0].set_ylabel('Count')
    
    #Boxplot
    sns.boxplot(x=column_data, ax=axes[1], color='red')
    axes[1].set_title(f'{col} - Boxplot for Listing')
    axes[1].set_xlabel(col)
    
    plt.tight_layout()
    plt.show()
    print("\n" + "="*70 + "\n")

#Sold Dataset
df_sold= pd.read_csv(data_d / "Sold_Combined_2.csv", low_memory=False)
print(f"Sold Dataset Rows,Columns: {df_sold.shape}")

#Missing Value Count and Percentage of Sold
missing_count_s= df_sold.isnull().sum()
missing_percentage_s= missing_count_s/len(df_sold)*100
df_missing_s= pd.DataFrame({
    'Missing Count': missing_count_s,
    'Percentage(%)': missing_percentage_s
})
print("Missing Values of Sold")
print(df_missing_s.sort_values(by='Percentage(%)', ascending=False).head(15))

#Flag >90% missing values for sold
high_missing_s= df_missing_s[df_missing_s["Percentage(%)"]>90]
print(f"There are {len(high_missing_s)} columns with >90% missing values and include:")
for col in high_missing_s.index:
    per= round(high_missing_s.loc[col,"Percentage(%)"],2)
    print(f"-{col} : {per}")

#Percentile Summary for Sold
percentile_summary_s= df_sold[key_columns].describe(percentiles=[0.1,0.25,0.5,0.75,0.9])
print("Percentile Summary for Sold")
print(percentile_summary_s)

#Outliers using IQR
Q1=df_sold[key_columns].quantile(0.25)
Q3=df_sold[key_columns].quantile(0.75)
#Already set up equations for lower bound, upper bound and IQR 
lower_outlier_s= (df_sold[key_columns] < lower_bound). sum()
upper_outlier_s= (df_sold[key_columns] > upper_bound).sum()
total_outlier_s= lower_outlier_s + upper_outlier_s
outlier_percent_s= round(total_outlier_s/len(df_sold[key_columns])*100,2)
print(f"Lower Outlier of Key Columns for Sold: \n{lower_outlier_s}")
print(f"Upper Outlier of Key Columns for Sold: \n{upper_outlier_s}")
print(f"Total Outliers (%): \n{outlier_percent_s}")

#Visualization + Box Plot
for col in key_columns:
    column_data_s= df_sold[col]
    fig,axes= plt.subplots(2,1, figsize=(10,8))
    sns.histplot(data=column_data_s, kde=True, ax=axes[0], color= 'lightgreen', bins=30)
    axes[0].set_title(f'{col} - Histogram Distribution for Sold')
    axes[0].set_xlabel(col)
    axes[0].set_ylabel("Count")

    #Boxplot
    sns.boxplot(x=column_data_s, ax=axes[1], color= "purple")
    axes[1].set_title(f'{col} -Boxplot for Sold')
    axes[1].set_xlabel(col)

    plt.tight_layout()
    plt.show()
    print("\n" + "="*70 + "\n")

#Suggested Question 1: Residential Vs Other Property Type Share
df_residential_l= df_listing[df_listing["PropertyType"]== "Residential"]
print(f"Number of rows for Residential (Listing):{(len(df_residential_l))} ")
residential_percent= (len(df_residential_l)/(len(df_listing)))*100
print(f"Percentage of Residential vs other property type share:{residential_percent}%")

#Suggested Question 2: Median and Average of Close Price
mean_close= df_sold["ClosePrice"].mean()
median_close=df_sold["ClosePrice"].quantile(0.5)
print(f"The median Close Price for Listing is: {median_close}")
print(f"The average(mean) Close Price for Listing is: {mean_close}")

#Suggested Question 3: Days on Market Distribution


#Suggested Question 4: Percentage of Homes Sold above vs below list price
above_count= (df_sold['ClosePrice'] > df_sold['ListPrice']).sum()
below_count= (df_sold['ClosePrice'] < df_sold['ListPrice']).sum()
at_count=(df_sold['ClosePrice'] == df_sold['ListPrice']).sum()
above_percent= (above_count/len(df_sold))*100
below_percent= (below_count/len(df_sold))*100
at_percent=(at_count/len(df_sold))*100
print(f"Percentage of homes sold above the list price: {above_percent:.2f}%")
print(f"Percentage of homes sold below the listing price:{below_percent:.2f}%")
print(f"Percentage of homes sold at the listing price:{at_percent:.2f}%")

#Suggested Question 5: Inconsistency (List Date Vs Close Date)
df_listing["ListingDate_new"]=pd.to_datetime(df_listing['ListingContractDate'], errors= 'coerce')
df_listing["CloseDate_new"]=pd.to_datetime(df_listing['CloseDate'], errors='coerce')
check_error= len(df_listing[df_listing['CloseDate_new'] < df_listing['ListingDate_new']])
print(f"Rows with Timeline errors: {check_error}")
if check_error > 0:
    print("Data consistency issue found where Close Date is before Listing Contract Date")

#Suggested Question 6: Counties with the Highest Median Closing Prices
df_county= df_sold.groupby('CountyOrParish')[['ClosePrice']].agg('median').reset_index()
df_county=df_county.sort_values(by='ClosePrice', ascending=False)
print(df_county.head(10))

## Listing: Dataset Rows,Columns: (480383, 81)


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



list_cols = [col for col in df_listing.columns if col.startswith('List')]
print(list_cols)