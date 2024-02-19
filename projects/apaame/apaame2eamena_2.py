
# follow the steps of https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#update-ir-apaame-links to match EAMENA with APAAME

#%%

import os
import pandas as pd
import psycopg2 as pg
import sqlalchemy as sa
from sqlalchemy import create_engine
import json
import numpy as np

## my PG credentials (local)
pg_creds = 'C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.json'

## files
loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"
resources_loc_path = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv"

## fieldnames
# reference number in APAAME
apaame_ref_field = "Resource ID(s)" # "ref"
# to join EAMENA and APAAME tables
eamena_on = 'catalog_id'
apaame_on = 'Original filename' # "field51"

# column name in the SQL/ final df
eamena_img_url = "img_url" 
eamena_direct_url = "direct_url"

#%%
# APAAME
# list colnames

# resources = pd.read_csv("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/resource.csv")
resources = pd.read_csv(resources_loc_path)
for column in resources.columns:
    print(column)
    
#%%
# APAAME
# create Direct URL link

# split the path
rs_root = "https://apaame.arch.ox.ac.uk/pages/download.php?ref=" 
rs_options = "&size=scr&noattach=true"
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


#%%
# EAMENA
# read credentials (secret) and connect the Pg DB

with open(pg_creds, 'r') as file:
    db_config = json.load(file)
connection_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
engine = create_engine(connection_str)

#%%
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
  AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://eamena-media.s3.eu-wes%'
  -- AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr%'
) q3
ON q1.ir_id = q3.ir_id
LIMIT 50;
"""

#%%
# EAMENA
# SQL database

df_eamena = pd.read_sql_query(sa.text(sqll), engine)
# df_eamena = pd.read_sql_query(sqll, engine)
# len(df_eamena)
df_eamena.head()

#%%
# counts by types of repo

df_eamena_copy = df_eamena.copy(deep=True)
df_eamena_copy['img_url'] = df_eamena_copy['img_url'].str.slice(0, 30)
img_url_counts = df_eamena_copy['img_url'].value_counts()
img_url_counts_df = img_url_counts.reset_index()
img_url_counts_df.columns = ['img_url', 'count']  # Rename columns to 'img_url' and 'count'
print(img_url_counts_df.to_markdown())

# %%
# EAMENA
# export SQL resut to XLSX or CSV

df_eamena_filename = 'eamena_fickr_paths.xlsx'
fileout = loc_path + df_eamena_filename
# df_eamena.to_csv(fileout, index=False)
df_eamena.to_excel(fileout, index=False, engine='openpyxl')

# %%
# Join the EAMENA and APAAME on common field (APAAME photograph ID, without its extension)

eamena_flickr_paths_loc_path = loc_path + "eamena_fickr_paths.csv"
eamena_flickr_paths = pd.read_csv(eamena_flickr_paths_loc_path)
# remove the file extension (`...splitext(x)[0]..`)
# resources['Original filename'] = resources['Original filename'].apply(lambda x: os.path.splitext(x)[0] if isinstance(x, str) else x)
df_apaame['apaame_id'] = df_apaame['apaame_id'].apply(lambda x: os.path.splitext(x)[0] if isinstance(x, str) else x)

# %%
# eamena_fickr_paths.columns

eamena_apaame_match = pd.merge(eamena_flickr_paths, df_apaame, left_on=eamena_on, right_on='apaame_id', how='inner')
# append an empty row at the end of the df for GitHub display purpose
eamena_apaame_match.loc[len(eamena_apaame_match)] = np.nan
fileout = loc_path + "eamena_apaame_match.csv"
eamena_apaame_match.to_csv(fileout, index=False)

#%%
# TODO: update the DB with 'eamena_apaame_match.csv' results

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

# %%

# https://database.eamena.org/report/
# https://database.eamena.org/report/000117a1-b1e2-4e09-b676-124be29a05d4

# "https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg"
# "https://apaame.arch.ox.ac.uk/pages/download.php?ref=8&size=scr&noattach=true"

# SELECT resourceinstanceid AS ir_id, tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url
# FROM tiles
# WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg'

