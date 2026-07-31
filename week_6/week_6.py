import pandas as pd
from pathlib import Path
data_5= Path("./Data")
df_listing= pd.read_csv(data_5/"Cleaned_Listing(with_flag).csv", low_memory=False)
df_sold=pd.read_csv(data_5/"Cleaned_Sold(with_flag).csv", low_memory=False)

#Convert metrics used for analysis to datetime format for Listing
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate']
print(df_listing[date_cols].dtypes)
for col in date_cols:
    df_listing[col]=pd.to_datetime(df_listing[col])
print(df_listing[date_cols].dtypes)

# Object to datetime format for sold
print(df_sold[date_cols].dtypes)
for col in date_cols:
    df_sold[col]=pd.to_datetime(df_sold[col])
print(df_sold[date_cols].dtypes)

#Engineering Metrics
def add_metrics(df):
    df["price_ratio"]=df["ClosePrice"]/df["OriginalListPrice"]
    df["ppsf"]=df["ClosePrice"]/df["LivingArea"]
    df["YrMo"]=df["CloseDate"].dt.to_period("M")
    df["listing_to_contract_days"]= (df["PurchaseContractDate"] - df["ListingContractDate"]).dt.days
    df["contract_to_close_days"]=(df["CloseDate"] - df["PurchaseContractDate"]).dt.days
    return df
df_listing= add_metrics(df_listing)
df_sold= add_metrics(df_sold)

metrics_columns=["ClosePrice","OriginalListPrice","LivingArea","CloseDate","PurchaseContractDate",
                 "ListingContractDate","price_ratio","ppsf", "YrMo","listing_to_contract_days", 
                 "contract_to_close_days"]
df_listing[metrics_columns].head()
df_sold[metrics_columns].head()

#School District Mapping
import geopandas as gpd

gdf_districts = gpd.read_file(data_5/"DistrictAreas2526_-284845464123469011.geojson")
gdf_unified = gdf_districts[gdf_districts["DistrictType"] == "Unified"]
gdf_unified = gdf_unified.to_crs("EPSG:4326")

def add_school_dist(df):
    gdf_properties = gpd.GeoDataFrame(
     df,geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),crs="EPSG:4326")
    joined = gpd.sjoin(gdf_properties, gdf_unified[["geometry", "DistrictName"]], how="left", predicate="within")
    after_drop = pd.DataFrame(joined.drop(columns=["index_right", "geometry"], errors="ignore"))
    return after_drop


df_listing = add_school_dist(df_listing)
df_sold = add_school_dist(df_sold)

df_listing.to_csv(data_5/"Listing_with_district.csv", index= False)
df_sold.to_csv(data_5/"Sold_with_district.csv", index= False)

#Segment and Aggregate 
new_metrics = [
    "price_ratio", 
    "ppsf", 
    "DaysOnMarket", 
    "listing_to_contract_days", 
    "contract_to_close_days"
]

#Sold
#Segment by PropertyType and PropertySubType, CountyORParish and MLSAreaMajor, ListOfficeName and BuyerOfficeName,DistrictName(School)
segment_property_s = df_sold.groupby(["PropertyType", "PropertySubType"])[new_metrics].agg(["mean", "median","std"])
segment_location_s = df_sold.groupby(["CountyOrParish", "MLSAreaMajor"])[new_metrics].agg(["mean", "median","std"])
segment_offices_s = df_sold.groupby(["ListOfficeName", "BuyerOfficeName"])[new_metrics].agg(["mean", "median","std"]) 
segment_district_s = df_sold.groupby("DistrictName")[new_metrics].agg(["mean", "median","std"])

print(f"Sample summary statistic (Sold): Property\n{segment_property_s.head()}\n")
print(f"Sample summary statistic (Sold): Location\n{segment_location_s.head()}\n")
print(f"Sample summary statistic (Sold): Offices\n{segment_offices_s.head()}\n")
print(f"Sample summary statistic (Sold): School District\n{segment_district_s.head()}\n")



