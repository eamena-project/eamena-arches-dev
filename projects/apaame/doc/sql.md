# SQL snippets

## 1

Select images ressources from the IR

```SQL
SELECT q1.ir_id, q1.ir_num, q2.apaame_num, img_url, img_name
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS ir_num
    FROM tiles
    WHERE resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
	AND tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
) q1
INNER JOIN(
	SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS apaame_num
    FROM tiles
    WHERE resourceinstanceid::text LIKE '45ea21b3-5434-442e-98ab-a83851611128' 
	AND tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
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

Gives

| ir_id  	|  ir_num 	|  apaame_num 	|  img_url 	|  img_name 	|
|---	|---	|---	|---	|---	|
|  45ea21b3-5434-442e-98ab-a83851611128	|   INFORMATION-0088488	|  APAAME_20091019_DDB-0250 	|   /files/601bc682-2d7f-44af-9f23-e2d71f89e08e	|  APAAME_20091019_DDB-0250.jpg 	|

---