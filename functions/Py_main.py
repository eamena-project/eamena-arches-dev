from _conn import conn
from Py_functions import get_uuid_from_eaid, get_geom_from_uuid, get_related_resources_from_uuid, get_geom_from_uuid, export_geom_from_urlgeojson
from Py_sources import testdb_hp_fields, testdb_bc_fields

conn = conn("24")
cur = conn.cursor()

my_uuid = get_uuid_from_eaid('EAMENA-0181523')
# my_geom = get_geom_from_uuid(my_uuid)
# my_related_resources = get_related_resources_from_uuid(my_uuid)
my_geom = get_geom_from_uuid('2a774cbd-d13f-41ce-8af1-292344bd4dff', 'bc')
export_geom_from_urlgeojson(out_geom_name = "new_new_new_geojson")


# - - - - - - - - - - - - -
cur.close()