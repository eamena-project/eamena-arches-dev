# SQL and Advanced Search queries

Miscellaneous and compendium of equivalent queries between Advanced Search and SQL queries for frontend and backend querying. These queries are too specific to be added to the [eamenaR](https://github.com/eamena-project/eamenaR) package

* Abrevv.

| Abrevv. | Full name |
|----------|----------|
| HP | Heritage Place |
| AS | Advanced Search |

Main correspondances between EAMENA fieldnames and field UUIDs are listed here: https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/data_quality/mds-template-readonly.tsv


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



# Other


## URL

The **Search URL** is the URL in the web search bar, while the **GeoJSON URL** is the API URL that can be exported (or copied) here in green:

![](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/geojson-export.png)
