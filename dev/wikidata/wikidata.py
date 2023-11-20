def maping_eamena_and_periodo(lperiods):
	"""
	Map periods existing in a GeoJSON exported from EAMENA (ex: Sistan) to their PeriodO equivalent
     
     :param lperiods: a list of periods existing in a GeoJSON

	"""
	pass


lperiods = ["Iron Age (Iran)", "Classical/Pre-Islamic (Levant/Mesopotamia/Iran/Northern Arabia)", "Islamic (Iran)", "Contemporary Islamic (MENA)", "Unknown"]



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
