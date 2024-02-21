# Collect nodes' names and UUIDs from resource models

import requests
import json
import pandas as pd

def nodes_uuids(rm = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/graphs/resource_models/Heritage%20Place.json"):
	# url = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/graphs/resource_models/Information%20Resource.json"
	response = requests.get(rm)
	graph_data = json.loads(response.text)
	# root_node_id = graph_data['graph'][0]['root']['nodeid']
	df_nodes = pd.DataFrame(columns=['level3', 'uuid'])
	df_nodes = df_nodes.rename(columns={'level3': 'db.concept.name', 'uuid': 'db.concept.uuid'})
	for i in range(1, len(graph_data['graph'][0]['nodes'])):
		new_row = [graph_data['graph'][0]['nodes'][i]['name'], graph_data['graph'][0]['nodes'][i]['nodeid']]
		df_nodes.loc[i] = new_row
	return(df_nodes)
	# outDir = os.path.dirname(os.path.realpath(__file__)) + '\\'
	# outDir = '/content/'
	# file_path = outDir + "ir-uuids-readonly.tsv"
	# print(file_path)
	# df_nodes.to_csv(file_path, sep='\t', index=False)
df_nodes = nodes_uuids()
print(df_nodes.to_markdown())
file_path = "C:/Rprojects/eamenaR/inst/extdata/ids_temp.csv"
df_nodes.to_csv(file_path, sep=',', index=False)