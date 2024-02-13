
#%%

import pandas as pd
import psycopg2 as pg
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
df = pd.DataFrame({
    'apaame_id': resources["field51"].tolist(),
    'direct_url': direct_urls
})
df

#%%
# EAMENA
# SQL statement

sqll = """
SELECT q1.ir_id, q1.information_id, q2.catalog_id, img_url, img_name
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS information_id
    FROM tiles
    WHERE tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
    AND resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
) q1
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
    FROM tiles
    WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
    AND resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
) q2
ON q1.ir_id = q2.ir_id
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url,
	tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, name}' AS img_name
    FROM tiles
    WHERE resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
	AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
) q3
ON q1.ir_id = q3.ir_id;
"""


#%%
# EAMENA
# read credentials (secret) and connect

with open(pg_creds, 'r') as file:
    db_config = json.load(file)
try:
    conn = pg.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )
    print("Connected to the database successfully.")
except Exception as e:
    print("Unable to connect to the database.")
    print(e)


#%%
# EAMENA
# SQL database

cur = conn.cursor()
cur.execute(sqll)
rows = cur.fetchall()
for row in rows:
	print(row)
    
#%%
# close

cur.close()
conn.close()

