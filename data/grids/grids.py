# %% load
import os
import json
import geopandas as gpd

# %%

os.getcwd()

# %% load

geojson_data = os.getcwd() + "\\" + "EAMENA_Grid.geojson"
data = gpd.read_file(geojson_data)

# %% statistics

print(f"number of GS: {len(data)}")

# %%
