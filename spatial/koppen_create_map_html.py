
#%%
import os

os.getcwd()

#%%
import folium

# Create a folium map centered at a specific location
m = folium.Map(location=[35, 20], zoom_start=5)

# Add WMS layer to the map
wms_url = 'http://54.155.109.226:8080/geoserver/ows'  # Replace with your WMS server URL
wms_layer = folium.WmsTileLayer(url=wms_url, layers='Beck_KG_V1_present_0p0083', name='Koppen_Cimate_Classification')
wms_layer.add_to(m)

# Add HTML title to the map
title_html = """
    <span align="center" style="font-size:16px">Koppen Climate Classification</span>
	<a href="https://github.com/eamena-project/eamena-arches-dev/blob/main/data/layouts/koppen_climate_class.md">Legend</a>
    """
m.get_root().html.add_child(folium.Element(title_html))

# Save the map as an HTML file
outFile = os.getcwd() + "\geoserver\koppen_climate_classification.html"
m.save(outFile)

# %%
