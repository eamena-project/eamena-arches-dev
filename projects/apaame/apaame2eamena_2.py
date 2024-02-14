
# follow the steps of https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#update-ir-apaame-links to match EAMENA with APAAME

#%%

import os
import pandas as pd
import psycopg2 as pg
import sqlalchemy as sa
from sqlalchemy import create_engine
import json
import numpy as np

## my PG credentials
pg_creds = 'C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.json'

## files
loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"
resources_loc_path = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv"
resources = pd.read_csv(resources_loc_path)

## fieldnames
# reference number in APAAME
apaame_ref_field = "Resource ID(s)" # "ref"
# to join EAMENA and APAAME tables
eamena_on='catalog_id'
apaame_on='Original filename' # "field51"

#%%
# APAAME
# list colnames

# resources = pd.read_csv("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/resource.csv")
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
  AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr%'
) q3
ON q1.ir_id = q3.ir_id
-- LIMIT 1295;
"""

#%%
# EAMENA
# SQL database

df_eamena = pd.read_sql_query(sa.text(sqll), engine)
# df_eamena = pd.read_sql_query(sqll, engine)
# len(df_eamena)
df_eamena.head()


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
resources['Original filename'] = resources['Original filename'].apply(lambda x: os.path.splitext(x)[0] if isinstance(x, str) else x)

# %%
# eamena_fickr_paths.columns

eamena_apaame_match = pd.merge(eamena_flickr_paths, resources, left_on=eamena_on, right_on=apaame_on, how='inner')
# append an empty row at the end of the df for GitHub display purpose
eamena_apaame_match.loc[len(eamena_apaame_match)] = np.nan
fileout = loc_path + "eamena_apaame_match.csv"
eamena_apaame_match.to_csv(fileout, index=False)

#%%
# TODO: update the DB with these results

