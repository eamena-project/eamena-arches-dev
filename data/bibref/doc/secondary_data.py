# Creates secondary data for the Zenodo dump (metadata, lists, maps, etc.)

#%%

import pandas as pd
import os
import requests
import json

GEOJSON_URL = r"https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=90&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Sistan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22e6e6abc5-3470-45c0-880e-8b29959672d2%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea81-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22lt%22%2C%22val%22%3A%222021-07-01%22%7D%2C%2234cfea4d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%22d2e1ab96-cc05-11ea-a292-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea8a-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%5D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D"

#%%

resp = requests.get(GEOJSON_URL)
data = resp.json()

#%%

df = pd.DataFrame(columns=['eaid', 'uuid'])
for i in range(len(data)):
    data_row = {'eaid': data[0]['eamenaid']['en']['value'], 'uuid': data[i]['uuid']} 
    df.loc[i] = data_row
print(df.to_markdown(index=False))

# %%
