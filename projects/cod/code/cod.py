
# %%


# %%
# # Creates a BU for Information Resources, grabbing the exact coordinates of the HP (IR and HP will ovelap), adding the HP COD identifier into the field 'Catalogue ID' of the IR, and filling IR with other constant data (Country, Grid ID, etc.)

# def geojson_to_wkt(geojson):
#     # Check if the GeoJSON type is 'Point'
#     if geojson['type'] == 'Point':
#         # Extract the coordinates and convert them to WKT format
#         coordinates = geojson['coordinates']
#         wkt = f"POINT ({coordinates[0]} {coordinates[1]})"
#         return wkt
#     else:
#         raise ValueError("The provided GeoJSON type is not a Point.")

# def create_ir_bu_from_hp():
# # GeoJSON URL of the 91 HP of the COD project
# 	import uuid
# 	import requests
# 	import pandas as pd
# 	import re

# 	geojson_url = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=91&term-filter=%5B%7B%22inverted%22%3Afalse%2C%22type%22%3A%22string%22%2C%22context%22%3A%22%22%2C%22context_label%22%3A%22%22%2C%22id%22%3A%22QRF0%22%2C%22text%22%3A%22QRF0%22%2C%22value%22%3A%22QRF0%22%7D%5D&language=*&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D"
# 	resp = requests.get(geojson_url)
# 	data = resp.json()
# 	# l_geom_place_exp, l_country_type, l_grid_id, l_ir_type = [],[],[],[]
# 	pattern = r"(COD-\d+)"
# 	l_reference_id = []
# 	l_cod_number = []
# 	l_geom_place_exp = []
# 	# for i in data['features'][0]['properties'].keys():
# 	for i in range(len(data['features'])):
# 		# Reference ID (random UUID)
# 		random_uuid = uuid.uuid4()
# 		l_reference_id.append(random_uuid)
# 		# COD number
# 		name = data['features'][i]['properties']['Resource Name']
# 		cod_number = re.search(pattern, name)
# 		l_cod_number.append(cod_number.group(1))
# 		# Geometric Place Expression
# 		geom_place_exp = geojson_to_wkt(data['features'][i]['geometry'])
# 		l_geom_place_exp.append(geom_place_exp)
# 	df = pd.DataFrame(
# 	{'ResourceID': l_reference_id,
# 	'Catalogue ID': l_cod_number,
# 	'Geometric Place Expression': l_geom_place_exp,
# 	'Country Type': ['Egypt'] * len(l_geom_place_exp), 
# 	# 'Grid ID': ['E31N30-12'] * len(l_geom_place_exp), # It should go into the related resources append
# 	'Information Resource Type': ['Photograph'] * len(l_geom_place_exp), #l_ir_type
# 	})
# 	return df

# df = create_ir_bu_from_hp()
# df.to_csv("C:/Rprojects/eamena-arches-dev/projects/cod/business_data/bu_ir_cod.csv", index=False)



# data['features'][0]['geometry']# ['coordinates']
# print(wkt_format)


# %%
# 

def merge2dbs(data_in_N, data_in_S, path_out):
	"""
	Merge the tables of the 2 databases, and remove duplicated rows

	:param data_in_N: A folder path to the folder root of the tables from the first DB
	:param data_in_S: A folder path to the folder root of the tables from the second DB
	:param path_out: A folder path

	"""
	import os
	import pandas as pd

	xlsx_files = os.listdir(data_in_N)
	for xlsx_file in xlsx_files:
		data_in_filename = os.path.splitext(xlsx_file)[0]
		df1 = pd.read_excel(data_in_N + xlsx_file)
		df2 = pd.read_excel(data_in_S + xlsx_file)
		combined_df = pd.concat([df1, df2])
		unique_df = combined_df.drop_duplicates()
		csv_output_path = path_out + data_in_filename + '.csv'
		unique_df.to_csv(csv_output_path, index=False)
		print(f"The file {data_in_filename + '.csv'} has been created in {path_out}")


data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
data_in_N = data_in + "N/"
data_in_S = data_in + "S/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
# merge2dbs(data_in_N, data_in_S, path_out)

# %%
# convert all XLSX tables into CSV

def xlsx2csv(data_in, path_out):
	"""
	Read an XLSX, or a folder of XLSX, and convert it/them into a CSV. The filenames would be the same.

	:param data_in: A folder path or a file path
	:param path_out: A folder path

	"""
	import os
	import pandas as pd

	if os.path.isdir(data_in):
		print(f"Read the directory {data_in}")
		all_files = os.listdir(data_in)
		xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
		for xlsx_file in xlsx_files:
			data_in_filename = os.path.splitext(xlsx_file)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(f"{data_in}/{xlsx_file}")
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")
	elif os.path.isfile(data_in):
		if data_in.endswith('.xlsx'):
			data_in_filename = os.path.basename(data_in)
			data_in_filename = os.path.splitext(data_in_filename)[0]
			# data_in_filename = os.path.splitext(data_in)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(data_in)
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")


# data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/221224PhotosBCKP.xlsx"
data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
# xlsx2csv(data_in, path_out)


#%%
# EXIF metdata
