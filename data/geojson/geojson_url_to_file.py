#%% export a GeoJSON URL to a GeoJSON file
import os
import json
import requests

outDir = "C:/Users/Thomas Huet/Desktop/Sistan/data/"

# needed to export as JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


FILENAME = "sistan_grids_OK_OK_OK"
json_file_name = outDir + FILENAME + ".geojson"
GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=25&resource-type-filter=%5B%7B%22graphid%22%3A%2277d18973-7428-11ea-b4d0-02e7594ce0a0%22%2C%22name%22%3A%22Grid%20Square%22%2C%22inverted%22%3Afalse%7D%5D&map-filter=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22id%22%3A1%2C%22buffer%22%3A%7B%22width%22%3A%221%22%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D%2C%22geometry%22%3A%7B%22type%22%3A%22MultiPolygon%22%2C%22coordinates%22%3A%5B%5B%5B%5B61.9185199386503%2C31.434624233128837%5D%2C%5B61.93140337423312%2C31.176955521472394%5D%2C%5B62.17296779141103%2C31.164072085889572%5D%2C%5B62.195513803680974%2C30.829102760736195%5D%2C%5B61.91207822085889%2C30.829102760736195%5D%2C%5B61.92496165644171%2C30.587538343558283%5D%2C%5B61.396740797546%2C30.593980061349694%5D%2C%5B61.40318251533741%2C30.316986196319018%5D%2C%5B60.797661042944775%2C30.320207055214723%5D%2C%5B60.810544478527596%2C30.68094325153374%5D%2C%5B61.07465490797545%2C30.68094325153374%5D%2C%5B61.06821319018404%2C31.083550613496932%5D%2C%5B60.82342791411042%2C31.089992331288343%5D%2C%5B60.80732361963189%2C31.312231595092026%5D%2C%5B60.54643404907974%2C31.318673312883437%5D%2C%5B60.53355061349692%2C31.437845092024542%5D%2C%5B61.9185199386503%2C31.434624233128837%5D%5D%5D%5D%7D%7D%5D%7D"
# read
resp = requests.get(GEOJSON_URL)
data = resp.json()
# Create the JSON file and write the data to it
json_string = json.dumps(data, cls = NpEncoder)
json_string = json.loads(json_string)
with open(json_file_name, 'w') as json_file:
  json.dump(json_string, json_file, indent=4)
  print(FILENAME + " has been exported in '" + outDir + "'")

# %%
