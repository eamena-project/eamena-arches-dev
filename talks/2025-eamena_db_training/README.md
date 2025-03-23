# DB Handover
> Thomas and Salah, 24/03/25 to 25/03/25, School of Archaeology, Oxford

## GitHub

* use the GH search engine
* use mermaid for [flowchart diagrams](https://mermaid.js.org/syntax/flowchart.html)

| GitHub repository | description |
|----------------|-------------|
| [eamena-arches-dev](https://github.com/eamena-project/eamena-arches-dev)    | development repository (**general purpose**) |
| [eamena-functions](https://github.com/eamena-project/eamena-functions)    | data management functions (Python) |
| [eamena-data](https://github.com/eamena-project/eamena-data)   | reference data (ex: concepts), working data, etc. |
| [eamenaR](https://github.com/eamena-project/eamenaR)   |  R package for front-end statistical analysis |
| [eamena](https://github.com/eamena-project/eamena)   |  EAMENA/Arches package to install an Arches/EAMENA-like instance |
| [EAMENA-MachineLearning-ACD](https://github.com/eamena-project/EAMENA-MachineLearning-ACD)  |  ML Automatic Change Detection (Leicester team) |
| [eamena-gee](https://github.com/eamena-project/eamena-gee)  |  development repository for GEE, AI/ML, etc. |
| ...  |  ... |
| [arches](https://github.com/eamena-project/arches)  |  fork of https://github.com/archesproject/arches for PR |

## Data management

### Reference data

Follow this workflow for reference data

```mermaid
flowchart LR
  subgraph GitHub
  subgraph raw_data
    A[XLSX file] --is read by--> B[Python or R<br>script];
  end
  subgraph dynamic_data
    C[CSV or TSV<br>file];
    D[Python or R<br>script];
  end
  raw_data --creates--> C;
  C --is read by--> D
  dynamic_data --creates--> E[HTML file]
  raw_data --creates--> E[HTML file]
  end
  subgraph website
    F[website]
  end
  E -- is read by --> F[HTML iframe]

  click A "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-template.xlsx" _blank
  click B "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/mds/ref_hp_field_description.R" _blank
  click E "https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/fields-description.html" _blank
  click F "https://eamena.org/advanced-use#rm-hp-fields" _blank
  
```

### Back-end programming


```mermaid
flowchart LR
	A[Jupyter Notebook<br>with Inline code] ---> B[Jupyter Notebook<br>with Imported functions]
	C[Python functions] -- is read by --> B
	C ---> D[Arches Plugin]
	C ---> E[Python libraries]
	E ---> F[Arches App]
	subgraph Jupyter_Notebook
		A;
		B;
	end
	subgraph GitHub[<a href='https://github.com/eamena-project/eamena-functions'>eamena-functions</a>]
		C;
		E;
  	end

  click Jupyter_Notebook "https://github.com/eamena-project/eamena-functions" _blank
  click D "https://database.eamena.org/citations/" _blank
  click B "https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/citation/citation_generator.ipynb" _blank
  click C "https://github.com/eamena-project/eamena-functions/blob/main/zenodo/zenodo.py" _blank
  
  
```