#                                                                    Results
# Convert date cols from string to date time format (Listing & Sold)
#CloseDate               object --> datetime64[ns]
#PurchaseContractDate    object --> datetime64[ns]
#ListingContractDate     object --> datetime64[ns]


#                                                        Engineering Metrics: Sold
#    ClosePrice  OriginalListPrice  LivingArea   CloseDate  PurchaseContractDate  ListingContractDate  price_ratio        ppsf    YrMo  listing_to_contract_days  contract_to_close_days
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 0    240000.0           499000.0      1140.0  2024-01-26            2023-11-22           2021-10-06     0.480962  210.526316 2024-01                     777.0                    65.0
# 1    815000.0           759900.0      1974.0  2024-01-05            2021-06-30           2021-03-08     1.072510  412.867275 2024-01                     114.0                   919.0
# 2    810000.0           739900.0      1974.0  2024-01-05            2021-11-18           2021-03-08     1.094743  410.334347 2024-01                     255.0                   778.0
# 3    858000.0                NaN      1995.0  2024-01-30            2024-08-05           2024-01-30          NaN  430.075188 2024-01                     188.0                  -188.0
# 4   1890500.0          1890500.0      3194.0  2024-01-29            2024-01-29           2024-01-29     1.000000  591.891046 2024-01                       0.0                     0.0



#                                                         Summary Statistic by Location (CountyOrParish, MLSAreaMajor): Sold
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                    price_ratio                          ppsf                             DaysOnMarket                      listing_to_contract_days          contract_to_close_days
# CountyOrParish  MLSAreaMajor       mean       median   std          mean        median     std           mean       median   std           mean       median   std           mean       median   std
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Alameda         699 - Not Defined  1.030622   1.013767 0.101710     775.337269  728.052126 239.378726    26.135106  13.0     34.464614     26.688551  13.0     38.955174     28.516549  25.0     32.219138
#                 BERK - Berkeley    1.090453   1.000000 0.186561     576.712240  609.097918 200.175139    27.666667  12.0     32.470499     47.000000  12.0     65.886266     28.333333  31.0     11.239810
# Amador          699 - Not Defined  0.890853   0.889054 0.052264     207.368222  185.063273  71.575840    79.333333  78.0     53.417850     83.833333  78.0     46.948553     14.833333  10.5     28.230598
# Butte           699 - Not Defined 20.173891   0.965852 141.255224   251.246472  259.042691  77.592545    64.037037  37.5     70.281902     71.851852  58.0     71.037170     37.240741  31.0     28.660627
#                 PARA - Paradise    0.960056   0.977621 0.095079     259.038419  269.032258  40.633161    73.301587  50.0     68.266469     81.666667  54.0     73.092738     37.031746  29.0     23.872625
# ...                      ...            ...        ...      ...            ...         ...        ...          ...   ...          ...           ...   ...           ...           ...   ...          ...
# Ventura         WEH - West Hills   1.075001   1.075001      NaN     379.858657  379.858657         NaN     9.000000   9.0          NaN     16.000000  16.0          NaN     68.000000  68.0          NaN
#                 WV - Westlake Vil. 0.977482   0.973401 0.352000     691.977021  638.737893 194.123086    55.034060  33.5     65.157801     58.738063  38.0     66.994124     22.326057  18.0     24.649318
#                 WW - Wagon Wheel   0.966142   0.966142 0.038391     349.157414  349.157414   9.592528    39.500000  39.5     34.648232     44.500000  44.5     34.648232     21.500000  21.5     10.606602
# Yolo            699 - Not Defined  1.047108   0.989891 0.183474     327.062838  331.294811  63.175492    33.937500  11.5     39.509440     38.812500  25.5     40.958872     30.250000  25.5     21.831170
# Yuba            699 - Not Defined  0.917627   0.890323 0.063553     288.486082  283.882784  55.244782   122.222222  78.0    110.550642    129.333333  79.0    115.923466     35.666667  32.0     10.954451

