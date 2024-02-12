# Reference Data

* [Heritage Places](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#heritage-places)
* [Information Resources](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#information-resources)

## Heritage Places

### UUIDs

Fieldnames (ex: "Effect type") have UUIDs. To find these correspondances, check the `nodeid` in the RM. For example, the "Effect type" field has the UUID `34cfea90-c2c0-11ea-9026-02e7594ce0a0`, see:

- https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Heritage%20Place.json#L2036

- https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Heritage%20Place.json#L6530


### MDS
> Minimum Data Standards. Completness of data

Minimum Data Standards (MDS) of Heritage Places

#### Files

##### Templates

The template `mds-template-*` is the reference table for the MDS, fieldnames' descriptions, and for the eamenaR mapping file `ids.csv` (see [eamenaR documentation](https://github.com/eamena-project/eamenaR#correspondances-between-concept-labels-and-uuids))

* [mds-template.xlsx](mds/mds-template.xlsx):
	- an editable XLSX file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This file is considered to be the authorative document for mds.

* [mds-template-readonly.tsv](mds/mds-template-readonly.tsv):
	- a read-ony TSV file with the list of HP fields with their UUID and a "Yes" mark if these fields belong to the mds. This files results from the automatic export of [mds-template.xlsx](mds/mds-template.xlsx), it will be overwrite each time 'mds-template.xlsx' is updated)


**Level of aggregation**

It means that fields, and field and field values (`level3`) can be aggregated and sum up into broader categories (`level1` and `level2`). 

#### Scripts

* [mds-reference.ipynb](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/mds-reference.ipynb)
  - a Jupyter/Python document to run mds reference
* [mds-assessment.ipynb](https://github.com/eamena-project/eamena-functions/blob/main/mds/mds.ipynb):
	- a Jupyter/Python document to run mds assessement on heritage places
* [convert_xlsx_to_tsv.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/convert_xlsx_to_tsv.py):
	- a Python simple script to convert 'mds-template.xlsx' into 'mds-template-readonly.tsv'. This script is run automatically, in a GitHub Action with [mds-to-tsv.yml](https://github.com/eamena-project/eamena-arches-dev/blob/main/.github/workflows/mds-to-tsv.yml), each time 'mds-template.xlsx' is updated.


<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/audit-data-mds-excel.png" width="1000">
  <br>
    <em>A screenshot of the editable 'mds-template.xlsx'</em>
</p>


#### Interactivity

MDS fields in this HTML circular plot ([here](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/mds/mds-reference.html))

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-mds-pie.png" width="600">
  <br>
    <em>A screenshot of the `mds_level.html` file showing the 98 fields of the Heritage Places with the MDS fields (highlighted, thumbs up) using the `mds-reference.ipynb` script</em>
</p>

The Entity-relationships diagram of HP with fieldnames and CIDOC-CRM entities and relationships ([here](https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/erd/EAMENA-erd.html))

<p align="center">
  <img alt="img-name" src="https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-v7-hp-data-erd.png" width="650">
  <br>
    <em>A screenshot of the `EAMENA-erd.html` file (detail) showing the 98 fields of the Heritage Places with the MDS fields (colored, thumbs up) using the `EAMENA-erd.ipynb` script</em>
</p>


## Other

Check the completness of data. Python function to model the quality of HP with a radar diagram based on the groups appearing in the BU file (different levels of data agregation and summing):

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

## Information Resources

field names' UUIDs are listed here: [ir-uuids-readonly.tsv](ir-uuids-readonly.tsv). The Pyton script that generate this file is [nodes_id.ipynb](nodes_id.ipynb)

## Other

~~https://github.com/eamena-project/eamena-arches-5-project/blob/master/eamena/statistics/hr_quality_rec.py~~



