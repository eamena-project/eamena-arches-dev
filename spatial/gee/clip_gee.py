#%%

import ee

#%%

ee.Authenticate()

# ee.Initialize(project='clipgee')

#%%

service_account = 'clipgee@clipgee.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'C:/Rprojects/eamena-arches-dev/spatial/credentials/clipgee-d255ac0a9453.json')
ee.Initialize(project='clipgee', credentials)

# ee.Initialize()

#%%

coordinates = [
    [30.71875, 42.75],
    [30.71875, 42.8125],
    [30.75, 42.8125],
    [30.75, 42.75],
    [30.71875, 42.75]
]

aoi = ee.Geometry.Polygon(coordinates)

# Example: Load Landsat 8 Image
landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
            .filterDate('2020-01-01', '2020-12-31') \
            .filterBounds(aoi) \
            .sort('CLOUD_COVER') \
            .first()

clipped_image = landsat.clip(aoi)

#%%

import folium

# Get the URL of the image
url = clipped_image.getMapId({'bands': ['B4', 'B3', 'B2'], 'max': 0.3})

# Create a folium map object.
center = [42.78125, 30.734375] # Center of your AOI
my_map = folium.Map(location=center, zoom_start=10)

# Add the image layer to the map.
my_map.add_ee_layer(url['tile_fetcher'].url_format, name='Clipped Landsat Image')

# Display the map.
display(my_map)

# task = ee.batch.Export.image.toDrive(image=clipped_image,
#                                      description='clipped_image',
#                                      folder='Your_Folder_Name',
#                                      fileNamePrefix='clipped_landsat',
#                                      scale=30)
# task.start()

