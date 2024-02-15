# Creates an HTML output of grids for EAMENA website

#%%
# libraries, variables and load

import os
import requests
import folium as fo

grid_name = "EAMENA_Grid_contour"

# to read from GitHub
indir = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/grids/"
# the raw GeoJSON
infile = indir + grid_name + ".geojson"
# to save locally
outdir = os.path.dirname(os.path.abspath(__file__))
outfile = outdir + "\\" + grid_name + ".html"

geojson_data = requests.get(infile).json()

#%%
# create the map

m = fo.Map(location=[28.5, 34.3], zoom_start=4)
fo.GeoJson(
    geojson_data,  # Replace with the path to your GeoJSON file
    name='geojson'
).add_to(m)

#%%
# save

m.save(outfile)
# %%
