import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv
import numpy as np
from tqdm import tqdm
import pandas as pd

def read_london_lad_geopandas(lsoa_array):
    # Get Local Authority Boundaries as GeoPandas
    shapefile = 'lsoa/Lower_Super_Output_Area_(LSOA)_IMD2019__(WGS84).shp'
    gdf = gpd.read_file(shapefile)
    # Convert coordinates
    gdf.to_crs(epsg=4326, inplace=True)
    # London
    # print(gdf['lsoa11cd'])
    ladgdf = gdf[gdf['lsoa11cd'].isin(lsoa_array)]
    return ladgdf


# List of LSOAs in our dataset
pd_data = pd.read_csv("pred_environment.csv")

with open("pred_environment.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter = ',')
    data = [data for data in data_iter]
data_array = np.asarray(data, dtype=str)
lsoa_array = data_array.T[2][1:]

# pd_data["pred_environment"] += 1

# Get LAD GeoPandas DataFrame
london_lads_gdf = read_london_lad_geopandas(lsoa_array)

# Read the data table (all data items) and merge with the LAD geo data
gdf = london_lads_gdf.merge(pd_data, left_on='lsoa11cd', right_on='Code')


# # Default GeoPandas plot
# london_lads_gdf.plot()
# plt.show()

# Create plots
ax = gdf.plot(column="pred_environment", cmap="bwr_r", legend=True, vmin=1, vmax=10)
ax.set_axis_off()
ax.set_title("Living environment (predicted)")
plt.savefig("pred_environment_map.png")

ax = gdf.plot(column="mae_environment", cmap="YlOrRd", legend=True, vmin=0, vmax=9)
ax.set_axis_off()
ax.set_title("Living environment (MAE)")
plt.savefig("mae_environment_map.png")