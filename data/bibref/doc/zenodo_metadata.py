# Creates secondary data for the Zenodo dump (metadata, lists, maps, etc.)

#%%

import pandas as pd
import requests
import json
from collections import Counter
from datetime import datetime


#%%

# GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=90&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Sistan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22e6e6abc5-3470-45c0-880e-8b29959672d2%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea81-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22lt%22%2C%22val%22%3A%222021-07-01%22%7D%2C%2234cfea4d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%22d2e1ab96-cc05-11ea-a292-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea8a-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%5D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D"
# GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=553&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Sistan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22e6e6abc5-3470-45c0-880e-8b29959672d2%22%7D%7D%2C%7B%22op%22%3A%22or%22%2C%2234cfea69-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea73-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea43-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%224ed99706-2d90-449a-9a70-700fc5326fb1%22%7D%2C%2234cfea5d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea95-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22%22%7D%7D%5D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D&map-filter=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22id%22%3A%22ae42a8fbd96c8f995719a2688f2fad87%22%2C%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22buffer%22%3A%7B%22width%22%3A0%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D%2C%22geometry%22%3A%7B%22coordinates%22%3A%5B%5B%5B61.50347983389591%2C31.348261268106413%5D%2C%5B61.43021147281084%2C31.09323453208181%5D%2C%5B61.44626174025299%2C30.892059795871234%5D%2C%5B61.85928759678521%2C30.736782130955646%5D%2C%5B62.03615110465293%2C31.065294359669124%5D%2C%5B61.76357322781999%2C31.32515741066436%5D%2C%5B61.55549851268111%2C31.371359451751502%5D%2C%5B61.52844879971215%2C31.36425292277393%5D%2C%5B61.50347983389591%2C31.348261268106413%5D%5D%5D%2C%22type%22%3A%22Polygon%22%7D%7D%5D%7D"
GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=307&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Sistan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22e6e6abc5-3470-45c0-880e-8b29959672d2%22%7D%7D%2C%7B%22op%22%3A%22or%22%2C%2234cfea69-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea73-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea43-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%224ed99706-2d90-449a-9a70-700fc5326fb1%22%7D%2C%2234cfea5d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea95-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22%22%7D%7D%5D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D&map-filter=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22id%22%3A%22ae42a8fbd96c8f995719a2688f2fad87%22%2C%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22buffer%22%3A%7B%22width%22%3A0%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D%2C%22geometry%22%3A%7B%22coordinates%22%3A%5B%5B%5B61.6012854423829%2C31.200317996554716%5D%2C%5B61.43021147281084%2C31.09323453208181%5D%2C%5B61.59265954771092%2C31.014768151044933%5D%2C%5B61.759781654852475%2C30.9118316755916%5D%2C%5B62.03615110465293%2C31.065294359669124%5D%2C%5B61.76357322781999%2C31.32515741066436%5D%2C%5B61.73211151793541%2C31.294427967038885%5D%2C%5B61.68254540589061%2C31.26085644276789%5D%2C%5B61.6012854423829%2C31.200317996554716%5D%5D%5D%2C%22type%22%3A%22Polygon%22%7D%7D%5D%7D"
resp = requests.get(GEOJSON_URL)
data = resp.json()

#%%

def field_values(fieldname = None):
    l = list()
    for i in range(len(data['features'])):
        l.append(data['features'][i]['properties'][fieldname])
    return(l)

def summed_values(l = None):
    # split_names = [name.strip() for item in l for name in item.split(',')]
    split_names = [name.strip() for item in l if item is not None for name in item.split(',')]
    name_counts = Counter(split_names)
    df = pd.DataFrame.from_dict(name_counts, orient='index').reset_index()
    df = df.rename(columns={'index': 'name', 0: 'n_hp'})
    df = df.sort_values('n_hp', ascending=False)
    return df

#%%
## TITLE & DESCRIPTION = free text

TITLE = "This is the title of my Zenodo deposit"
DESCRIPTION = "This is the description of my Zenodo deposit"

#%%
## CONTRIBUTORS

contributors_layout = {"name": None,
                       "affiliation": None,
                       "orcid": None}

l = field_values("Assessment Investigator - Actor")
df = summed_values(l)
CONTRIBUTORS = list()
# contributors_list = contributors_layout.copy()
for name in df['name']:
    contributors_layout['name'] = name
    # TODO: "affiliation" and "orcid"
    CONTRIBUTORS.append(contributors_layout.copy())

#%%
## KEYWORDS

KEYWORDS = list()
KEYWORDS.append('EAMENA')

# Countries
l = field_values("Country Type")
df = summed_values(l)
KEYWORDS = KEYWORDS + df['name'].tolist()

# Periods
l = field_values("Cultural Period Type")
df = summed_values(l)
KEYWORDS = KEYWORDS + df['name'].tolist()

# remove keywords like 'Unknown'
KEYWORDS.remove('Unknown')

#%%
## DATES

l = field_values("Assessment Activity Date")
df = summed_values(l)
date_strings = df['name'].tolist()
date_strings.remove('None')
# date_strings = [x for x in date_strings if x is not 'None']
date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in date_strings]
min_date = min(date_objects)
max_date = max(date_objects)
min_date_str = min_date.strftime('%Y-%m-%d')
max_date_str = max_date.strftime('%Y-%m-%d')

DATES = [{'type': 'created', 'start': min_date_str, 'end': max_date_str}]

# %%

metadata = {
     'metadata': {
         'title': TITLE,
         'upload_type': 'dataset',
         'description': DESCRIPTION,
         'creators': [{'name': "EAMENA database",
                       'affiliation': "University of Oxford, University of Southampton"}],
         'contributors': CONTRIBUTORS,
         'license': 'cc-by',
         'keywords': KEYWORDS,
         'dates': DATES,
         'grants': [{'id': '051z6e826::4178'}]
     }
 }

print(json.dumps(metadata, indent=4))

