#%%
import os

os.getcwd()


#%% export a GeoJSON URL to a GeoJSON file
import os
import json
import requests

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


FILENAME = "d_filename"
json_file_name = FILENAME + ".geojson"
GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=1641&language=*&map-filter=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22id%22%3A%22aae2151af2ec4b2df176fb5d0af13213%22%2C%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22buffer%22%3A%7B%22width%22%3A10%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D%2C%22geometry%22%3A%7B%22coordinates%22%3A%5B%5B%5B62.25610623447383%2C30.24925189573038%5D%2C%5B60.503941375853714%2C30.249894660302147%5D%2C%5B60.49313482420084%2C31.749969983638096%5D%2C%5B62.2415366336333%2C31.742499880993094%5D%2C%5B62.25610623447383%2C30.24925189573038%5D%5D%5D%2C%22type%22%3A%22Polygon%22%7D%7D%5D%7D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D"
# read
resp = requests.get(GEOJSON_URL)
data = resp.json()
# Create the JSON file and write the data to it
json_string = json.dumps(data, cls = NpEncoder)
json_string = json.loads(json_string)
with open(json_file_name, 'w') as json_file:
  json.dump(json_string, json_file, indent=4)
  print(json_file_name + " has been exported in " + os.getcwd())
