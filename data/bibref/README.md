# How-to-cite EAMENA database and datasets

## Data entry

### GUI process

### Bulk-Upload process

1. Upload your BU to EAMENA

```mermaid
flowchart LR
	A[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/notes/Arches%207%20Upgrade.md#splitchunk'>BU</a>] --read XLSX--> B{{bulk-uploader}}:::eamenaFunc;
	subgraph EAMENA
	B -- OK --> C[(Postgres DB)];
	B -- OK --> E{{citation-generator}}:::eamenaFunc;
		subgraph citation-generator
		direction TD
		E -- collect BU UUID --> F;
		E -- creates Search URL --> G;
		end
	end
	B -- not OK --> D((STOP)):::stop;
	classDef eamenaFunc fill:#e3c071;
	classDef stop fill:#EE4B2B;
```


## Glossary

- `cff`: https://citation-file-format.github.io/

- `data paper route`: a publication, upstream, of the dataset as a data paper

- `Shared Dataset`: For example, how all the data from Nichole's and Jennie’s PhD theses were credited