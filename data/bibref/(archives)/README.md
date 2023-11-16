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
* `keywords`: `'EAMENA', MaREA` + locations ("Country Type") + periods ("Cultural Period Type")


#### others or by default

* `access_right`: 'open' (other options in the [documentation](https://help.zenodo.org/docs/about/whats-changed/#deposit-access))


---

## `https://database.eamena.org/citations`
>⚠️ work in progress, please do not take into account

```mermaid
flowchart LR
	U[/user/] -- send --> A[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/notes/Arches%207%20Upgrade.md#splitchunk'>Search URL</a>];
		subgraph EAMENA DB
		A --Search URL--> G{{<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#citation-generator'>citation-generator</a>}}:::eamenaFunc;
			subgraph plugins
			G -- creates reference --> H[email creation];
			end
		subgraph "https://database.eamena.org/citations"
		G -- update the List of citations --> I[List of citations.md]
		G -- creates plain text files --> J[KEY1.ris <br> KEY1.bib <br> ...]
		end
		subgraph "Zenodo"
		G -- creates a new deposit on<br>the EAMENA Zenodo account --> DOI
		end
	end
	H -- send --> Z[/user/];
	classDef eamenaFunc fill:#e3c071;
```

`https://database.eamena.org/citations` will be folder, or a website, hosted on EAMENA AWS, hosting a [List of citations](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#list-of-citations) and several individual reference bibliographic files (.bib, .ris) 

```mermaid
flowchart LR
	subgraph "https://database.eamena.org/citations"
	I[List of citations.md];
	J[KEY1.ris <br> KEY1.bib <br> ...]
	end
```

#### List of citations

Exposed on GitHub. For example

|  **id** 	| **complete citation**	|  **citation downloads** 	|  **search URL** | 
|---	|---	|---	|---	|
| KEY1 	| Contributor, A. (2023), KEY1,  in *University of Oxford, University of Southampton EAMENA Database*. Retrieved from https:/database.eamena.org (Accessed: 2023-06-01)| [.ris](https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bibref/citations/KEY1.ris), [.bib](https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bibref/citations/KEY1.bib)  	| https://tinyurl.com/eamena-0001|  
|  KEY2	|   ...	| ...  	|  ... 	|


Where:

* **id**: unique identifier, which refers to a Search URL (see [List of citations](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#list-of-citations)). For example: `eamena-dataset-1`, `eamena-dataset-2`, ...

* **complete citation**: APA-like citation
	- Contributor, A. (2023), 'KEY',  in *University of Oxford, University of Southampton EAMENA Database*. Retrieved from www.https://database.eamena.org (Accessed: 2023-06-01)

* **citation downloads**: links to downloadable .bib and .ris formats. One by entry. These files are produced on-the-fly.
* **search url**: the shortened URL (here a 'tinyurl' one). The complete URL is listed in [this dataframe](https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bibref/urls/urls.tsv). Shortening URL will be a service hosted locally (see IT solutions [here](https://github.com/awesome-selfhosted/awesome-selfhosted#url-shorteners))

## API

Retrieve the results by changing the Search URL

```
https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&reportlink=false&precision=6&total=1146&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%223f6fc20d-c2a8-4291-b536-046a034e0be9%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea43-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22c08b6e33-a244-415b-8bb1-b1f0949fc581%22%7D%2C%2234cfea5d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea69-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea95-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22%22%7D%2C%2234cfea73-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%5D
```

to:

```
https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=1146&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%223f6fc20d-c2a8-4291-b536-046a034e0be9%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea43-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22c08b6e33-a244-415b-8bb1-b1f0949fc581%22%7D%2C%2234cfea5d-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea69-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%2C%2234cfea95-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22%22%7D%2C%2234cfea73-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%5D
```

## Glossary

- `data paper route`: a publication, upstream, of the dataset as a data paper
- `Search URL`: the URL of a search in EAMENA
- `Shared Dataset`: For example, how all the data from Nichole's and Jennie’s PhD theses were credited