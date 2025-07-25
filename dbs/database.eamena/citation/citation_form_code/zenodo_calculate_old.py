
#%% test

def summed_values(data = None, fieldname = None):
	"""
	Creates a dataframe summing the number of occurences for a given field
	
	::param data: dictionary of Heritage Places (JSON)
	"""
	import pandas as pd
	from collections import Counter

	l = list()
	for i in range(len(data['features'])):
		l.append(data['features'][i]['properties'][fieldname])
	split_names = [name.strip() for item in l if item is not None for name in item.split(',')]
	name_counts = Counter(split_names)
	df = pd.DataFrame.from_dict(name_counts, orient='index').reset_index()
	df = df.rename(columns={'index': 'name', 0: 'n_hp'})
	df = df.sort_values('n_hp', ascending=False)
	return df

def zenodo_contributors(data = None, fieldname = "Assessment Investigator - Actor", 
						contributors_layout_HP = {"name": None, "type": "DataCollector"}, contributors_layout_GS = [{'name': "University of Oxford", "type": "DataManager"},{'name': "University of Southampton", "type": "DataManager"}]):
	"""
	Creates dictionary of contributors, filling a dictionary layout (`contributors_layout_*`). Contributors are sorted according to the total number of their name occurences in the selected `fieldname`.
	
	:param data: dictionary of Heritage Places (JSON)
	"""
	if fieldname in list(data['features'][0]['properties'].keys()):
	# HPs
		df = summed_values(data, fieldname)
		CONTRIBUTORS = list()
		for name in df['name']:
			contibut = contributors_layout_HP.copy()
			contibut['name'] = name
			# TODO: "affiliation" and "orcid"
			contibut = {key: value for key, value in contibut.items() if value is not None and value != 'null'}
			CONTRIBUTORS.append(contibut)
	else:
	# not HPs (GS, ...)
		CONTRIBUTORS = contributors_layout_GS
	return CONTRIBUTORS

def zenodo_keywords(data = None, constant = ['EAMENA', 'MaREA', 'Cultural Heritage'], additional = None, fields = ["Country Type", "Cultural Period Type"]):
	"""
	Creates a list of keywords with a constant basis (`constant`) and parsed supplementary `fields` (for space-time keywords)
	
	:param data: dictionary of Heritage Places (JSON)
	:param additional: additional keyworks provided by the user
	"""
	KEYWORDS = list()
	KEYWORDS = KEYWORDS + constant + additional
	if all(elem in list(data['features'][0]['properties'].keys()) for elem in fields):
	# HPs
		for fieldname in fields:
			df = summed_values(data, fieldname)
			KEYWORDS = KEYWORDS + df['name'].tolist()
		try:
			KEYWORDS.remove('Unknown')
		except ValueError:
			pass
	return KEYWORDS

def zenodo_dates(data = None, fields = ["Assessment Activity Date"]):
	"""
	Get the min and the max of dates recorded in `fields`	

	:param data: dictionary of Heritage Places (JSON)
	"""
	from datetime import datetime

	if all(elem in list(data['features'][0]['properties'].keys()) for elem in fields):
	# HPs
		ldates = list()
		for fieldname in fields:
			df = summed_values(data, fieldname)
			ldates = ldates + df['name'].tolist() 
		if 'None' in ldates:
			ldates.remove('None')
		# ldates.remove('None')
		# date_strings = [x for x in date_strings if x is not 'None']
		date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in ldates]
		min_date = min(date_objects)
		max_date = max(date_objects)
		min_date_str = min_date.strftime('%Y-%m-%d')
		max_date_str = max_date.strftime('%Y-%m-%d')
		DATES = [{'type': 'created', 'start': min_date_str, 'end': max_date_str}]
		return DATES
	else:
	# not HPs (GS, ...)
		DATES = [{'type': 'created', 'start': '2021-01-01', 'end': '2021-01-02'}]
		return DATES

