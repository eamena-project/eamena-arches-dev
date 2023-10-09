# SQL snippets

SQL queries to work with IR and APAAME resources

## 1

Select images ressources from the IR `45ea21b3-5434-442e-98ab-a83851611128`

```SQL
SELECT q1.ir_id, q1.ir_num, q2.catalog_id, img_url, img_name
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
    tiledata -> '341f9905-5253-11ea-a3f7-02e7594ce0a0' -> 'en' ->> 'value' AS catalog_id
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

| ir_id  	|  ir_num 	|  catalog_id 	|  img_url 	|  img_name 	|
|---	|---	|---	|---	|---	|
|  45ea21b3-5434-442e-98ab-a83851611128	|   INFORMATION-0088488	|  APAAME_20091019_DDB-0250 	|   /files/601bc682-2d7f-44af-9f23-e2d71f89e08e	|  APAAME_20091019_DDB-0250.jpg 	|

---

### 1.1

Select all IR having a Catalog ID (`4c403a80-8a3d-11ea-a6a6-02e7594ce0a0`) not NULL (limit to 20)

```SQL
SELECT q1.ir_id, q1.ir_num, q2.catalog_id, img_url, img_name
FROM (
    SELECT
    resourceinstanceid AS ir_id,
    tiledata -> '4c403a80-8a3d-11ea-a6a6-02e7594ce0a0' -> 'en' ->> 'value' AS ir_num
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
LIMIT 20;

```

Gives

<a name="id-catalog"></a>

|ir_id                                |ir_num              |catalog_id                               |img_url                                                                                 |img_name                                     |
|:------------------------------------|:-------------------|:----------------------------------------|:---------------------------------------------------------------------------------------|:--------------------------------------------|
|000117a1-b1e2-4e09-b676-124be29a05d4 |INFORMATION-0033853 |APAAME_20141020_RHB-0143                 |https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg                       |15784162651_852ef747a0_o_d.jpg               |
|00012dab-00cf-4cf1-90b5-d09c5cf3c6d6 |INFORMATION-0090288 |APAAME_20091008_KRH-0062                 |https://live.staticflickr.com/7559/15976540576_f78c5c5355_o_d.jpg                       |15976540576_f78c5c5355_o_d.jpg               |
|0002dce4-8a0b-4eb4-908f-92ec2eff8fa8 |INFORMATION-0101891 |APAAME_20100516_RHB-0082                 |https://live.staticflickr.com/4013/4616248328_0610d38320_o_d.jpg                        |4616248328_0610d38320_o_d.jpg                |
|00030cf8-6a42-46d8-9542-ba6c42b06772 |INFORMATION-0095691 |APAAME_20181017_RHB-0098                 |https://live.staticflickr.com/1923/45408035381_012a36622f_o_d.jpg                       |45408035381_012a36622f_o_d.jpg               |
|000348ec-dd61-48bb-97be-6ca6677d5fbe |INFORMATION-0110777 |APAAME_20101021_KRH-0050                 |https://live.staticflickr.com/1244/5135603365_88730e84ef_o_d.jpg                        |5135603365_88730e84ef_o_d.jpg                |
|00043464-0e2b-478b-b7fa-f957575bcf1e |INFORMATION-0075120 |APAAME_20170927_MND-0067                 |https://live.staticflickr.com/4443/36914020933_9abbd87dbd_o_d.jpg                       |36914020933_9abbd87dbd_o_d.jpg               |
|00057705-b4da-437e-a075-08ec9b499296 |INFORMATION-0104221 |APAAME_20100601_DDB-0153                 |https://live.staticflickr.com/4137/4907412552_43e6119bd9_o_d.jpg                        |4907412552_43e6119bd9_o_d.jpg                |
|00065c87-42b1-4e3f-9b88-d0ac1f10df5e |INFORMATION-0024585 |APAAME_20130428_DDB-0358                 |https://live.staticflickr.com/7282/8741111142_a8ebe9c19b_o_d.jpg                        |8741111142_a8ebe9c19b_o_d.jpg                |
|00067e65-aa23-4949-aa6e-2f2147ab845c |INFORMATION-0026892 |APAAME_20141012_REB-0063                 |https://live.staticflickr.com/5613/15370938680_9557e2c641_o_d.jpg                       |15370938680_9557e2c641_o_d.jpg               |
|0006b31f-db5f-49c6-8c4f-7d44a09805bc |INFORMATION-0053706 |SL02/1-28                                |https://live.staticflickr.com/4103/4973742302_ed7949c432_o_d.jpg                        |4973742302_ed7949c432_o_d.jpg                |
|0006b31f-db5f-49c6-8c4f-7d44a09805bc |INFORMATION-0053706 |APAAME_20020401_RHB-0028                 |https://live.staticflickr.com/4103/4973742302_ed7949c432_o_d.jpg                        |4973742302_ed7949c432_o_d.jpg                |
|0006c625-5acc-4d18-b301-ef7e4142ec3a |INFORMATION-0079245 |SL98/7.11                                |https://live.staticflickr.com/3669/9319637095_61eb538bbd_o_d.jpg                        |9319637095_61eb538bbd_o_d.jpg                |
|0006c625-5acc-4d18-b301-ef7e4142ec3a |INFORMATION-0079245 |APAAME_19980512_DLK-0058                 |https://live.staticflickr.com/3669/9319637095_61eb538bbd_o_d.jpg                        |9319637095_61eb538bbd_o_d.jpg                |
|00073fc5-fb77-43f9-bf4b-c63e8db2eb4c |INFORMATION-0141654 |APAAME_20191022_PF-0077                  |https://live.staticflickr.com/65535/49553345351_64f9bf52db_o_d.jpg                      |49553345351_64f9bf52db_o_d.jpg               |
|0007ba59-2b07-4e16-92af-e898cd84c4e6 |INFORMATION-0028034 |APAAME_20141013_MND-0213                 |https://live.staticflickr.com/3932/15419496628_7e7d1a76fb_o_d.jpg                       |15419496628_7e7d1a76fb_o_d.jpg               |
|00085a1a-753c-4475-b053-ed91ccdb112c |INFORMATION-0068379 |AP786                                    |https://live.staticflickr.com/4196/35567537936_acd0ee769d_o_d.jpg                       |35567537936_acd0ee769d_o_d.jpg               |
|00085a1a-753c-4475-b053-ed91ccdb112c |INFORMATION-0068379 |UCLCA/IA/C/1                             |https://live.staticflickr.com/4196/35567537936_acd0ee769d_o_d.jpg                       |35567537936_acd0ee769d_o_d.jpg               |
|00088a67-db92-4f89-b0fe-782244abab49 |INFORMATION-0144482 |JORDAN_45B-SQN_JordanValley_Run-10_10848 |https://eamena-uploads-v2.s3.amazonaws.com/JORDAN_45B-SQN_JordanValley_Run-10_10848.jpg |JORDAN_45B-SQN_JordanValley_Run-10_10848.jpg |
|0008f5cc-2ab8-4edd-bd73-66535822d966 |INFORMATION-0092303 |APAAME_20090917_DLK-0212                 |https://live.staticflickr.com/2482/4192526976_b2b35c7ac0_o_d.jpg                        |4192526976_b2b35c7ac0_o_d.jpg                |
|000b5730-5b56-4328-a892-7026eeb3801d |INFORMATION-0070199 |ASA/3/423                                |https://live.staticflickr.com/7780/17403206596_a73079d051_o_d.jpg 