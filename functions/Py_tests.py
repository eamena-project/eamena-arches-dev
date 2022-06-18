import urllib, geojson, subprocess #, gdal,

url= ' http://ig3is.grid.unep.ch/istsos/wa/istsos/services/ghg/procedures/operations/geojson?epsg=4326'
response = urllib.urlopen(url)
data = geojson.loads(response.read())

with open('data.geojson', 'w') as f:
    geojson.dump(data, f)

args = ['ogr2ogr', '-f', 'ESRI Shapefile', 'destination_data.shp', 'data.geojson']
subprocess.Popen(args)

print("cceec")