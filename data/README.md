# Features

[Heritage Places](#heritage-places), [Grids](#grids), Built components, etc.

## Heritage Places

### ERMS
> Completness of data

Enhanced record minimum standard of Heritage Places

#### Files

##### Templates

* [erms-template-readonly.tsv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/erms-template-readonly.tsv):
	- a read-ony TSV file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the ERMS. This files results from the automatic export of [erms-template.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/erms-template.xlsx), it will be overwrite each time 'erms-template.xlsx' is updated.
* [erms-template.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/erms-template.xlsx):
	- an editable XLSX file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the ERMS. This file is considered to be the authorative document for ERMS.

**Level of aggregation**

It means that fields, and field and field values (`level1`) can be aggregated and sum up into broader categories (`level1` and `level2`). 

#### Scripts

* [erms.ipynb](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/erms.ipynb):
	- a Jupyter/Python document to run ERMS assessement
* [convert_xlsx_to_tsv.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/convert_xlsx_to_tsv.py):
	- a Python simple script to convert 'erms-template.xlsx' into 'erms-template-readonly.tsv'. This script is run automatically, in a GitHub action with [update-trigger.yml](https://github.com/eamena-project/eamena-arches-dev/blob/main/.github/workflows/update-trigger.yml), each time 'erms-template.xlsx' is updated.


<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/audit-data-erms.png" width="1000">
  <br>
    <em>A screenshot of the editable 'erms-template.xlsx'</em>
</p>


#### Bulk

[Bulk Upload](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk)
### Grids

[Grids](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/grids#grids)

## Spatial

[Spatial](https://github.com/eamena-project/eamena-arches-dev/tree/main/spatial)


