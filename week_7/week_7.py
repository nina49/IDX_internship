import pandas as pd
from pathlib import Path
data_7=Path("./Data")
df_listing= pd.read_csv(data_7/"Listing_with_district.csv", low_memory=False)
df_sold=pd.read_csv(data_7/"Sold_with_district.csv", low_memory=False)

#Outlier Filter on Listing 
key_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]
df_listing["outlier_flag"] = False

for col in key_cols:
    if col not in df_listing.columns:
        continue

    Q1 = df_listing[col].quantile(0.25)
    Q3 = df_listing[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    iqr_outlier = (df_listing[col] < lower) | (df_listing[col] > upper)
    negative_value = df_listing[col] < 0

    df_listing["outlier_flag"] = df_listing["outlier_flag"]| iqr_outlier | negative_value
total_flagged = df_listing[df_listing["outlier_flag"]]
print(f"There are {len(total_flagged)} outliers:\n{total_flagged}")
df_listing_filtered = df_listing[df_listing["outlier_flag"] == False].copy()

#Before Filter Listing Statistic
print(f"Number of rows, columns (Listing): {df_listing.shape}")
starting_cols = [col for col in key_cols if col in df_listing.columns]
print(df_listing[starting_cols].describe())

#After Filter
print(f"Number of rows, columns (Listing) filtered: {df_listing_filtered.shape}")
final_cols = [col for col in key_cols if col in df_listing_filtered.columns]
print(df_listing_filtered[final_cols].describe())
df_listing_filtered.to_csv(data_7 / "Listing_outlier_filtered.csv", index=False)
df_listing.to_csv(data_7/"Sold_outliers_flag.csv",index=False)

#Outlier Filter on Sold
df_sold["outlier_flag"] = False

for col in key_cols:
    Q1 = df_sold[col].quantile(0.25)
    Q3 = df_sold[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    iqr_outlier = (df_sold[col] < lower) | (df_sold[col] > upper)
    negative_value = df_sold[col] < 0

    df_sold["outlier_flag"] = df_sold["outlier_flag"]| iqr_outlier | negative_value
total_flagged_s = df_sold[df_sold["outlier_flag"]]
print(f"There are {len(total_flagged_s)} outliers:\n{total_flagged_s}")
df_sold_filtered = df_sold[df_sold["outlier_flag"] == False].copy()

#Before Filter Sold Statistic
print(f"Number of rows, columns (Sold): {df_sold.shape}")
starting_cols_s = [col for col in key_cols if col in df_sold.columns]
print(df_sold[starting_cols_s].describe())

#After Filter
print(f"Number of rows, columns (Sold) filtered: {df_sold_filtered.shape}")
final_cols_s = [col for col in key_cols if col in df_sold_filtered.columns]
print(df_sold_filtered[final_cols_s].describe())
df_sold_filtered.to_csv(data_7 / "Sold_outlier_filtered.csv", index=False)
df_sold.to_csv(data_7/"Sold_outlier_flag.csv",index=False)

                                            #Results
                                            
                                            #Listing
#Before rows,columns: 564289, 52
#After rows,columns:  481097, 53
#Flagged 83192 outliers 

#Before Filter
#        ClosePrice    LivingArea   DaysOnMarket
#count  1.508810e+05  5.637290e+05  564289.000000
#mean   1.199853e+06  1.978992e+03      19.278148
#std    4.227119e+06  2.287875e+04      27.314731
#min    5.250000e+02  0.000000e+00     -58.000000
#25%    5.998000e+05  1.248000e+03       5.000000
#50%    8.500000e+05  1.670000e+03      10.000000
#75%    1.350000e+06  2.300000e+03      22.000000
#max    8.200000e+08  1.702132e+07     731.000000

#After Filter
#ClosePrice     LivingArea   DaysOnMarket
#count  1.169680e+05  480626.000000  481097.000000
#mean   9.462760e+05    1741.517205      12.109909
#std    4.865246e+05     701.998496      10.159534
#min    5.250000e+02       0.000000       0.000000
#25%    5.900000e+05    1222.000000       5.000000
#50%    8.250000e+05    1611.000000       9.000000
#75%    1.220000e+06    2145.000000      18.000000
#max    2.475000e+06    3878.000000      47.000000
                                              
                                               #Sold 
#Before rows,columns: 426372, 55
#After rows,columns:  359806, 56
#Flagged 66566 outliers 

#Before Filter
#ClosePrice    LivingArea   DaysOnMarket
#count  4.263700e+05  4.261340e+05  426372.000000
#mean   1.191405e+06  1.902620e+03      37.672084
#std    6.201901e+06  2.609139e+04      53.860324
#min    0.000000e+00  0.000000e+00    -288.000000
#25%    5.750000e+05  1.248000e+03       8.000000
#50%    8.200000e+05  1.642000e+03      19.000000
#75%    1.300000e+06  2.220000e+03      49.000000
#max    9.895000e+08  1.702132e+07   12430.000000

#After Filter
#      ClosePrice     LivingArea   DaysOnMarket
#count  3.598050e+05  359704.000000  359806.000000
#mean   8.979786e+05    1674.936574      26.609031
#std    4.602358e+05     628.434538      25.985475
#min    0.000000e+00       0.000000       0.000000
#25%    5.625000e+05    1212.000000       7.000000
#50%    7.850000e+05    1569.000000      16.000000
#75%    1.150000e+06    2037.000000      39.000000
#max    2.387500e+06    3678.000000     110.000000
