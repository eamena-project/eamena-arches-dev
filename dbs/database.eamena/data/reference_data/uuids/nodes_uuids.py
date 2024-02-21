def nodes_uuids(rm = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/graphs/resource_models/Heritage%20Place.json"):
	######################################################
	## Collect nodes' names and UUIDs from resource models
	######################################################
	import requests
	import json
	import pandas as pd
	response = requests.get(rm)
	graph_data = json.loads(response.text)
	df_nodes = pd.DataFrame(columns=['level3', 'uuid'])
	df_nodes = df_nodes.rename(columns={'level3': 'db.concept.name', 'uuid': 'db.concept.uuid'})
	for i in range(1, len(graph_data['graph'][0]['nodes'])):
		new_row = [graph_data['graph'][0]['nodes'][i]['name'], graph_data['graph'][0]['nodes'][i]['nodeid']]
		df_nodes.loc[i] = new_row
	return(df_nodes)