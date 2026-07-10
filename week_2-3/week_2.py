import pandas as pd
from pathlib import Path

data_d= Path("./Data")

# Load the Dataset from Week 1 without the Residential Filter
listing= pd.read_csv(data_d / "Listing_Combined_2.csv", low_memory=False)
print(f"Listing Dataset(Before) Rows,Columns: {listing.shape}")

property_types= listing["PropertyType"].unique()
print(f"Unique property types in Listing Dataset:{property_types}")

#Suggested Question 1: Residential Vs Other Property Type Share for Listing Dataset
df_listing= listing[listing["PropertyType"]== "Residential"]
print(f"Listing Dataset(After) Rows,Columns: {df_listing.shape}")
residential_percent= (len(df_listing)/(len(listing)))*100
print(f"Percentage of Residential vs other property type share:{residential_percent}%")

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

#Histogram + Box Plot
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
sold= pd.read_csv(data_d / "Sold_Combined_2.csv", low_memory=False)
print(f"Sold Dataset(Before) Rows,Columns: {sold.shape}")

#Suggested Question 1: Residential Vs Other Property Type Share for Sold Dataset
df_sold= sold[sold["PropertyType"]== "Residential"].copy()
print(f"Sold Dataset(After) Rows,Columns: {df_sold.shape}")
residential_percent= (len(df_sold)/(len(sold)))*100
print(f"Percentage of Residential vs other property type share(Sold):{residential_percent}%")

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

#Histogram + Box Plot
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



#Suggested Question 2: Median and Average of Close Price
mean_close= df_sold["ClosePrice"].mean()
median_close=df_sold["ClosePrice"].quantile(0.5)
print(f"The median Close Price for Sold is: {median_close}")
print(f"The average(mean) Close Price for Sold is: {mean_close}")

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
df_sold["ListingDate_new"]=pd.to_datetime(df_sold['ListingContractDate'], errors= 'coerce')
df_sold["CloseDate_new"]=pd.to_datetime(df_sold['CloseDate'], errors='coerce')
check_error= len(df_sold[df_sold['CloseDate_new'] < df_sold['ListingDate_new']])
print(f"Rows with Timeline errors: {check_error}")
if check_error > 0:
    print("Data consistency issue found where Close Date is before Listing Contract Date")

#Suggested Question 6: Counties with the Highest Median Closing Prices
df_county= df_sold.groupby('CountyOrParish')[['ClosePrice']].agg('median')
df_county=df_county.sort_values(by='ClosePrice', ascending=False).reset_index()
print(df_county.head(10))


#                                          Listing Dataset
# After Residential Filter: Rows= 564,289  |  Columns=84
#Percentage of Residential vs other property type share: 63.56%

# >90% missing values (13): FireplacesTotal, AboveGradeFinishedArea, TaxAnnualAmount,
# BuilderName, TaxYear,ElementarySchoolDistrict,CoBuyerAgentFirstName, BelowGradeFinishedArea,
# BusinessType,CoveredSpaces, MiddleOrJuniorSchool, LotSizeDimensions, MiddleOrJuniorSchoolDistrict

#Percentile Summary
#ClosePrice:       min:525 | max:820,000,000 | mean:1,199,853 | median:850,000
#LivingArea:       min:0   | max:17,021,320  | mean:1,978.992 | median:1,670
#DaysOnMarket:     min:-58 | max:731         | mean:19.28     | median:10

#Total Outlier Percentage
# Highest Volatility:     LotSizeAcres:14.73% | DaysOnMarket:9.22%
# Moderate:               ListPrice:8.38%    | OriginalListPrice:8.22% | BathroomsTotalInteger:6.31%
#Stable (<5%):            Remaining key numeric columns range between 0.25% and 4.94%

#Histogram and Boxplot
#ClosePrice, ListPrice, OriginalListPrice, LivingArea, LotSizeAcres| heavily right skewed where the 
#histogram shows points around O, significant price differences of properties. (Cleaning: using Log Transformation)
#BathroomsTotalInteger: includes impossible extreme outlier of over 2,000 bathrooms
#BedroomsTotal: includes impossible extreme outlier of over 90 bedrooms
#DaysOnMarket: includes negative values which is not realistic
#Data Entry for BathroomsTotalInteger, BedroomsTotal, DaysOnMarket
#YearBuilt: left-skewed, nothing too concerning, includes outliers which are properties built around the 1800s

#                                         Sold Dataset
#After Residential Filter: Rows: 426,372 | Columns:82
#Percentage of Residential vs other property type share:67.16%
#>90% missing values (15): WaterfrontYN, BasementYN, FireplacesTotal, AboveGradeFinishedArea, 
# TaxAnnualAmount, BuilderName, TaxYear, BuildingAreaTotal, ElementarySchoolDistrict, CoBuyerAgentFirstName,
# BelowGradeFinishedArea, BusinessType, CoveredSpaces, LotSizeDimensions, MiddleOrJuniorSchoolDistrict

#Percentile Summary
#ClosePrice:       min:0   | max:989,500,000 | mean:1,191,405 | median:820,000
#LivingArea:       min:0   | max:17,021,320  | mean:1,978.992 | median:1,670
#DaysOnMarket:     min:0   | max:12,430      | mean:37.67     | median:19

#Total Outlier Percentage
# Highest Volatility:     LotSizeAcres:12.82%| DaysOnMarket:25.73%
# Moderate:               ListPrice:6.20%    | OriginalListPrice:6.18% | ClosePrice:6.85% 
#Stable (<5%):            Remaining key numeric columns range between 0.25% and 4.61%

#Histogram and Boxplot
#ClosePrice, ListPrice, OriginalListPrice, LivingArea, LotSizeAcres| heavily right skewed
#BathroomsTotalInteger and BedroomsTotal: extremely high outliers (reaching 175 bathrooms, 40+bedrooms)
#DaysOnMarket: extreme outlier of 12,000 days equivalent to 33 years (could be dead listing)
#YearBuilt: only one left skewed and has historic outliers(properties built in the 1800s)

#Suggested Question (answered using Sold Dataset)
#1: Percentage of Residential vs other property type share:67.16%
#2: ClosePrice: median:820,000 | mean:1,191,405
#3: DaysOn Market: heavily rightly skewed with extreme outlier (25.73% of the data), max of 12,430 with median 10
#4:ClosingPrice > ListPrice: 39.93% |ClosingPrice < ListPrice: 42.69% | ClosingPrice = ListPrice: 17.38% 
#5:CloseDate before ListingContractDate: 63 rows | DaysOnMarket have negative values
#6:
 # CountyOrParish  ClosePrice
#1     Del Norte   2485000.0
#2   Other County   2462500.0
#3      San Mateo   1700000.0
#4    Santa Clara   1600000.0
#5     Santa Cruz   1200000.0
#6  San Francisco   1189870.0
#7         Orange   1175000.0
#8          Marin   1165000.0
#9        Alameda   1130000.0
#10         Alpine   1100000.0
