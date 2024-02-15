# library(leaflet)
# library(rgdal)
# library(htmlwidgets)

# ## create leaflet map with a QDGC grid for a particular country
# # see: https://github.com/eamena-project/eamena-arches-dev/tree/main/data/grids/qdgc_#readme

# grids.path <- paste0(getwd(),"/data/grids")
# grid.afghanistan <- readOGR(grids.path, layer = "afghanistan", verbose = FALSE)

# map.afghanistan <- leaflet() %>%
#   addTiles() %>%
#   addPolygons(data = grid.afghanistan,
#               weight = 2,
#               fillOpacity = 0,
#               col = 'red')
# saveWidget(map.afghanistan, file=paste0(grids.path, "/grid_afghanistan.html"))

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

# EAMENA_Grid_contour.geojson
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
