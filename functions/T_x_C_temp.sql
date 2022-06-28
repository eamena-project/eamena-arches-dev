SELECT * FROM tiles
WHERE resourceinstanceid IN
(
SELECT resourceinstanceid FROM tiles
WHERE resourceinstanceid::text like 'cb52672e-7bf0-4097-afda-86686d59cf31'
)

SELECT value FROM values 
WHERE valueid = '63649eae-36a8-40e1-97e1-43fc74c0d1d9'
-- LIMIT 10

SELECT 
tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0' as ThreatCat,
tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssessDat
--nodegroupid
FROM tiles 
WHERE resourceinstanceid::text like 'cb52672e-7bf0-4097-afda-86686d59cf31'
AND ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
	) --AND tiles IS NOT NULL
	
SELECT 
tiles.tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
values.value as ThreatCat,
tiles.tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssessDat
FROM tiles LEFT JOIN values ON
values.valueid::text = tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0'
WHERE ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
	) --AND tiles IS NOT NULL
AND resourceinstanceid::text like 'cb52672e-7bf0-4097-afda-86686d59cf31'

SELECT 
tiles.tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
values.value as ThreatCat,
tiles.tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssessDat,
resourceinstanceid as ResourceID
FROM tiles LEFT JOIN values ON
values.valueid::text = tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0'
WHERE ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
	) --AND tiles IS NOT NULL
LIMIT 100