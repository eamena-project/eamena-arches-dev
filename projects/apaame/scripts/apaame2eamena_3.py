
#%%

def update_ea_apaame_links(pg_creds = 'C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.json', loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/", resources_loc_path = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv", apaame_ref_field = "Resource ID(s)", eamena_on = 'catalog_id', apaame_on = 'Original filename', eamena_img_url = "img_url", eamena_direct_url = "direct_url", rs_root = "https://apaame.arch.ox.ac.uk/pages/download.php?ref=", rs_options = "&size=scr&noattach=true", verbose = True):
	"""
	Update the links between the INFORMATION resources and the photographh directly in the Postgres DB EAMENA backend using the metadata exported from ResourceSpace (RS). Follow the steps of https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#update-ir-apaame-links to match EAMENA with APAAME

	:param pg_creds: my PG credentials (local)
	:param resources_loc_path: the CSV file of the RS metadata
	:param apaame_ref_field: "ref", reference number in APAAME
	:param eamena_on: to join EAMENA and APAAME tables
	:param apaame_on: to join EAMENA and APAAME tables,"field51"
	:param eamena_img_url: column name in the SQL/ final df
	:param eamena_direct_url: column name in the SQL/ final df
	:param rs_root: first part of the RS URL
	:param rs_options: last part of the RS URL
	"""

	import os
	import pandas as pd
	import psycopg2 as pg
	import sqlalchemy as sa
	from sqlalchemy import create_engine
	import json
	import numpy as np

	# resources = pd.read_csv("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/resource.csv")
	resources = pd.read_csv(resources_loc_path)
	for column in resources.columns:
		print(column)
		
	# APAAME
	# create Direct URL link

	refs = resources[apaame_ref_field].tolist()
	direct_urls = list()
	for rs_refnum in refs:
		direct_url = rs_root + str(rs_refnum) + rs_options
		direct_urls.append(direct_url)
	# create the df
	df_apaame = pd.DataFrame({
		'apaame_id': resources[apaame_on].tolist(),
		'direct_url': direct_urls
	})
	df_apaame

	# EAMENA
	# read credentials (secret) and connect the Pg DB
	if verbose:
		print("Read Pg")
	with open(pg_creds, 'r') as file:
		db_config = json.load(file)
	connection_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
	engine = create_engine(connection_str)

	# EAMENA
	# SQL statement to collect all IR having a Flickr URL

	sqll = """
	SELECT q1.ir_id, q1.information_id, q2.catalog_id, img_url --, img_name
	FROM (
		SELECT
		resourceinstanceid AS ir_id,
		tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS information_id
		FROM tiles
	WHERE tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
	) q1
	INNER JOIN(
	SELECT
		resourceinstanceid AS ir_id,
		tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
		FROM tiles
	WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
	) q2
	ON q1.ir_id = q2.ir_id
	INNER JOIN(
	SELECT
		resourceinstanceid AS ir_id,
		tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url
		-- tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, name}' AS img_name
		FROM tiles
	WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
	-- AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://eamena-media.s3.eu-west-2%'
	-- AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr%'
	AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://eamena-media.s3.eu-west-2.amazonaws.com/uploadedfiles/50729348183_b255e5f50a_o.jpg'
	) q3
	ON q1.ir_id = q3.ir_id
	-- LIMIT 50;
	"""
	# EAMENA, SQL database
	df_eamena = pd.read_sql_query(sa.text(sqll), engine)
	# df_eamena = pd.read_sql_query(sqll, engine)
	# len(df_eamena)
	if verbose:
		print(df_eamena.head().to_markdown())

	# counts by types of repo
	# TODO
	counts_by_types_of_repo = False
	if counts_by_types_of_repo:
		df_eamena_copy = df_eamena.copy(deep=True)
		df_eamena_copy['img_url'] = df_eamena_copy['img_url'].str.slice(0, 30)
		img_url_counts = df_eamena_copy['img_url'].value_counts()
		img_url_counts_df = img_url_counts.reset_index()
		img_url_counts_df.columns = ['img_url', 'count']  # Rename columns to 'img_url' and 'count'
		print(img_url_counts_df.to_markdown())

	export_xlsx_read_csv = False
	if export_xlsx_read_csv:
		# EAMENA
		# export SQL resut to XLSX or CSV
		df_eamena_filename = 'eamena_fickr_paths.xlsx'
		fileout = loc_path + df_eamena_filename
		# df_eamena.to_csv(fileout, index=False)
		df_eamena.to_excel(fileout, index=False, engine='openpyxl')
		# Join the EAMENA and APAAME on common field (APAAME photograph ID, without its extension)
		eamena_flickr_paths_loc_path = loc_path + "eamena_fickr_paths.csv"
		eamena_flickr_paths = pd.read_csv(eamena_flickr_paths_loc_path)
		# remove the file extension (`...splitext(x)[0]..`)
		# resources['Original filename'] = resources['Original filename'].apply(lambda x: os.path.splitext(x)[0] if isinstance(x, str) else x)
	
	if verbose:
		print("Match EA + APAAME")
	df_apaame['apaame_id'] = df_apaame['apaame_id'].apply(lambda x: os.path.splitext(x)[0] if isinstance(x, str) else x)
	# eamena_fickr_paths.columns
	eamena_apaame_match = pd.merge(df_eamena, df_apaame, left_on=eamena_on, right_on='apaame_id', how='inner')
	# eamena_apaame_match = pd.merge(eamena_flickr_paths, df_apaame, left_on=eamena_on, right_on='apaame_id', how='inner')
	# append an empty row at the end of the df for GitHub display purpose
	eamena_apaame_match.loc[len(eamena_apaame_match)] = np.nan
	# fileout = loc_path + "eamena_apaame_match.csv"
	# eamena_apaame_match.to_csv(fileout, index=False)

	# TODO: update the DB with 'eamena_apaame_match.csv' results
	update_the_DB_with_eamena_apaame_match_csv_results = False
	if update_the_DB_with_eamena_apaame_match_csv_results:
		filein = loc_path + "eamena_apaame_match.csv"
		df_matches = pd.read_csv(filein)
		df_matches = df_matches.dropna(how='any')
		for index, row in df_matches.iterrows():
			img_url = row[eamena_img_url]
			direct_url = row[eamena_direct_url]
			# print(img_url)
			# print(eamena_direct_url)
			# to update IR
			sqll_update = """
			UPDATE tiles
			SET tiledata = jsonb_set(tiledata, '{c712066a-8094-11ea-a6a6-02e7594ce0a0, 0, url}', '"%s"')
			WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE '%s';
			""" % (direct_url, img_url)
			# sqll_update = """
			# UPDATE tiles SET tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' = '%s'
			# WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE '%s'
			# """ % (eamena_direct_url, img_url)
			print(sqll_update)
	out_res = []
	out_res.append(eamena_apaame_match)
	out_res.append(df_eamena)
	out_res.append(df_apaame)
	if verbose:
		print("done")
	return(out_res)

# https://database.eamena.org/report/
# https://database.eamena.org/report/000117a1-b1e2-4e09-b676-124be29a05d4

# "https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg"
# "https://apaame.arch.ox.ac.uk/pages/download.php?ref=8&size=scr&noattach=true"

# SELECT resourceinstanceid AS ir_id, tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url
# FROM tiles
# WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg'


loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"
eamena_apaame_match = update_ea_apaame_links()
# fileout = loc_path + "eamena_apaame_match_1.csv"
# eamena_apaame_match.to_csv(fileout, index=False)
eamena_apaame_match[2].head()

# %%

# def update_csvexport_metadata(

import pandas as pd

infile = "C:/Rprojects/eamena-arches-dev/projects/apaame/data/metadata/240510-collection1/metadata_export_collection9_20240510-09_50.xlsx"
resources = pd.read_excel(infile)

