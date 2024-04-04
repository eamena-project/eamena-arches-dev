def nodes_uuids(choice = "rm", rm = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/graphs/resource_models/Heritage%20Place.json", concept = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/reference_data/concepts/EAMENA.xml", output_file_path='C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv', export=True):
	# Creates pandas dataframes from RM (JSON files) and Concepts (XML files)
	import requests
	import json
	import pandas as pd
	from lxml import etree
	if choice == "rm":
		print("*Read Resource Models")
		response = requests.get(rm)
		rm_data = json.loads(response.text)
		# Collect nodes' names and UUIDs from resource models
		df_nodes = pd.DataFrame(columns=['level3', 'uuid'])
		df_nodes = df_nodes.rename(columns={'level3': 'db.concept.name', 'uuid': 'db.concept.uuid'})
		for i in range(1, len(rm_data['graph'][0]['nodes'])):
			new_row = [rm_data['graph'][0]['nodes'][i]['name'], rm_data['graph'][0]['nodes'][i]['nodeid']]
		if not export:
			df_nodes.loc[i] = new_row
		return(df_nodes)
	if choice == "concept":
		print("*Read Concepts")
		response = requests.get(concept)
		root = etree.fromstring(response.content)
		id_value_pairs_corrected = []
		for concept in root.xpath('//skos:Concept', namespaces=root.nsmap):
			parent = concept.getparent()
			parent_pref_label = parent.find('skos:prefLabel', namespaces=root.nsmap) if parent is not None else None
			parent_content = json.loads(parent_pref_label.text) if parent_pref_label is not None and '{http://www.w3.org/XML/1998/namespace}lang' in parent_pref_label.attrib and parent_pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us" else {'id': None, 'value': None}
			for pref_label in concept.findall('skos:prefLabel', namespaces=root.nsmap):
				if '{http://www.w3.org/XML/1998/namespace}lang' in pref_label.attrib and pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us":
					content = json.loads(pref_label.text)
					# Include parent id and value along with the child's
					id_value_pairs_corrected.append((parent_content['id'], parent_content['value'], content['id'], content['value']))
		df = pd.DataFrame(id_value_pairs_corrected, columns=['parent_uuid', 'parent_concept', 'uuid', 'concept'])
		if export:
			df.to_csv(output_file_path, sep='\t', index=False)
			print("The TSV of Concepts has been created.")
		else:
			return df


# %%
