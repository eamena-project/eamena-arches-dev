# How-to-cite EAMENA database and datasets

## Data entry

### GUI process

### Bulk-Upload process

1. Upload your BU to EAMENA

```mermaid
flowchart
	LR
	A[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/notes/Arches%207%20Upgrade.md#splitchunk'>BU</a>] --read XLSX--> B{bulk-uploader};
	subgraph local
	B -- OK --> C[(EAMENA)];
	end
	B -- not OK --> D[STOP];
```


## Glossary

- `cff`: https://citation-file-format.github.io/

- `data paper route`: a publication, upstream, of the dataset as a data paper

- `Shared Dataset`: For example, how all the data from Nichole's and Jennie’s PhD theses were credited