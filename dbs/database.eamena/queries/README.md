# SQL and Advanced Search queries

Miscellaneous and compendium of equivalent queries between Advanced Search and SQL queries for frontend and backend querying. These queries are too specific to be added to the [eamenaR](https://github.com/eamena-project/eamenaR) package


* Abrevv.

| Abrevv. | Full name |
|----------|----------|
| AS | EAMENA Advanced Search |
| GS | Grid Squares |
| HP | Heritage Place |

* UUID and fiel names

Main correspondances between EAMENA Heritage Places fieldnames and field UUIDs are listed here: https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds-template-readonly.tsv

---

[APAAME dev](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/queries#apaame-and-archdams)


## Total number of HP

* SQL

```SQL
SELECT COUNT(resourceinstanceid::text) FROM resource_instances
WHERE graphid::text LIKE '34cfe98e-c2c0-11ea-9026-02e7594ce0a0'
```

* AS

```
https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&reportlink=false&precision=6&total=368511&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D
```

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

## examples

### ex1

#### APAAME ID of a given IR

Using 

```SQL
SELECT tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS apaame_num FROM tiles 
WHERE resourceinstanceid::text LIKE '88ab19b3-1f4c-40ba-9467-55ef66fc9f26' 
AND tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
```


# Other


## URL

The **Search URL** is the URL in the web search bar, while the **GeoJSON URL** is the API URL that can be exported (or copied) here in green:

![](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/geojson-export.png)