def zenodo_related_identifiers(site = 'https://zenodo.org/oai2d', set = 'user-eamena', metadataPrefix = 'oai_dc', reference_data_list = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/lod/zenodo/reference_data_list.tsv"):
	"""
	Parse the 'EAMENA database' community in Zenodo ('user-eamena') to check if there are already uploaded datasets. Handle differently the refrence data (collections, RMs, ...) and the datasets, or business data. The former are 'isDescribedBy' related identifiers, whereas the latter are 'isContinuedBy' related resources.

	:param reference_data_list: the list of reference data already existing in the 'eamena' Zenodo community. These objects will not be added as 'isContinuedBy' in the metadata key 'related_identifiers' but as 'isDescribedBy'
	"""
	import pandas as pd
	from sickle import Sickle

	# reference_data_list = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/lod/zenodo/reference_data_list.tsv"
	reference_data = pd.read_csv (reference_data_list, sep = '\t')
	l_isDescribedBy = reference_data['url'].tolist()

	sickle = Sickle(site)
	records = sickle.ListRecords(metadataPrefix=metadataPrefix, set=set)
	# record = records.next()
	# return record.metadata['identifier'][0]# record = records.next()
	l = list()
	for record in records:
		l.append(record.metadata['identifier'][0])
	# remove the reference data
	l_isContinuedBy = [x for x in l if x not in l_isDescribedBy]
	## create the record
	# business data
	l_isContinuedBy_out = list()
	for busdata in l_isContinuedBy:
		l_isContinuedBy_out.append({'relation': 'isContinuedBy',
									'identifier': busdata})
	# reference data
	l_isDescribedBy_out = list()   
	for refdata in l_isDescribedBy:
		l_isDescribedBy_out.append({'relation': 'isDescribedBy',
									'identifier': refdata})
	# merge lists
	l_related_identifiers = l_isContinuedBy + l_isDescribedBy_out
	return(l_related_identifiers)

def zenodo_statistics(data = None):
	"""
	Calculate basic statistics on HPs. Return a list with: the total number of Heritage Places; the number of Heritage Places layered by number of geometries (some have 1, 2, 3, ...); the total number of geometries; etc.

	:param data: dictionary of Heritage Places (JSON)
	"""
	from collections import Counter

	l = list()
	LIST_HPS = list()
	for i in range(len(data['features'])):
		ea_id = data['features'][i]['properties']['EAMENA ID']
		l.append(ea_id)
	my_dict = {i:l.count(i) for i in l}
	value_counts = Counter(my_dict.values())
	HPS_GEOM_NB = dict(value_counts)
	HPS_NB = sum(HPS_GEOM_NB.values())   
	LIST_HPS.append(HPS_NB)
	LIST_HPS.append(HPS_GEOM_NB)
	HPS_GEOM_NB_TOTAL = {key: key * value for key, value in HPS_GEOM_NB.items()}
	HPS_GEOM_NB_TOTAL = sum(HPS_GEOM_NB_TOTAL.values())
	LIST_HPS.append(HPS_GEOM_NB_TOTAL)
	return(LIST_HPS)

# #%% test
# import requests

# GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&language=*&total=1641&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D&map-filter=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22Grid%20ID%22%3A%22E60N30-24%22%2C%22buffer%22%3A%7B%22width%22%3A%220%22%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B60.5%2C31.25%5D%2C%5B60.5%2C31.5%5D%2C%5B60.75%2C31.5%5D%2C%5B61%2C31.5%5D%2C%5B61.25%2C31.5%5D%2C%5B61.5%2C31.5%5D%2C%5B61.75%2C31.5%5D%2C%5B62%2C31.5%5D%2C%5B62%2C31.25%5D%2C%5B62.25%2C31.25%5D%2C%5B62.25%2C31%5D%2C%5B62.25%2C30.75%5D%2C%5B62%2C30.75%5D%2C%5B62%2C30.5%5D%2C%5B61.75%2C30.5%5D%2C%5B61.5%2C30.5%5D%2C%5B61.5%2C30.25%5D%2C%5B61.25%2C30.25%5D%2C%5B61%2C30.25%5D%2C%5B60.75%2C30.25%5D%2C%5B60.75%2C30.5%5D%2C%5B60.75%2C30.75%5D%2C%5B61%2C30.75%5D%2C%5B61%2C31%5D%2C%5B60.75%2C31%5D%2C%5B60.75%2C31.25%5D%2C%5B60.5%2C31.25%5D%5D%5D%7D%7D%5D%7D"
# resp = requests.get(GEOJSON_URL)
# data = resp.json()

# #%% test




# # %%

# zenodo_statistics(data)

# # zenodo_contributors(data)
# # zenodo_keywords(data)
# # zenodo_dates(data)
# # # %%

# # %%

# %%
