# citation-generator
> "How-to-cite" EAMENA database and datasets

Automate the generation of DOI and bibliographic references for the EAMENA sub-datasets 

## Use

An user provide a GeoJSON URL/Search URL ([example](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/sistan#dataset)) to the EAMENA plugin (ie [Arches plugin](https://arches.readthedocs.io/en/stable/developing/extending/extensions/plugins/)) `citation-generator`.

```mermaid
flowchart LR
	subgraph EAMENA DB
		U[/user/] -- Search URL --> E[Export GeoJSON URL]
		E ---> G{{citation-generator}}:::eamenaFunc;
		subgraph plugins
		G
		H{{bulk-uploader}}:::eamenaFunc;
		I{{...}}:::eamenaFunc;
		end
	subgraph "Zenodo"
	G -- creates a new deposit on<br>the EAMENA Zenodo account --> DOI
	end
end
classDef eamenaFunc fill:#e3c071;
```

The core of the Python `citation-generator` function is currently hosted here: https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation-generator.ipynb

## Zenodo

[OAI-PMH compliant](https://developers.zenodo.org/#oai-pmh)

### Proposed metadata

* `title`: *free text*. Name for the dataset (mandatory).
* `description`: *free text*. Dataset description (mandatory).
* `upload_type`: `'dataset'` (always)
* `creators` (always):
 ```
'creators': [{'name': "EAMENA database",
			  'affiliation': "University of Oxford, University of Southampton"}]
```
* `contributors` (example):
 ```
'contributors': [{'name': "Thomas, Huet",
				  "type": "DataCollector"},
				  {'name': "Ash, Smith",
			  	  "type": "DataCollector"}]
```
TODO: add "affiliation", "orcid".
* `license`: `'cc-by'` (always)
* `dates`: creation dates
```
'dates': [{'type': 'created', 'start': '2021-08-01', 'end': '2022-05-01'}],
```
* `grants`: (always, = Arcadia fund, num 4178)
```
'grants': [{'id': '051z6e826::4178'}],
```
* `keywords`: `'EAMENA', MaREA` + locations ("Country Type"[^1]) + periods ("Cultural Period Type[^1]")


#### others or by default

* `access_right`: 'open' (other options in the [documentation](https://help.zenodo.org/docs/about/whats-changed/#deposit-access))



[^1]: All unique values from this EAMENA field, for example in a given GeoJSON export, the field  