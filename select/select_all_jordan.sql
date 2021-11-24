SELECT nodes.nodeid, geojson_geometries.geom
FROM nodes, geojson_geometries
WHERE nodes.nodeid = geojson_geometries.nodeid
AND ST_Overlaps( JORDAN_GEOM, geojson_geometries.geom)
-- LIMIT 20
