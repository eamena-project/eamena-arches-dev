-- SELECT nodes.nodeid, geojson_geometries.geom
-- FROM nodes, geojson_geometries
-- WHERE nodes.nodeid = geojson_geometries.nodeid
-- AND ST_Overlaps(JORDAN_GEOM, geojson_geometries.geom)
-- LIMIT 20

-- by Galen Mancino
select resource_instances.resourceinstanceid, resource_x_resource.resourceinstanceidfrom, resource_instances.graphid from resource_instances
inner join resource_x_resource on resource_instances.resourceinstanceid = resource_x_resource.resourceinstanceidfrom
where resource_instances.graphid = '81212939-f98a-11e9-b345-06f597a7d5ce'
group by resource_instances.graphid, resource_instances.resourceinstanceid, resource_x_resource.resourceinstanceidfrom
having count(resource_x_resource.resourcexid) > 4;
