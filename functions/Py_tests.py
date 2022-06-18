import os
import urllib.request, geojson, subprocess #, gdal,

def export_geom_from_urlgeojson(out_geom_type = "geojson", out_geom_name = "out_geom", out_geom_dir = os.getcwd() + "\\data\\test\\"):
    # url= 'http://ig3is.grid.unep.ch/istsos/wa/istsos/services/ghg/procedures/operations/geojson?epsg=4326'
    url= 'http://34.244.135.144/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=3&resource-type-filter=%5B%7B%22graphid%22%3A%226c4f0703-c381-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Built%20Component%22%2C%22inverted%22%3Afalse%7D%5D'
    response = urllib.request.urlopen(url)
    data = geojson.loads(response.read())

    out_geom = out_geom_dir + out_geom_name + "." + out_geom_type

    with open(out_geom, 'w') as f:
        geojson.dump(data, f)
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', out_geom]
    subprocess.Popen(args)
    print("File "+ out_geom_name + "." + out_geom_type + " created!")

export_geom_from_urlgeojson()