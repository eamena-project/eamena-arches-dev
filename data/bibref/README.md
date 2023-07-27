# How-to-cite EAMENA database and datasets

## Data entry

### Bulk-Upload process

Upload your BU to EAMENA

```mermaid
flowchart LR
	U[/user/] -- send --> A[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/notes/Arches%207%20Upgrade.md#splitchunk'>BU</a>]
	subgraph EAMENA
		A ---> B{{bulk-uploader}}:::eamenaFunc;
		subgraph bulk-uploader
		B -- OK --> H[email creation];
		B -- OK --> C[(Postgres DB)];
		end	
	B -- OK --> E{{citation-generator}}:::eamenaFunc;
		subgraph citation-generator
		E
		end
		E -- collect BU UUID --> H;
		E -- recreates Search URL --> H;
	end
	H -- send --> I[/user/];
	B -- not OK --> D((STOP)):::stop;
	classDef eamenaFunc fill:#e3c071;
	classDef stop fill:#EE4B2B;
```

## Data output

When an user do an export, he/she has to copy the URL and send the URL to `citation-generator`

```mermaid
flowchart LR
	U[/user/] -- send --> A[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/notes/Arches%207%20Upgrade.md#splitchunk'>Search URL</a>];
	subgraph EAMENA
	A --Search URL--> G{{citation-generator}}:::eamenaFunc;
		subgraph citation-generator
		G -- creates reference --> H[email creation];
		end
	end
	H -- send --> I[/user/];
	classDef eamenaFunc fill:#e3c071;
```

## Glossary

- `cff`: https://citation-file-format.github.io/

- `data paper route`: a publication, upstream, of the dataset as a data paper

- `Shared Dataset`: For example, how all the data from Nichole's and Jennie’s PhD theses were credited