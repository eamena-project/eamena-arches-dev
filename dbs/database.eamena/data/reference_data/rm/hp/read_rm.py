#%% 
# import

import json

hp_concepts = "Heritage Place.json"
f = open(hp_concepts)
data = json.load(f)                                                             # convert in dict
hp_conceptscollections = list(data.keys())                                      # list of the concept collections
nb = 0
# sum all concepts
for hp_conceptscollection in hp_conceptscollections:
    nb = nb + len(data[hp_conceptscollection])
print(nb)

# %%
# remove the Arabic hard written in the HP RM and export in a temp file

import json
import re

# Load data from the input JSON file
with open('Heritage Place.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Loop through all graphs and their cards to modify the 'name' field
for graph in data['graph']:
    for card in graph['cards']:
        if 'name' in card and card['name']:
            # Use a regular expression to remove text after the '/'
            card['name'] = re.sub(r'/.*', '', card['name']).strip()

# Write the updated data to a new JSON file
with open('temp/Heritage Place_without_hard_written_arabic.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# %%
