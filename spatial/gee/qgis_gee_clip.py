# earth engine packages
import ee
from ee_plugin import Map

# define AOI (as map canvas)
e = iface.mapCanvas().extent()
AOI = ee.Geometry.Polygon([[[e.xMinimum(), e.yMaximum()],[e.xMinimum(), e.yMinimum()],[e.xMaximum(), e.yMinimum()],[e.xMaximum(), e.yMaximum()]]]) # must be in WGS84
#### AOI = ee.Geometry.BBox(-122.24, 37.13, -122.11, 37.20)

# bands
R = 'B4' #TCI_R
G = 'B3' #TCI_G
B = 'B2' #TCI_B

#natural colour             |4/3/2      |general - recognisable to the naked eye
#natural-like               |12/8/3     |general - recognisable but clearer than natural colour
#color infrared             |8/4/3      |agricultural areas (bright red)
#false colour (agriculture) |11/8/2     |agricultural areas (bright green)
#false color (urban)        |12/11/4    |urbanisation
#false colour (land/water)  |8/11/4     |coastal and wetland areas
#false colour (geology 1)   |12/11/2    |desertification, mining and industry
#false colour (geology 2)   |11/3/2     |desertification, mining and industry

# date
Y1 = 2020
Y2 = 2021
M1 = 7
M2 = M1 + 3

# Sentinel-2 composite
collection = ee.ImageCollection("COPERNICUS/S2_SR").filterBounds(AOI).filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10).filter(ee.Filter.calendarRange(Y1,Y2,'year')).filter(ee.Filter.calendarRange(M1,M2,'month')).select(['B.*'])

print(collection)

image = ee.Image(collection.median()).clip(AOI).divide(10000)

Map.addLayer(image, {'bands':[R, G, B], 'min': 0, 'max':0.5, 'gamma': 1}, 'Sentinel-2 composite')

# export

task = ee.batch.Export.image.toDrive(
    image=image,
    description='image_export',
    folder='gee_python',
    region=AOI,
    scale=10,
    crs='EPSG:4326'
)

task.start()
