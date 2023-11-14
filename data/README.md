# Features

[Heritage Places](#heritage-places), [Grids](#grids), Built components, etc.

## Heritage Places

### DMS
> Data Minimum Standards. Completness of data

Data Minimum Standards (MDS) of Heritage Places

#### Files

##### Templates

* [mds-template-readonly.tsv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds-template-readonly.tsv):
	- a read-ony TSV file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This files results from the automatic export of [mds-template.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds-template.xlsx), it will be overwrite each time 'mds-template.xlsx' is updated.
* [mds-template.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds-template.xlsx):
	- an editable XLSX file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This file is considered to be the authorative document for mds.

**Level of aggregation**

It means that fields, and field and field values (`level1`) can be aggregated and sum up into broader categories (`level1` and `level2`). 

#### Scripts

* [mds.ipynb](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds.ipynb):
	- a Jupyter/Python document to run mds assessement
* [convert_xlsx_to_tsv.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/convert_xlsx_to_tsv.py):
	- a Python simple script to convert 'mds-template.xlsx' into 'mds-template-readonly.tsv'. This script is run automatically, in a GitHub action with [update-trigger.yml](https://github.com/eamena-project/eamena-arches-dev/blob/main/.github/workflows/update-trigger.yml), each time 'mds-template.xlsx' is updated.


<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/audit-data-mds.png" width="1000">
  <br>
    <em>A screenshot of the editable 'mds-template.xlsx'</em>
</p>


#### Bulk

[Bulk Upload](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk)
### Grids

[Grids](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/grids#grids)

## Spatial

[Spatial](https://github.com/eamena-project/eamena-arches-dev/tree/main/spatial)


