# Iconic images for EAMENA Concepts

Associate one image to an EAMENA concept to illustrate the latter (ex: Threat type = Agricultural/Pastoral).


<p align="center">
  <img alt="img-name" src="image.png" width="500">
  <img alt="img-name" src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/concepts_images_threat_type_agricole.png" width="500">
  <br>
    <em>The `Agricultural/Pastoral` threat concept in the RDM illustrated with a photograph showing  Agricultural/Pastoral (orchads) threat over cultural heritage.</em>
</p>

The objective is to link the concept image UUID to the RM ex: Threat type = Agricultural/Pastoral, UUID: `767e9467-3bc2-3f71-9427-0ace387bd843`) and display these images as leafs in the Entity-Relationship Diagram of HPs (interactive graph)

## IT

Iconic images (i.e. visual documentation) of particular cases of Threats, Disturbances, etc., affecting Heritage Places are listed in [list.tsv](https://github.com/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/cases/list.tsv) and stored in the [img/](https://github.com/eamena-project/eamena-data/tree/main/reference-data/concepts/heritage_places/cases/img) folder, while the `concepts_images.ipynb` ([GitHub](https://github.com/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/concepts_images.ipynb) | [Colab](https://colab.research.google.com/github/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/concepts_images_graph.ipynb)) script allows to manage images and metadata

<center>

| field | description |
|----------|----------|
| label_parent    | parent node name (ie [field labels](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-template-readonly.tsv))  |
| label    | concept name (ie [value labels](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv), or case) |
| image    | image filename   |
| uuid    | EAMENA UUID of this case (ie value, list: [value uuid](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv)) |
| uuid_parent    | EAMENA UUID of the parent node (ie field, list: [field uuid](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-template-readonly.tsv))  |

<em>The list.tsv table</em>

</center>

see: [eamena-arches-dev/.../reference_data#values](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#values)

## Images metadata

* [website 'hub'](https://eamena.org/advanced-use#rm-hp-fields)
* [GitHub thread #91](https://github.com/eamena-project/eamena-arches-dev/issues/91)
* [fields](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-template-readonly.tsv) and [values](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv) UUIDs
* [Concepts in Google Colab](https://colab.research.google.com/drive/1qzKlquPN6c_6wzmSheujZ0mas9UzfRlg)
* [COD GitHub project](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/cod#photographs)
* [COD Resource Space server](https://cityofthedead.arch.ox.ac.uk/pages/collections_featured.php)


### Values UUIDs


* Ambiguous UUIDs for values

![alt text](image-1.png)

Check the first one

![alt text](image-2.png)

in the DB back office

![alt text](image-3.png)

The concept is:

![alt text](image-4.png)

TODO: return parent UUID and labels

```py
import requests
import json
import pandas as pd
from lxml import etree   
concept = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/reference_data/concepts/EAMENA.xml"
response = requests.get(concept)
root = etree.fromstring(response.content)
id_value_pairs_corrected = []
ct = 0
for concept in root.xpath('//skos:Concept', namespaces=root.nsmap):
  ct = ct + 1
  if ct > 3:
    break
  parent = concept.getparent()
  # print(parent)
  parent_pref_label = parent.find('skos:prefLabel', namespaces=root.nsmap) if parent is not None else None
  parent_content = json.loads(parent_pref_label.text) if parent_pref_label is not None and '{http://www.w3.org/XML/1998/namespace}lang' in parent_pref_label.attrib and parent_pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us" else {'id': None, 'value': None}
  # print(parent_content)
  for pref_label in concept.findall('skos:prefLabel', namespaces=root.nsmap):
    if '{http://www.w3.org/XML/1998/namespace}lang' in pref_label.attrib and pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us":
      content = json.loads(pref_label.text)
      # Include parent id and value along with the child's
      id_value_pairs_corrected.append((parent_content['id'], parent_content['value'], content['id'], content['value']))
df = pd.DataFrame(id_value_pairs_corrected, columns=['parent_uuid', 'parent_concept', 'uuid', 'concept'])
# df = nodes_uuids(choice = "concept")
df.head()
```


See: 
* https://colab.research.google.com/github/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/concepts_images_graph.ipynb
* ~~https://colab.research.google.com/github/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/concepts_images.ipynb~~
