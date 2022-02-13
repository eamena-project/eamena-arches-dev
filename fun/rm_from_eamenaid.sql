DELETE FROM tiles WHERE tiles.tiledata IN (SELECT t.tiledata
FROM tiles t
LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
WHERE (t.tiledata::json -> n.nodeid::text)::text like '%EAMENA-0187145%')