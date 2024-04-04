# %%

def concepts_readonly(url='https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml', output_file_path='C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv', export=True):
    import requests
    from lxml import etree
    import json
    import pandas as pd

    response = requests.get(url)
    root = etree.fromstring(response.content)
    
    # Initialize a list to store id and value pairs for concepts and their parents
    id_value_pairs_corrected = []
    
    # Extract concepts
    for concept in root.xpath('//skos:Concept', namespaces=root.nsmap):
        parent = concept.getparent()
        parent_pref_label = parent.find('skos:prefLabel', namespaces=root.nsmap) if parent is not None else None
        parent_content = json.loads(parent_pref_label.text) if parent_pref_label is not None and '{http://www.w3.org/XML/1998/namespace}lang' in parent_pref_label.attrib and parent_pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us" else {'id': None, 'value': None}
        for pref_label in concept.findall('skos:prefLabel', namespaces=root.nsmap):
            if '{http://www.w3.org/XML/1998/namespace}lang' in pref_label.attrib and pref_label.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == "en-us":
                content = json.loads(pref_label.text)
                # Include parent id and value along with the child's
                id_value_pairs_corrected.append((parent_content['id'], parent_content['value'], content['id'], content['value']))

    # Convert the corrected list of tuples into a pandas DataFrame
    df = pd.DataFrame(id_value_pairs_corrected, columns=['parent_uuid', 'parent_concept', 'uuid', 'concept'])

    if export:
        df.to_csv(output_file_path, sep='\t', index=False)
        print("The TSV has been created.")
    else:
        return df

df = concepts_readonly()

# %%
