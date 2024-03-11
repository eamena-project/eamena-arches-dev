import ee  # Import the Earth Engine library

# Initialize the Earth Engine object, using the authentication credentials.
ee.Initialize()

# Define the Area of Interest (AOI) with the provided coordinates.
AOI = ee.Geometry.Polygon(
    [[[59.974807, 29.88018],
      [59.975204, 29.880725],
      [59.9761, 29.880255],
      [59.975601, 29.87959],
      [59.974786, 29.880087],
      [59.974807, 29.88018]]]
)

# Define the bands and date range for filtering the satellite images.
R, G, B = 'B4', 'B3', 'B2'  # Red, Green, Blue bands for Sentinel-2
Y1, Y2 = 2020, 2021  # Year range
M1, M2 = 7, 10  # Month range (July to October)

# Filter the Sentinel-2 image collection based on the AOI and the date range.
collection = ee.ImageCollection("COPERNICUS/S2_SR")\
    .filterBounds(AOI)\
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))\
    .filter(ee.Filter.calendarRange(Y1, Y2, 'year'))\
    .filter(ee.Filter.calendarRange(M1, M2, 'month'))\
    .select(['B.*'])

# Compute the median of the image collection and clip it to the AOI.
image = collection.median().clip(AOI).divide(10000)

# Display the image (You will use folium or the Map display in Colab for visualization).
# For example, using folium:
import folium

# Function to add EE drawing method to folium.
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map data © Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Create a folium map object.
my_map = folium.Map(location=[59.9755, 29.8805], zoom_start=15)

# Add the image layer to the map object.
my_map.add_ee_layer(image, {'bands': [R, G, B], 'min': 0, 'max': 0.3}, 'Color Composite')

# Display the map.
my_map.add_child(folium.LayerControl())
display(my_map)

# Note: The visualization parameters (min, max) might need adjustment based on your specific needs.
