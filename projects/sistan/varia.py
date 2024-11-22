
# %% 
# merge SHP with different geometries and merge them in a GeoJSON file

import os
import geopandas as gpd

print(os.getcwd())

points_gdf = gpd.read_file('C:/Users/Thomas Huet/Desktop/Sistan/data/Heritage Place_Geometry_point.shp')
lines_gdf = gpd.read_file('C:/Users/Thomas Huet/Desktop/Sistan/data/Heritage Place_Geometry_line.shp')
polygons_gdf = gpd.read_file('C:/Users/Thomas Huet/Desktop/Sistan/data/Heritage Place_Geometry_poly.shp')

merged_gdf = gpd.overlay(lines_gdf, polygons_gdf, how='union')
merged_gdf = gpd.overlay(points_gdf, merged_gdf, how='union')

merged_gdf.to_file('C:/Users/Thomas Huet/Desktop/Sistan/data/sistan.geojson', driver='GeoJSON')

# %%
# update the GeoJSON file

import os
import geopandas as gpd
from shapely.geometry import Point

# Your list of IDs
id_list = [
    'E61N31-24', 'E61N31-23', 'E61N31-14', 'E61N31-13',
    'E60N31-24', 'E60N31-23', 'E60N31-22', 'E61N31-11',
    'E61N31-12', 'E61N31-21', 'E61N31-22', 'E62N31-11',
    'E61N30-33', 'E61N30-34', 'E61N30-43', 'E61N30-44',
    'E62N30-33', 'E61N30-42', 'E61N30-41', 'E61N30-32',
    'E61N30-31', 'E60N30-42', 'E60N30-24', 'E61N30-13',
    'E61N30-14'
]

# Read GeoJSON file
geojson_file_path = "C:/Users/Thomas Huet/Desktop/Sistan/data/EAMENA_Grid.geojson"
gdf = gpd.read_file(geojson_file_path)

# Update the 'select' field based on the 'id' field
gdf['select'] = gdf['square'].isin(id_list).astype(int)

# Export the modified GeoJSON file
output_geojson_path = "C:/Users/Thomas Huet/Desktop/Sistan/data/EAMENA_Grid_ok.geojson"
gdf.to_file(output_geojson_path, driver='GeoJSON')
# %%
