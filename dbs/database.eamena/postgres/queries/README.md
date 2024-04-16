# SQL and Advanced Search queries

Miscellaneous and compendium of equivalent queries between Advanced Search and SQL queries for frontend and backend querying. These queries are too specific to be added to the [eamenaR](https://github.com/eamena-project/eamenaR) package


* Abrevv.

| Abrevv. | Full name |
|----------|----------|
| AS | EAMENA Advanced Search |
| GS | Grid Squares |
| HP | Heritage Place |

* UUID and fiel names

Main correspondances between EAMENA Heritage Places fieldnames and field UUIDs are listed here: https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/mds/mds-template-readonly.tsv

---

[APAAME dev](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/queries#apaame-and-archdams)

## User permissions

Create the `eamenar_temp` with a password and revokes all his pervious privileges (see [Reuben's notes](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/postgres#creating-a-readonly-postgres-user))

```SQL
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM eamenar_temp;
REVOKE ALL PRIVILEGES ON SCHEMA public FROM eamenar_temp;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM eamenar_temp;
REVOKE ALL PRIVILEGES ON DATABASE eamena FROM eamenar_temp;
```

Grant a `SELECT` permission (i.e. read-only) on a specific view

```SQL
GRANT SELECT ON nb_hp_by_gs TO eamenar_temp;
```

Check the `eamenar_temp` user permissions

```SQL
SELECT table_catalog, table_schema, table_name, privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'eamenar_temp'
```

## Total number of HP

* SQL

```SQL
SELECT COUNT(resourceinstanceid::text) FROM resource_instances
WHERE graphid::text LIKE '34cfe98e-c2c0-11ea-9026-02e7594ce0a0'
```

where:

- `34cfe98e-c2c0-11ea-9026-02e7594ce0a0` is the UUID of the HP resource model, see [the RM](https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Heritage%20Place.json#L14)

gives:

- 207,409

* AS

```
https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&reportlink=false&precision=6&total=368511&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D
```

## Total number of IR

```SQL
SELECT COUNT(resourceinstanceid::text) FROM resource_instances
WHERE graphid::text LIKE '35b99cb7-379a-11ea-9989-06f597a7d5ce'
```

where:
- `35b99cb7-379a-11ea-9989-06f597a7d5ce'` is the UUID of the IR resource model, see [the RM](https://github.com/achp-project/prj-eamena-marea/blob/8e397ad1343cd7fb04e4ca8a50247a1e3a687cb2/resource_models/Information%20Resource.json#L27)

gives:

- 136,442

## All the data of a specific HP

```SQL
SELECT * FROM tiles 
WHERE resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128'
```

Where `45ea21b3-5434-442e-98ab-a83851611128` is the UUID of a HP


## HP with Overall Site Condition
> HP having a value in OSC

* SQL 

```SQL
SELECT COUNT(resourceinstanceid::text) FROM tiles 
WHERE tiledata ->> '34cfe9f5-c2c0-11ea-9026-02e7594ce0a0'::text is not NULL
```
* AS

```
https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&reportlink=false&precision=6&total=368511&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfe9f5-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22not_null%22%2C%22val%22%3A%22%22%7D%7D%5D
```

NB: use `34cfea68-c2c0-11ea-9026-02e7594ce0a0` for Disturbance Cause Category Type	


## HP centroids


* SQL

```SQL
SELECT ids.ri, ids.ei, coords.x, coords.y FROM (
-- EAMENA ID
SELECT * FROM (
SELECT
resourceinstanceid::TEXT AS ri,
tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0'::text as ei
FROM tiles
) AS x
WHERE ei IS NOT NULL
) AS ids,
(
-- coordinates
SELECT * FROM (
SELECT
resourceinstanceid::TEXT AS ri,
ST_X(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) x,
ST_Y(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) y
FROM tiles
) AS x
WHERE x IS NOT NULL AND y IS NOT NULL
) AS coords
WHERE ids.ri = coords.ri
ORDER BY ei
LIMIT 10
```

## HP without GS

* SQL

```SQL
SELECT ids.ri, ids.ei, coords.x, coords.y FROM (
-- EAMENA ID
SELECT * FROM (
SELECT
resourceinstanceid::TEXT AS ri,
tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0'::text as ei
FROM tiles
) AS x
WHERE ei IS NOT NULL
) AS ids,
(
-- coordinates
SELECT * FROM (
SELECT
resourceinstanceid::TEXT AS ri,
ST_X(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) x,
ST_Y(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) y
FROM tiles
) AS x
WHERE x IS NOT NULL AND y IS NOT NULL
) AS coords
WHERE ids.ri = coords.ri
EXCEPT
SELECT ids.ri, ids.ei, coords.x, coords.y FROM (
	-- EAMENA ID
	SELECT * FROM (
		SELECT
		resourceinstanceid::TEXT AS ri,
		tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0'::text as ei
		FROM tiles
		) AS x
	WHERE ei IS NOT NULL
	) AS ids,
	(
	-- coordinates
	SELECT * FROM (
		SELECT
		resourceinstanceid::TEXT AS ri,
		ST_X(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) x,
		ST_Y(ST_AsText(ST_Centroid(ST_GeomFromGeoJSON(tiledata -> '5348cf67-c2c5-11ea-9026-02e7594ce0a0' -> 'features' -> 0 -> 'geometry')))) y
		FROM tiles
		) AS x
	WHERE x IS NOT NULL AND y IS NOT NULL
	) AS coords,
	(
	-- coordinates
	SELECT * FROM (
		SELECT
		resourceinstanceid::TEXT AS ri,
		tiledata ->> '34cfea5d-c2c0-11ea-9026-02e7594ce0a0'::text as gr
		FROM tiles
		) AS x
	WHERE gr IS NOT NULL
	) AS grd
WHERE ids.ri = coords.ri AND grd.ri = coords.ri AND grd.ri = ids.ri
```

# APAAME and ArchDAMS
> IR 

SQL queries to work with IR and APAAME resources

---

**useful links**:

- [APAAME project](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/README.md#workflow)
- [Reference data](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data) for UUIDs

---

## examples

### ex1

#### APAAME ID of a given IR

Using INFORMATION-0052511 (UUID: `88ab19b3-1f4c-40ba-9467-55ef66fc9f26`), 

* APAAME ID

```SQL
SELECT tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id FROM tiles 
WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
AND resourceinstanceid::text LIKE '88ab19b3-1f4c-40ba-9467-55ef66fc9f26' 
```

where:
* `341f9905-5253-11ea-a3f7-02e7594ce0a0` is the "Catalogue ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L13))
* `88ab19b3-1f4c-40ba-9467-55ef66fc9f26` is the HP INFORMATION-0052511's UUID


Returns:

| catalog_id |
|----------|
| SL00/4.33 (RHB)    |
| APAAME_20000906_RHB-0018    |

* File Upload

This is location of the image, it can be an URL

```SQL
SELECT tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS file_upload FROM tiles 
WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
AND resourceinstanceid::text LIKE '88ab19b3-1f4c-40ba-9467-55ef66fc9f26' 
```

where:
* `c712066a-8094-11ea-a6a6-02e7594ce0a0` is the "File Upload" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/a0d644aa376bfce54afa465974f74db821832f52/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L64))

Returns:

| file_upload |
|----------|
| https://live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg    |

## ex2


### 2.1

Select images ressources from INFORMATION-0088488

```SQL
SELECT q1.ir_id, q1.information_id, q2.catalog_id, img_url, img_name
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS information_id
    FROM tiles
    WHERE tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
    AND resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
) q1
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
    FROM tiles
    WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
    AND resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
) q2
ON q1.ir_id = q2.ir_id
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url,
	tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, name}' AS img_name
    FROM tiles
    WHERE resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
	AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
) q3
ON q1.ir_id = q3.ir_id;
```

where:
* `4c403a80-8a3d-11ea-a6a6-02e7594ce0a0` is the "INFORMATION ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L33))
* `45ea21b3-5434-442e-98ab-a83851611128` is INFORMATION-0088488
* `341f9905-5253-11ea-a3f7-02e7594ce0a0` is the "Catalogue ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L13))
* `c712066a-8094-11ea-a6a6-02e7594ce0a0` is the "File Upload" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/a0d644aa376bfce54afa465974f74db821832f52/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L64))

gives:

| ir_id  	|  information_id 	|  catalog_id 	|  img_url 	|  img_name 	|
|---	|---	|---	|---	|---	|
|  45ea21b3-5434-442e-98ab-a83851611128	|   INFORMATION-0088488	|  APAAME_20091019_DDB-0250 	|   /files/601bc682-2d7f-44af-9f23-e2d71f89e08e	|  APAAME_20091019_DDB-0250.jpg 	|

---

### 2.2

Select all IR having a Catalog ID not NULL (limit to 20)

```SQL
SELECT q1.ir_id, q1.information_id, q2.catalog_id, img_url, img_name
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS information_id
    FROM tiles
	WHERE tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
) q1
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
    FROM tiles
	WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
) q2
ON q1.ir_id = q2.ir_id
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url,
	tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, name}' AS img_name
    FROM tiles
	WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
) q3
ON q1.ir_id = q3.ir_id
LIMIT 5;
```

where:
* `4c403a80-8a3d-11ea-a6a6-02e7594ce0a0` is the "INFORMATION ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L33))
* `341f9905-5253-11ea-a3f7-02e7594ce0a0` is the "Catalogue ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L13))
* `c712066a-8094-11ea-a6a6-02e7594ce0a0` is the "File Upload" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/a0d644aa376bfce54afa465974f74db821832f52/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L64))

gives:

<a name="id-catalog"></a>

|ir_id                                |information_id              |catalog_id                               |img_url                                                                                 |img_name                                     |
|:------------------------------------|:-------------------|:----------------------------------------|:---------------------------------------------------------------------------------------|:--------------------------------------------|
|000117a1-b1e2-4e09-b676-124be29a05d4 |INFORMATION-0033853 |APAAME_20141020_RHB-0143                 |https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg                       |15784162651_852ef747a0_o_d.jpg               |
|00012dab-00cf-4cf1-90b5-d09c5cf3c6d6 |INFORMATION-0090288 |APAAME_20091008_KRH-0062                 |https://live.staticflickr.com/7559/15976540576_f78c5c5355_o_d.jpg                       |15976540576_f78c5c5355_o_d.jpg               |
|0002dce4-8a0b-4eb4-908f-92ec2eff8fa8 |INFORMATION-0101891 |APAAME_20100516_RHB-0082                 |https://live.staticflickr.com/4013/4616248328_0610d38320_o_d.jpg                        |4616248328_0610d38320_o_d.jpg                |
|00030cf8-6a42-46d8-9542-ba6c42b06772 |INFORMATION-0095691 |APAAME_20181017_RHB-0098                 |https://live.staticflickr.com/1923/45408035381_012a36622f_o_d.jpg                       |45408035381_012a36622f_o_d.jpg               |
|000348ec-dd61-48bb-97be-6ca6677d5fbe |INFORMATION-0110777 |APAAME_20101021_KRH-0050                 |https://live.staticflickr.com/1244/5135603365_88730e84ef_o_d.jpg                        |5135603365_88730e84ef_o_d.jpg                |


### 2.3

Same as 2.2, but only Flickr URLs

```SQL
SELECT q1.ir_id, q1.information_id, q2.catalog_id, img_url
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS information_id
    FROM tiles
  WHERE tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
) q1
INNER JOIN(
  SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
    FROM tiles
  WHERE tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
) q2
ON q1.ir_id = q2.ir_id
INNER JOIN(
  SELECT
    resourceinstanceid AS ir_id,
    tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' AS img_url
    FROM tiles
  WHERE tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' IS NOT NULL
  AND tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' #>> '{0, url}' LIKE 'https://live.staticflickr%'
) q3
ON q1.ir_id = q3.ir_id
```

where:
* `4c403a80-8a3d-11ea-a6a6-02e7594ce0a0` is the "INFORMATION ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L33))
* `341f9905-5253-11ea-a3f7-02e7594ce0a0` is the "Catalogue ID" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/5584e36842825dfd8d60c5b368bf7186ab72a39e/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L13))
* `c712066a-8094-11ea-a6a6-02e7594ce0a0` is the "File Upload" field UUID ([here](https://github.com/eamena-project/eamena-arches-dev/blob/a0d644aa376bfce54afa465974f74db821832f52/dbs/database.eamena/data/reference_data/ir-uuids-readonly.tsv#L64))

# Other


## URL

The **Search URL** is the URL in the web search bar, while the **GeoJSON URL** is the API URL that can be exported (or copied) here in green:

![](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/geojson-export.png)
