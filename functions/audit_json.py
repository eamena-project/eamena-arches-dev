import json

hp_concepts = "C:\Rprojects\eamena-arches-dev\data\model\Heritage Place_concepts.json"
f = open(hp_concepts)
data = json.load(f)                                                             # convert in dict
hp_conceptscollections = list(data.keys())                                      # list of the concept collections
nb = 0
# sum all concepts
for hp_conceptscollection in hp_conceptscollections:
    nb = nb + len(data[hp_conceptscollection])
print(nb)
