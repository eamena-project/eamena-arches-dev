# EAMANA DB's Data

[Reference Data](#reference-data), [Business data](#business-data)

---

# Reference Data

**Reference data** includes Resource Models, Concepts, Grids, etc. This is all data provided a priori (≠ Business data)

## Resource Models
> RM

* [Heritage Places](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#heritage-places)
* [Information Resources](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#information-resources)

### Heritage Places
> HP, HP Resource Model, HP RM

* HP reference data is located here: https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp

* The latest BU template serves as the reference for:
  - [field values descriptions](#fields)

* The template `mds-template-*` is the reference table for:
  - groups of fields and fields descriptions
  - [MDS](#mds)
  - eamenaR mapping file `ids.csv` (see [eamenaR documentation](https://github.com/eamena-project/eamenaR#correspondances-between-concept-labels-and-uuids))

* [mds-template.xlsx](rm/hp/mds/mds-template.xlsx):
  - an editable XLSX file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This file is considered the authoritative document for MDS.

* [mds-template-readonly.tsv](rm/hp/mds/mds-template-readonly.tsv):
  - a read-only TSV file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This files results from the automatic export of [mds-template.xlsx](rm/hp/mds/mds-template.xlsx), it will be overwrite each time 'mds-template.xlsx' is updated)

**Level of aggregation**

This indicates that fields, including field values (`level3`, the most detailed level), can be aggregated into broader categories (`level2` and `level1`, the most general levels). 

#### Fields

##### Field descriptions

Thinner categories (`level3`) colored by groups: [[fields-description.html](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/fields-description.html)]

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-field-descriptions.png" width="600">
  <br>
    <em>Screenshot of the HTML dynamic/interactive table 'fields-description.html', with a search on 'Agricul' with field colored by groups and field descriptions</em>
</p>

##### Groups of fields descriptions

Fields (`level3`) are grouped in broader categories, or groups (`level1`). These groups are colored according to the MDS reference file, and HTML links are added to value descriptions ([Individual reference sheets](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#individual-reference-sheets)): [[field-to-tsv.html](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/field-to-tsv.html)]

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-field-group-values-descriptions.png" width="250">
  <br>
    <em>Screenshot of the HTML dynamic/interactive table 'field-to-tsv.html', with colored groups and hyperlinks to the indiviudal reference sheets</em>
</p>

##### MDS
> Minimum Data Standards. Completness of data

Minimum Data Standards (MDS) of Heritage Places. MDS fields in this HTML circular plot [[mds-reference.html](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-reference.html)]

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-mds-pie.png" width="600">
  <br>
    <em>A screenshot of the `mds_level.html` file showing the 98 fields of the Heritage Places with the MDS fields (highlighted, thumbs up) using the `mds-reference.ipynb` script</em>
</p>

##### ERD
> Entity-relationships diagram

ERD of HP with fieldnames and CIDOC-CRM entities and relationships [[EAMENA-erd.html](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/erd/EAMENA-erd.html)]

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-erd.png" width="650">
  <br>
    <em>A screenshot of the Python `pyvis` ERD HTML file (detail) showing the 98 fields of the Heritage Places with the MDS fields (colored) using the coding from `EAMENA-erd.ipynb` or `EAMENA_spa.ipynb` scripts</em>
</p>

---

* [mds-reference.ipynb](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/mds-reference.ipynb)
  - a Jupyter/Python document to run mds reference
* [mds-assessment.ipynb](https://github.com/eamena-project/eamena-functions/blob/main/mds/mds.ipynb):
  - a Jupyter/Python document to run mds assessment on heritage places
* [convert_xlsx_to_tsv.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/convert_xlsx_to_tsv.py):
  - a Python simple script to convert 'mds-template.xlsx' into 'mds-template-readonly.tsv'. This script is run automatically, in a GitHub Action with [mds-to-tsv.yml](https://github.com/eamena-project/eamena-arches-dev/blob/main/.github/workflows/mds-to-tsv.yml), each time 'mds-template.xlsx' is updated.


<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/audit-data-mds-excel.png" width="1000">
  <br>
    <em>A screenshot of the editable 'mds-template.xlsx'</em>
</p>

##### Values
> Field values

Photographs give a visual documentation of field values [[concepts_images_graph.ipynb]](https://colab.research.google.com/github/eamena-project/eamena-data/blob/main/reference-data/concepts/heritage_places/concepts_images_graph.ipynb)

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-erd-img.png" width="650">
  <br>
    <em>A screenshot of the Python `pyvis` ERD HTML file (detail) using the coding from `concepts_images_graph.ipynb` script (in progress)</em>
</p>

Field value descriptions pertain to `level3` fields. They are listed in this file: [[README.md](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp/values#readme)]. The latter is generated through the [split_bu_template.py]() script

```sh
py C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/bulk_data/functions/split_bu_template.py "../templates/Bulk_Upload_template_240228.xlsx" "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/values"
```

This script reads a BU template (ex: `Bulk_Upload_template_240228.xlsx`). 

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-values.png" width="600">
  <br>
    <em>Screenshot of the BU template worksheet 'Condition Assessment'. The script which uses '#' and empty row markers to delineate field descriptions</em>
</p>



### Information Resources
> IR, IR Resource Model, IR RM

field names' UUIDs are listed here: [ir-uuids-readonly.tsv](ir-uuids-readonly.tsv). The Python script that generate this file is [nodes_id.ipynb](nodes_id.ipynb)

## Grids

<p align="center">
  <img alt="img-name" src="image.png" width="650">
</p>

[EAMENA_Grid_contour.geojson](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/grids/EAMENA_Grid_contour.geojson) (screenshot, countour only) and [EAMENA_Grid.geojson]((https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/grids/EAMENA_Grid.geojson)) (with grid cells)

## UUIDs

Run the Python function [nodes_uuids()](uuids/nodes_uuids.py) on a RM (JSON) or a file of concepts (XML) to collect the UUIDs of the nodes

* For RM (example)

```Python
df_nodes = nodes_uuids(choice = "rm", rm = "https://raw.githubusercontent.com/eamena-project/eamena/master/eamena/pkg/graphs/resource_models/Heritage%20Place.json")
file_path = "C:/Rprojects/eamenaR/inst/extdata/ids_temp.csv"
df_nodes.to_csv(file_path, sep=',', index=False)
```
Gives this [ids_temp.csv](https://github.com/eamena-project/eamenaR/blob/main/inst/extdata/ids_temp.csv) file. Such a mapping table can be used in the [eamenaR package](https://github.com/eamena-project/eamenaR?tab=readme-ov-file#uuids-of-the-nodes)

* For concepts (example)
 
```Python
nodes_uuids(choice = "concept")
```
Gives the [concepts_readonly.tsv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/concepts_readonly.tsv) listing

> **Note:** Fieldnames (ex: "Effect type") have UUIDs. To check these correspondances, check the `nodeid` in the RM. For example, the "Effect type" field has the UUID `34cfea90-c2c0-11ea-9026-02e7594ce0a0` (see its [fieldname](https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Heritage%20Place.json#L2036) and [uuid](https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Heritage%20Place.json#L6530)).


### Other

Check the completeness of data. Python function to model the quality of HP with a radar diagram based on the groups appearing in the BU file (different levels of data aggregation and summing):

see: [template.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/template.xlsx)

1. Query an HP in Pg, for example [Apamea](http://52.50.27.140/report/dbc95d2d-38fb-465e-a6cb-0545eaa7584f) (`EAMENA-0500002` / `dbc95d2d-38fb-465e-a6cb-0545eaa7584f`) in the training instance <http://52.50.27.140/>:

```SQL
SELECT * FROM tiles 
WHERE resourceinstanceid::text LIKE 'dbc95d2d-38fb-465e-a6cb-0545eaa7584f'
```

The copied output is this one:

```
"db0f797d-eb8f-4080-be15-0a1defa6d200"	"{""34cfea63-c2c0-11ea-9026-02e7594ce0a0"": ""a0858dcd-6d72-4a83-bb70-32666471b433"", ""34cfea75-c2c0-11ea-9026-02e7594ce0a0"": {""ar"": {""value"": """", ""direction"": ""rtl""}, ""de"": {""value"": """", ""direction"": ""ltr""}, ""el"": {""value"": """", ""direction"": ""ltr""}, ""en"": {""value"": ""Thomas"", ""direction"": ""ltr""}, ""fr"": {""value"": """", ""direction"": ""ltr""}, ""pt"": {""value"": """", ""direction"": ""ltr""}, ""ru"": {""value"": """", ""direction"": ""ltr""}, ""zh"": {""value"": """", ""direction"": ""ltr""}, ""en-US"": {""value"": """", ""direction"": ""ltr""}, ""en-us"": {""value"": """", ""direction"": ""ltr""}}, ""34cfea76-c2c0-11ea-9026-02e7594ce0a0"": ""600257ae-01e7-4b40-a43f-dbef041af925"", ""34cfea7b-c2c0-11ea-9026-02e7594ce0a0"": ""994b1992-d107-42ab-9562-8931f61b0325""}"	"34cfe9fb-c2c0-11ea-9026-02e7594ce0a0"	"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"1516e4cc-b9a2-4f97-938a-b77e6955ec0b"	"{""34cfea5c-c2c0-11ea-9026-02e7594ce0a0"": ""ff32ca53-239a-4235-ac42-da1eb52fe00d"", ""34cfea90-c2c0-11ea-9026-02e7594ce0a0"": ""9cd1d57e-9b47-4535-a08e-d2619dace462""}"	"34cfe9ce-c2c0-11ea-9026-02e7594ce0a0"	"db237175-616d-4f0c-9d44-30a6b1c1c7e2"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"6a4485b9-4569-4f6b-bfc0-c6c6932c08a4"	"{""34cfea8e-c2c0-11ea-9026-02e7594ce0a0"": ""2eef0519-3503-4e5e-80a1-9b4555d03db3""}"	"34cfe9bf-c2c0-11ea-9026-02e7594ce0a0"	"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	1	
"f7b896c8-b8a0-4d32-ae21-2b6a298bb93f"	"{""34cfe9f5-c2c0-11ea-9026-02e7594ce0a0"": ""19cf501c-df75-440d-8e66-f62c26f9e6c7""}"	"34cfe9f5-c2c0-11ea-9026-02e7594ce0a0"	"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"b70172a4-49a9-46c5-ba94-3acc33352c5a"	"{""5348cf67-c2c5-11ea-9026-02e7594ce0a0"": {""type"": ""FeatureCollection"", ""features"": [{""id"": ""6b323728000a2d4816b112504af95cbb"", ""type"": ""Feature"", ""geometry"": {""type"": ""Polygon"", ""coordinates"": [[[36.40283415928309, 35.42958150293339], [36.39929749262117, 35.429703268074434], [36.39840087290628, 35.42842472491634], [36.397031037227066, 35.42860737518316], [36.392896624087285, 35.42698380274682], [36.39496383065665, 35.418398619473976], [36.39810199966627, 35.41693722056071], [36.393942680423805, 35.41496834955966], [36.39299624850372, 35.410421494546426], [36.410330896366276, 35.41263405871341], [36.41122751608253, 35.41389255434797], [36.410231271952426, 35.422112889059065], [36.4076410372208, 35.42278265715038], [36.40627120154207, 35.42436572324138], [36.40617157712927, 35.42586757769604], [36.40283415928309, 35.42958150293339]]]}, ""properties"": {""nodeId"": ""5348cf67-c2c5-11ea-9026-02e7594ce0a0""}}]}, ""5348cf6b-c2c5-11ea-9026-02e7594ce0a0"": ""52c60073-3f87-45ce-8eaa-d67a9e5412d3"", ""5348cf6c-c2c5-11ea-9026-02e7594ce0a0"": ""433b0da1-8fee-44f8-9e8f-63703880ad07"", ""5348cf6d-c2c5-11ea-9026-02e7594ce0a0"": {""ar"": {""value"": """", ""direction"": ""rtl""}, ""de"": {""value"": """", ""direction"": ""ltr""}, ""el"": {""value"": """", ""direction"": ""ltr""}, ""en"": {""value"": """", ""direction"": ""ltr""}, ""fr"": {""value"": """", ""direction"": ""ltr""}, ""pt"": {""value"": """", ""direction"": ""ltr""}, ""ru"": {""value"": """", ""direction"": ""ltr""}, ""zh"": {""value"": """", ""direction"": ""ltr""}, ""en-US"": {""value"": """", ""direction"": ""ltr""}, ""en-us"": {""value"": """", ""direction"": ""ltr""}}, ""ce842cdc-c2c7-11ea-9026-02e7594ce0a0"": [""11df2516-3710-417d-b1e2-3ce94ceeda3e""]}"	"3080eebe-c2c5-11ea-9026-02e7594ce0a0"		"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"e188f7bf-7411-4361-82f2-8e2b3deefc69"	"{""34cfe992-c2c0-11ea-9026-02e7594ce0a0"": {""en"": {""value"": ""EAMENA-0500002"", ""direction"": ""ltr""}, ""fr"": {""value"": ""EAMENA-0500002"", ""direction"": ""ltr""}}}"	"34cfe992-c2c0-11ea-9026-02e7594ce0a0"		"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"da500a22-d15c-4083-83cc-3178c2d43eeb"	"{""34cfea4d-c2c0-11ea-9026-02e7594ce0a0"": ""00b71e76-4958-42a6-82f8-bc8ea5639064"", ""34cfea81-c2c0-11ea-9026-02e7594ce0a0"": ""2023-09-26"", ""34cfea8a-c2c0-11ea-9026-02e7594ce0a0"": [{""resourceId"": ""d62fdaf6-a9a4-4032-9f63-2e4f21adaab7"", ""ontologyProperty"": ""http://www.ics.forth.gr/isl/CRMdig/L33_has_maker"", ""resourceXresourceId"": ""d28e3b17-b3a2-4dd9-baef-05d23531b333"", ""inverseOntologyProperty"": ""http://www.ics.forth.gr/isl/CRMdig/L33i_is_maker_of""}], ""bcd3a8ae-0404-11eb-a11c-0a5a9a4f6ef7"": false, ""d2e1ab96-cc05-11ea-a292-02e7594ce0a0"": [""20b1a4e0-97e1-41f7-b519-124a7317266b""]}"	"34cfea2e-c2c0-11ea-9026-02e7594ce0a0"		"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"{}"	"34cfe9b9-c2c0-11ea-9026-02e7594ce0a0"		"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"cfeab3e6-2b98-4866-b47a-905964d8c9f2"	"{}"	"34cfe9aa-c2c0-11ea-9026-02e7594ce0a0"	"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"013dd0ca-832e-4434-94ad-3c8ce98f53f6"	"{""34cfea68-c2c0-11ea-9026-02e7594ce0a0"": ""380aac42-a519-43ce-a59d-e6a78edaad27""}"	"34cfe9c2-c2c0-11ea-9026-02e7594ce0a0"	"cfeab3e6-2b98-4866-b47a-905964d8c9f2"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"db237175-616d-4f0c-9d44-30a6b1c1c7e2"	"{""34cfea36-c2c0-11ea-9026-02e7594ce0a0"": {""ar"": {""value"": """", ""direction"": ""rtl""}, ""de"": {""value"": """", ""direction"": ""ltr""}, ""el"": {""value"": """", ""direction"": ""ltr""}, ""en"": {""value"": ""Thomas Huet"", ""direction"": ""ltr""}, ""fr"": {""value"": """", ""direction"": ""ltr""}, ""pt"": {""value"": """", ""direction"": ""ltr""}, ""ru"": {""value"": """", ""direction"": ""ltr""}, ""zh"": {""value"": """", ""direction"": ""ltr""}, ""en-US"": {""value"": """", ""direction"": ""ltr""}, ""en-us"": {""value"": """", ""direction"": ""ltr""}}, ""34cfea3d-c2c0-11ea-9026-02e7594ce0a0"": ""42b9542f-4678-457d-98f9-8235383bce1c"", ""34cfea65-c2c0-11ea-9026-02e7594ce0a0"": null, ""34cfea79-c2c0-11ea-9026-02e7594ce0a0"": ""6583ee43-7f87-4e19-b8f6-7add9d89dbc1"", ""34cfea7a-c2c0-11ea-9026-02e7594ce0a0"": null, ""34cfea7f-c2c0-11ea-9026-02e7594ce0a0"": null, ""34cfea92-c2c0-11ea-9026-02e7594ce0a0"": ""2012-04-04""}"	"34cfe99e-c2c0-11ea-9026-02e7594ce0a0"	"013dd0ca-832e-4434-94ad-3c8ce98f53f6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
"2846e9cd-21a2-45e5-8c11-89f0baa261d5"	"{""34cfea8e-c2c0-11ea-9026-02e7594ce0a0"": ""16bc979c-7291-45c5-b881-46f103ec2f0d""}"	"34cfe9bf-c2c0-11ea-9026-02e7594ce0a0"	"b48fbdf0-095d-4985-9b59-9aef8ae83aa6"	"dbc95d2d-38fb-465e-a6cb-0545eaa7584f"	0	
```
2. Identify UUID values with `whatisthis` or the RDM, and collect fields keys

* Condition: `34cfe9f5-c2c0-11ea-9026-02e7594ce0a0`

```SQL
SELECT value FROM values 
WHERE valueid::text IN
(
SELECT tiledata ->> '34cfe9f5-c2c0-11ea-9026-02e7594ce0a0' AS Condition
FROM tiles 
WHERE resourceinstanceid::text LIKE 'dbc95d2d-38fb-465e-a6cb-0545eaa7584f'
AND tiledata -> '34cfe9f5-c2c0-11ea-9026-02e7594ce0a0' IS NOT NULL
)
```

* Damage Extent Type: `34cfea8e-c2c0-11ea-9026-02e7594ce0a0`

```SQL
SELECT value FROM values 
WHERE valueid::text IN
(
SELECT tiledata ->> '34cfea8e-c2c0-11ea-9026-02e7594ce0a0' AS DamageExtentType
FROM tiles 
WHERE resourceinstanceid::text LIKE 'dbc95d2d-38fb-465e-a6cb-0545eaa7584f'
AND tiledata -> '34cfea8e-c2c0-11ea-9026-02e7594ce0a0' IS NOT NULL
)
```

* Assessment Activity Type: `34cfea4d-c2c0-11ea-9026-02e7594ce0a0`

```SQL
SELECT value FROM values 
WHERE valueid::text IN
(
SELECT tiledata ->> '34cfea4d-c2c0-11ea-9026-02e7594ce0a0' AS DamageExtentType
FROM tiles 
WHERE resourceinstanceid::text LIKE 'dbc95d2d-38fb-465e-a6cb-0545eaa7584f'
AND tiledata -> '34cfea4d-c2c0-11ea-9026-02e7594ce0a0' IS NOT NULL
)
```



* ...

* Generalised (in Python)

```py
import psycopg2
```

```py
field_uuid = '34cfea8e-c2c0-11ea-9026-02e7594ce0a0'
sqll = 
"""
SELECT value FROM values 
WHERE valueid::text IN
(
SELECT tiledata ->> '%s' AS DamageExtentType
FROM tiles 
WHERE resourceinstanceid::text LIKE 'dbc95d2d-38fb-465e-a6cb-0545eaa7584f'
AND tiledata -> '%s' IS NOT NULL
)
""" (field_uuid, field_uuid)
res = cursor.execute(sqll)
```

* Generalised (in Python) in a loop

4. Create a GUI in <https://colab.research.google.com/>, or equivalent, to let a user request on a UUID (HP's uuid, or BU's uuid)

~~https://github.com/eamena-project/eamena-arches-5-project/blob/master/eamena/statistics/hr_quality_rec.py~~

# Business data

Add new HP from a BU ([BU Upload](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#bulk-upload)), append new values ([BU append](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#bu-append)) and related resources ([r2r append](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#r2r-append)) in an existing HP, using templates and [functions](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#function). 

* Abrevv.

| Abrevv.  | Full name              |
|----------|------------------------|
| HP       | Heritage Place         |
| IR       | Information Resources  |
| PO       | Person/Organisation    |
| GS       | Grid Squares           |



## Bulk Upload
> BU

Bulk upload is a process for uploading **many HPs** data in one single XLSX file, and possibly **many XLSX** files, into the EAMENA database without going through the graphical user interface (see [DB diagram, "local" subgraph](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena#diagram)): it speeds up data entry. The BU process is handle by the Bulk-Uploader plugin in the EAMENA DB.

### Template files

The last/updated version of the BU template appears on the upper part of this table (first row of the table, not strikethrough):  
  
<p align="center">

| Name 	| Host 	| URL 	|
|------|------	|-----	|
| Bulk_Upload_template_240911.xlsx | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/Bulk_Upload_template_240911.xlsx |
| ~~Bulk_Upload_template_240701.xlsx~~ | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/Bulk_Upload_template_240701.xlsx |
| ~~Bulk_Upload_template_231017.xlsx~~ | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/Bulk_Upload_template_231017.xlsx |
| ~~Bulk_Upload_template_221025.xlsx~~ | GitHub | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/Bulk_Upload_template_221025.xlsx	|
| ~~E61N30-13-Revised.xls~~ | GitHub | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/E61N30-13-Revised.xlsx    	|
| ~~34cfe98e-c2c0-11ea-9026-02e7594ce0a0.xlsx~~ | EAMENA DB | https://database.eamena.org/en/bulk-upload/templates/34cfe98e-c2c0-11ea-9026-02e7594ce0a0.xlsx    	|
| ~~BUS_TemplateUpdate20072021.xlsx~~   	 | Google Drive	| https://drive.google.com/file/d/1KtZlCB_mdTOPxh1DpFdfeXddjJLTvF1k/view?usp=sharing    	|

</p>

#### How to fill an Heritage Place BU

Explanations of the BU fields (ex: `Name Type`) are [**here**](https://eamena.org/advanced-use#rm-hp-fields) while explanation on possible values are within the different sheets (ex: `Alternative Reference`)

<p align="center">
  <img alt="img-name" src="../../../www/bu-to-tsv.png" width="500">
  <br>
	<em>The BU template. In yellow, the different sheets where the dropdown values (ie. controled vocabularies) are coming from alongside value definitions</em>
</p>


#### Individual reference sheets

To make it easier to reference and share controlled vocabularies, the numerous BU template sheets (XLSX) can be converted into TSV files that can be read on GitHub using the [split_bu_template.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/functions/split_bu_template.py) function. For example:

```bash
py split_bu_template.py "Bulk_Upload_template_231017.xlsx" "C:/Rprojects/eamena-arches-dev/data/bulk/templates/doc"
```

<p align="center">
  <img alt="img-name" src="../../../www/bu-to-tsv.png" width="500">
  <br>
	<em>The BU template is a set of different templates. In yellow, example of the BU template sheets that will be exported as TSV file</em>
</p>



Will create the many TSV located into the folder https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/bulk_data/templates/doc: 
* [bu_Archaeological Assessment](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/doc/bu_Archaeological%20Assessment.tsv)
* [bu_Assessment Summary](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/doc/bu_Assessment%20Summary.tsv)
* [bu_Built Component](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/doc/bu_Built%20Component.tsv)
* ...

<p align="center">
  <img alt="img-name" src="../../../www/bu-to-tsv-ex1.png" width="700">
  <br>
	<em>A search on 'Rol' in the <a href="https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bulk/templates/doc/bu_Person-Organization.tsv">bu_Person-Organization</a> file</em>
</p>


## Data append

Data append entails (i) the append of usual data ([BU append](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#bu-append)), such as Alternative names, coordinates, etc., and (ii) the append of related resources ([r2r append](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#r2r-append)) in a HP. It is different from [Bulk Upload](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#bulk-upload).

```mermaid
flowchart
  subgraph ide1 [filter_business_data];
  id6[r2r];
  id8[bu];
  end;
  id3[Data append] -- run --> ide1;
  id6 -- creates --> id4[r2r append for IR];
  id6 -- creates --> id5[r2r append for PO];
  id8 -- creates --> id7[BU append];
  
  click ide1 https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data#filter_business_data
  click id3 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/append/bu_append_to_be_mapped.csv" _blank
  click id5 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/business_data_relations/res2res_hp_po.relations" _blank
  click id4 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/business_data_relations/res2res_hp_ir.relations" _blank
  click id7 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/append/Fazzan_bu_append.csv" _blank

```

* r2r: `python manage.py packages -o import_business_data_relations -s ...`
* BU append: `python manage.py packages -o import_business_data -s ...`

#### limits

see: [#57](https://github.com/eamena-project/eamena-arches-dev/issues/57#issuecomment-2334212067) and following

#### templates

[bulk_data_hp_template.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/bulk_data_hp_template.csv) or [bulk_data_hp_template_empty.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/bulk_data_hp_template_empty.csv)




### BU append
> BU append, Append data to an already existing record

A BU append is necessarly a CSV file. A mapping file (`.mapping`) is also necessary, cf: https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/mapping_files, do not include Related Resources (see: [#57](https://github.com/eamena-project/eamena-arches-dev/issues/57)). **ResourceID** is the only required field.

The process is `import_business_data -s 'path\to\bu_append_file' -ow append`

---

To create a BU from a structured file, or to recast structured data (source) to a BU format (target), see the [eamenaR](https://github.com/eamena-project/eamenaR#bu-mapping) package

---

#### Template files
> BU append templates

The last/updated version of the BU template appears on the upper part of this table (first row of the table, not strikethrough):  
  
<p align="center">

| Name 	| Host 	| URL 	| Description |
|------|------	|-----	|------       |
| Bulk_Append_template_240911.csv | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/templates/Bulk_Append_template_240911.csv | |
| ~~caravanserail_outCSV2.csv~~ | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/append/caravanserail_outCSV2.csv | Adding new geometries (Polygons) to HP (caravanserails). These geometries will be added to already existing geometries (Points) |
| ~~bu_append_hp_grid_20240116.csv~~ | GitHub  | https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/append/bu_append_gs.csv | Append missing GS to HP |


#### Fields

There are slight changes between the fieldnames in the BU template and the field names in the BU append template. The latter is closer to what exists in the database, with many remaining extra trailing spaces and some longer field names

<p align="center">
  <img alt="img-name" src="image.png" width="400">
  <img alt="img-name" src="image-1.png" width="400">
  <br>
	<em>Be careful about the trailing spaces in the DB (in blue). These extra spaces have to be added to some fieldnames in the BU file</em>
</p>


| BU template                                      | BU append template                                       | changes                                                    |
|--------------------------------------------------|----------------------------------------------------------|------------------------------------------------------------|
| Assessment Investigator - Actor                  | Assessment Investigator - Actor                          |                                                            |
| Investigator Role Type                            | Investigator Role Type                                   |                                                            |
| Assessment Activity Type                          | Assessment Activity Type                                 |                                                            |
| Assessment Activity Date                          | Assessment Activity Date                                 |                                                            |
| GE Assessment(Yes/No)                             | GE Assessment(Yes/No)                                    |                                                            |
| Resource Name                                     | Resource Name                                            |                                                            |
| Name Type                                         | Name Type                                                |                                                            |
| Heritage Place Type                               | Heritage Place Type                                      |                                                            |
| Heritage Place Function                           | Heritage Place Function                                  |                                                            |
| Heritage Place Function Certainty                 | Heritage Place Function Certainty                        | extra trailing space                                      |
| Site Overall Shape Type                           | Overall Site Shape Type                                  | different fieldname                                      |
| Overall Archaeological Certainty Value            | Overall Archaeological Certainty Value                   | extra trailing space                                      |
| Overall Site Morphology Type                      | Overall Site Morphology Type                             |                                                            |
| Cultural Period Type                              | Cultural Period Type                                     |                                                            |
| Cultural Period Certainty                         | Cultural Period Certainty                                |                                                            |
| Cultural Subperiod Type                           | Cultural Sub-period Type                                 | different field name                                      |
| Cultural Subperiod Certainty                      | Cultural Sub-period Certainty                            | different field name                                      |
| Date Inference Making Actor                       | Date Inference Making Actor Name                         | different field name                                      |
| Site Feature Form Type                            | Site Feature Form Type                                   |                                                            |
| Site Feature Form Type Certainty                  | Site Feature Form Type Certainty                         |                                                            |
| Site Feature Shape Type                           | Site Feature Shape Type                                  |                                                            |
| Site Feature Arrangement Type                     | Site Feature Arrangement Type                            |                                                            |
| Site Feature Number Type                          | Site Feature Number Type                                 |                                                            |
| Site Feature Interpretation Type                  | Site Feature Interpretation Type                         |                                                            |
| Site Feature Interpretation Number                | Site Feature Interpretation Number Type                  | different field name                                      |
| Site Feature Interpretation Certainty             | Site Feature Interpretation Certainty                     |                                                            |
| Overall Condition State                           | Overall Condition State Type                             |                                                            |
| Damage Extent Type                                | Damage Extent Type                                       |                                                            |
| Disturbance Cause Category Type                   |      Disturbance Cause Category Type                        |                                                            |
| Disturbance Cause Type                            |                                                          |                                                            |
| Disturbance Cause Certainty                       | Disturbance Cause Certainty                              | extra trailing space                                      |
| Disturbance Date From                             |                                                          |                                                            |
| Disturbance Date To                               | Disturbance Date To                                      | extra trailing space                                      |
| Disturbance Date Occurred Before                  |                                                          |                                                            |
| Disturbance Cause Assignment Assessor Name        | Disturbance Cause Assignment Assessor Name - Actor       | different field name                                      |
| Effect Type                                       |                                                          |                                                            |
| Effect Certainty                                  |                                                          |                                                            |
| Threat Category                                   |                                                          |                                                            |
| Threat Type                                       | Threat Cause Type                                        | different field name                                      |
| Threat Probability                                | Threat Probability                                       | extra trailing space                                      |
| Threat Inference Making Assessor Name             | Threat Inference Making Assessor Name - Actor            | different field name                                      |
| Topography Type                                   |                                                          |                                                            |

Correct fieldnames are listed here (CSV layout). Those can be copied and placed as header in the [Data to append](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/bulk_data/append/bu_append_to_be_mapped.csv) file (remember to keep the trailing spaces, etc.)

```
ResourceID, Assessment Investigator - Actor,Investigator Role Type,Assessment Activity Type,Assessment Activity Date,GE Assessment(Yes/No),Information Resource Used, Resource Name,Name Type,Heritage Place Type,Heritage Place Function,Heritage Place Function Certainty ,Overall Site Shape Type,Overall Archaeological Certainty Value ,Overall Site Morphology Type,Cultural Period Type,Cultural Period Certainty,Cultural Subperiod Type,Cultural Subperiod Certainty,Date Inference Making Actor Name,Site Feature Form Type,Site Feature Form Type Certainty,Site Feature Shape Type,Site Feature Arrangement Type,Site Feature Number Type,Site Feature Interpretation Type,Site Feature Interpretation Number,Site Feature Interpretation Certainty,Overall Condition State,Damage Extent Type,Disturbance Cause Category Type,Disturbance Cause Type,Disturbance Cause Certainty,Disturbance Date From,Disturbance Date To,Disturbance Date Occurred Before,Disturbance Cause Assignment Assessor Name,Effect Type,Effect Certainty,Threat Category,Threat Type,Threat Probability,Threat Inference Making Assessor Name,Topography Type
```

The reference is [hp-uuids.csv](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/rm/hp/hp-uuids.csv) (raw format), directly created from the RM. You can also check the name of the fields in the reference data [mds-template-readonly.tsv](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/mds-template-readonly.tsv) file  

#### validated fields

| RM | field | format and description |
|----|--------------|----------|
| HP | **ResourceID**   | the UUID of the ressource  |
| HP | Assessment Activity Date   | Date format `YYYY-MM-DD`   |
| HP | Disturbance Cause Category Type |   |
| HP | Disturbance Cause Type |   |
| HP | Disturbance Cause Certainty |   |
| HP | Disturbance Date From | Date format `YYYY-MM-DD` |
| HP | Disturbance Date To | Date format `YYYY-MM-DD`  |
| HP | Disturbance Date Occurred Before | Date format `YYYY-MM-DD`  |
| HP | Disturbance Date Occurred On |  Date format `YYYY-MM-DD` |
| HP | Disturbance Cause Assignment Assessor Name | Free text  |
| HP | Grid ID | |

#### invalid fields

Do not BU append these fields but choose [Resource-to-Resource](#resource-to-resource-relationship) import

| RM | field | format and description |
|----|--------------|----------|
| HP | Assessment Investigator - Actor   | this is a *related resource*, will create an error  |


### r2r append
> res2res, r2r, resource-to-Resource relationship append

To update a r2r relationships, for example between an HP and a PO (field 'Assessment Investigator - Actor' in HP), or between an HP and a IR (field 'Information Resource Used' in IR).

#### Import

the process is `import_business_data_relations -s 'path\to\relations_file'` will add a new r2r relationship.

##### Examples

* the [res2res_hp_ir.relations](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/business_data_relations/res2res_hp_ir.relations) file

| resourceinstanceidfrom              | resourceinstanceidto                | relationshiptype                                         | datestarted | dateended | notes |
|-------------------------------------|-------------------------------------|----------------------------------------------------------|-------------|-----------|-------|
| a882affc-60cb-4dcb-a26c-c2721fd0797c | ecdc771c-ff31-42c7-9ec9-522e6302e6f0 | http://www.cidoc-crm.org/cidoc-crm/P129i_is_subject_of   |             |           |       |

Where `a882affc-60cb-4dcb-a26c-c2721fd0797c` is an HP and `ecdc771c-ff31-42c7-9ec9-522e6302e6f0` is INFORMATION-0000052.

* the [res2res_hp_po.relations](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/business_data_relations/res2res_hp_po.relations) file

| resourceinstanceidfrom              | resourceinstanceidto                | relationshiptype                                   | datestarted | dateended | notes |
|-------------------------------------|-------------------------------------|----------------------------------------------------|-------------|-----------|-------|
| 1062dbf4-70a2-4b87-b0f1-0f459b6c3016 | 5bc25761-cf35-4350-b0cd-002b8c813d64 | http://www.ics.forth.gr/isl/CRMdig/L33_has_maker   |             |           |       |


Where `1062dbf4-70a2-4b87-b0f1-0f459b6c3016` is EAMENA-0264152 and `5bc25761-cf35-4350-b0cd-002b8c813d64` is Martin Sterry.

## Functions

Python functions. The generic function to manage Business data is [business_data.py](https://github.com/eamena-project/eamena-functions/blob/main/business_data.py) in the [eamena-functions](https://github.com/eamena-project/eamena-functions/) repo.

### filter_business_data()

Filter data that have to be uploaded by BU append function and data that to be append by r2r functions, see [filter_business_data()](https://github.com/eamena-project/eamena-functions/blob/main/business_data.py#L5).

# Reference data

* [MDS](reference_data/README.md)

# Resource models

---

# Others

* [GeoJSON URL to GeoJSON file](https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/business_data/geojsonUrl_to_geojsonFile.ipynb)
* SQL 

## ~~BU process~~
> ⚠️ This process is no longer in use ⚠️ ~~step-by-step BU procedure from the user-side~~

<p align="center">
  <img alt="img-name" src="../../../www/folder-files.png" width="600">
  <br>
	<em>The folder `2021-11-22-B-BIJAN` contains two XLSX files</em>
</p>


Start by creating a root `examples/` folder on **your OneDrive**, or equivalent, create and authorise the DB Manager to write only in this folder. See the 'ideal' file/folder naming/structure on the [examples/](https://github.com/eamena-project/eamena-arches-dev/tree/main/output/bulk/examples) folder. 

1. choose short and self-explanatory names for your **XLSX file(s)**, like the format *`GridSquare-GridSquareSubpart-YourName`* (ex: `E61N31-23-Bijan.xlsx`), avoiding dots and spaces in the filename (~~`E61 N31 23.Bijan.xlsx`~~) 

2. add the BUs worksheets in a **folder** named *`YYYY-MM-DD-YourName`* (ex: `2021-11-23-Bijan`). If you run various BUs processes during the same day, you will have to name your folders with different suffixes (ex: Bulk 1: `2021-11-22-Bijan`; Bulk 2: `2021-11-22a-Bijan`)

3. add your BU folders in the root root `examples/` folder. Send a **Slack message** (eamena.slack.com) to the DB Manager with the **link to the folder(s)** 

:-1: if **the BU doesn't work**, because of errors, the DB Manager will send you an **error report** in the form of an error JSON file named in the same way as your BU files (ex: [`E61N31-22-Bijan.json`](https://github.com/eamena-project/eamena-arches-dev/blob/main/output/bulk/examples/2021-11-21-Bijan/E61N31-21-Bijan.json))
  - follow the recommendations of the error JSON file, correcting the content of your file. Once done, change the name of your file to something explicit, e.g. adding the suffix `-rev` (for `revised`) at the end of the file name (ex: `E61N31-22-Bijan.xlsx` -> `E61N31-22-Bijan-rev.xlsx`)

:+1: if **the BU works**, the DB Manager will send you a **confirmation** that your BU has been uploaded, and the JSON output will be uploaded into the **same OneDrive folder** as your BUs worksheets 
  - if you ask to, the DB Manager will send you a [BU summary](https://github.com/eamena-project/eamena-arches-dev/blob/main/output/bulk/BU.md#bu-summary) in the form of a JSON file named in the same way as your BU files with the suffix `-sum` (for `summary`), ex: [`E61N31-22-Bijan-rev-sum.json`](https://github.com/eamena-project/eamena-arches-dev/blob/main/output/bulk/examples/2021-11-21-Bijan/E61N31-21-Bijan-rev-sum.json)

4. once you received the confirmation that your BU has been uploaded into the DB, **move your BU folder into an archive folder** 


## BU summary
> After a successfull BU, render a short summary for the user

Once the BU process has been completed, a resume can be displayed with a Python command[^1]. The result is copied/pasted in a JSON file. A Search &Replace allows to convert the UUID into an URL[^2]


<p align="center">
  <img alt="img-name" src="../../../www/json_summary.png" width="500">
  <br>
	<em>screenshot of the JSON with URL</em>
</p>

The URL opens the Resource Report

<p align="center">
  <img alt="img-name" src="../../../www/json_summary_uuid.png" width="700">
  <br>
	<em>screenshot of the Resource Report</em>
</p>

The Resource name can be search in the map database

<p align="center">
  <img alt="img-name" src="../../www/json_summary_uuid_search.png" width="700">
  <br>
	<em>screenshot of the Resource Report</em>
</p>


[^1]: `python /opt/arches/eamena/manage.py bu -o summary -s "filename.json" | json_pp`
[^2]: Search: `"uuid" : "`, Replace by `"uuid" : "https://database.eamena.org/en/report/`