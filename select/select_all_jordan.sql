SELECT nodes.nodeid, geojson_geometries.geom
FROM nodes, geojson_geometries
WHERE nodes.nodeid = geojson_geometries.nodeid
AND ST_Overlaps(geojson_geometries.geom, JORDAN_GEOM)
-- LIMIT 20
