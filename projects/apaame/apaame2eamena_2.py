
#%%

import pandas as pd
import psycopg2 as pg
import sqlalchemy as sa
from sqlalchemy import create_engine
import json

# my PG credentials
pg_creds = 'C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.json'

#%%
# APAAME
# list colnames

resources = pd.read_csv("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/projects/apaame/resource.csv")
for column in resources.columns:
    print(column)
    
#%%
# APAAME
# create Direct URL link

# split the path
rs_root = "https://apaame.arch.ox.ac.uk/pages/download.php?ref=" 
rs_options = "&size=scr&noattach=true"
refs = resources["ref"].tolist()
direct_urls = list()
for rs_refnum in refs:
  direct_url = rs_root + str(rs_refnum) + rs_options
  direct_urls.append(direct_url)
# create the df
df_apaame = pd.DataFrame({
    'apaame_id': resources["field51"].tolist(),
    'direct_url': direct_urls
})
df_apaame


#%%
# EAMENA
# read credentials (secret) and connect

with open(pg_creds, 'r') as file:
    db_config = json.load(file)
connection_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
engine = create_engine(connection_str)

#%%
# EAMENA
# SQL statement

# params = ['%flickr%']

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

# print(sqll)

#%%
# EAMENA
# SQL database

df_eamena = pd.read_sql_query(sa.text(sqll), engine)
# df_eamena = pd.read_sql_query(sqll, engine)
# len(df_eamena)
df_eamena.head()


# %%
# EAMENA
# export

loc_path = 'C:/Users/Thomas Huet/Desktop/APAAME/'
df_eamena_filename = 'eamena_fickr_paths.xlsx'
fileout = loc_path + df_eamena_filename
# df_eamena.to_csv(fileout, index=False)
df_eamena.to_excel(fileout, index=False, engine='openpyxl')



# %%
# TODO: join the 2 tables on EAMENA 'catalog_id' and APAAME 'field51'

loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"
resources_loc_path = loc_path + "resource.csv"
eamena_flickr_paths_loc_path = loc_path + "eamena_fickr_paths.csv"
resources = pd.read_csv(resources_loc_path)
eamena_flickr_paths = pd.read_csv(eamena_fickr_paths_loc_path)

# %%
# eamena_fickr_paths.columns

joined_df = pd.merge(eamena_flickr_paths, resources, left_on='catalog_id', right_on='field51', how='inner')


# %%
# convert DNG to JPG
# see: https://technologytales.com/2016/06/08/batch-conversion-of-dng-files-to-other-file-types-with-the-linux-command-line/
# see: C:\Rprojects\Rdev\gmm\marmotta\extract\extract_lithics_4.py

import os
import subprocess

loc_path = "C:/Users/Thomas Huet/Desktop/APAAME/"

img_name = 'APAAME_20141020_RHB-0143'
imgin = img_name + '.dng'
imgout = img_name + '.jpg'
os.chdir(loc_path)
# not working ... 
cmd_to_jpg = "magick convert '%s' '%s'" % (imgin, imgout)
# while this works from PS or CMD
# magick convert "APAAME_20141020_RHB-0143.dng" "APAAME_20141020_RHB-0143.jpg"
# os.system(cmd_to_jpg)
subprocess.call(cmd_to_jpg)
print("      ... DNG converted to JPG")

# %%

cmd = "git --version"
returned_value = os.system(cmd)  # returns the exit code in unix
print('returned value:', returned_value)  


# %%
