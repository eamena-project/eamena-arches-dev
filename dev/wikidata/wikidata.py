
#%%


periodo_eamena = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/time/periodes/periodo/eamena.json"
response = requests.get(periodo_eamena)
json_data = json.loads(response.text)
periodo_ids = json_data["periods"].keys()
# for i in periodo_ids:
# 	match_label = (label == json_data["periods"][i]["label"]) 
# 	match_spatial = (spatialCoverageDescription == json_data["periods"][i]["spatialCoverageDescription"])
# 	if match_label and match_spatial:
# 		print(i)


#%%


def maping_eamena_and_periodo(periodo_eamena = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/time/periodes/periodo/eamena.json", lperiods = ["Iron Age (Iran)", "Classical/Pre-Islamic (Levant/Mesopotamia/Iran/Northern Arabia)", "Islamic (Iran)", "Contemporary Islamic (MENA)", "Unknown"]):
	"""
	Map periods existing in a GeoJSON exported from EAMENA (ex: Sistan) to their PeriodO equivalent to get the PeriodO unique ARK
     
     :param periodo_eamena: the EAMENA authority from PeriodO. A JSON file
     :param lperiods: a list of periods existing in a GeoJSON

	"""
	import re
	import requests
	import json

	# lperiods = ["Iron Age (Iran)", "Classical/Pre-Islamic (Levant/Mesopotamia/Iran/Northern Arabia)", "Islamic (Iran)", "Contemporary Islamic (MENA)", "Unknown"]
	# periodo_eamena = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/time/periodes/periodo/eamena.json"
	response = requests.get(periodo_eamena)
	json_data = json.loads(response.text)
	periodo_ids = json_data["periods"].keys()
	pattern = re.compile(r'(.*?)\s*\((.*?)\)')
	# loop over the dataset
	for period in lperiods:
		matches = pattern.match(period)
		if (matches != None):
			# Extract the matched groups
			label = matches.group(1).strip()
			spatialCoverageDescription = matches.group(2).strip()
			# loop over EAMENA periodo
			for i in periodo_ids:
				match_label = (label == json_data["periods"][i]["label"]) 
				match_spatial = (spatialCoverageDescription == json_data["periods"][i]["spatialCoverageDescription"])
				if match_label and match_spatial:
					print(i + " = " + period)

maping_eamena_and_periodo(lperiods= ["Chalcolithic (Southern Iran)", "Bronze Age (Southern Iran)", "Iron Age (Iran)", "Classical/Pre-Islamic (Levant/Mesopotamia/Iran/Northern Arabia)", "Islamic (Iran)", "Contemporary Islamic (MENA)", "Unknown"])

     



#%%

import requests

# Define the Wikidata item ID
wikidata_id = "Q794"

# Define the SPARQL query to retrieve the geometry
sparql_query = f"""
SELECT ?item ?itemLabel ?coord
WHERE {{
  wd:{wikidata_id} p:P625 ?statement.
  ?statement psv:P625 ?node.
  ?node wikibase:geoLatitude ?lat.
  ?node wikibase:geoLongitude ?lon.
  BIND(CONCAT("Point(", STR(?lon), " ", STR(?lat), ")") AS ?coord).
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
"""

# Define the Wikidata API endpoint
wikidata_api_url = "https://query.wikidata.org/sparql"

# Set headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# Set parameters for the request
params = {
    "query": sparql_query,
    "format": "json",
}

# Make the request to the Wikidata API
response = requests.get(wikidata_api_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the geometry from the response
    geometry = data["results"]["bindings"][0]["coord"]["value"]
    
    print(f"Geometry for {wikidata_id}: {geometry}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

# %%

import requests

# Define the Wikidata item ID for the country (Q794: Egypt in this case)
wikidata_id = "Q794"

# Define the SPARQL query to retrieve the geometry
sparql_query = f"""
SELECT ?item ?itemLabel ?geometry
WHERE {{
  wd:{wikidata_id} wdt:P3896 ?item.
  ?item wdt:P31 wd:Q1496967; wdt:P625 ?geometry.
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
"""

# Define the Wikidata API endpoint
wikidata_api_url = "https://query.wikidata.org/sparql"

# Set headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# Set parameters for the request
params = {
    "query": sparql_query,
    "format": "json",
}

# Make the request to the Wikidata API
response = requests.get(wikidata_api_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the geometry from the response
    geometry = data["results"]["bindings"][0]["geometry"]["value"]

    print(f"Geometry for {wikidata_id}: {geometry}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


# %%
