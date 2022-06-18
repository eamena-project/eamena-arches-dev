from _conn import conn
from Py_sources import testdb_hp_fields, testdb_bc_fields
import psycopg2
import psycopg2.extras


conn = conn("24")
cur = conn.cursor()

def get_uuid_from_eaid(eamenaid):
    """
    Retrieve the UUID of an Heritage Place from its EAMENA ID
    :param eamenaid: The EAMENA ID
    :type eamenaid: string
    :return: UUID
    :Example:
    >>> print(get_uuid_from_eaid('EAMENA-0181523'))
    cb52672e-7bf0-4097-afda-86686d59cf31
    """
    sql="SELECT resourceinstanceid FROM tiles t \
    LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid \
    WHERE (t.tiledata::json -> n.nodeid::text)::text like '%{0}%'".format(eamenaid)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(sql)
    uuid = dict_cur.fetchone()[0]
    return(uuid)

def get_geom_from_uuid(uuid,restyp):
    """
    Retrieve the geometry of an Heritage Place from its UUID

    Select the GeoJSON object in the tiledata field
    :param uuid: The UUID
    :param restyp: The type of resource, hp for 'Heritage Place', or bc for 'Built Component'
    :type uuid: UUID
    :return: geojson
    :Example:
    >>> my_uuid = get_uuid_from_eaid('EAMENA-0181523')
    >>> get_geom_from_uuid(my_uuid)
    TODO
    """
    if(restyp == 'hp'):
        sql="SELECT tiledata->>'{0}' as my_geojson FROM tiles \
        WHERE resourceinstanceid = '{1}' \
        AND nodegroupid = '{2}'".format(testdb_hp_fields["Geometric Place Expression"], uuid, testdb_hp_fields["geometry"])
        print(sql)
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(sql)
        mygeom = dict_cur.fetchone()[0]
        return(mygeom)
    if(restyp == 'bc'):
        sql="SELECT tiledata->>'{0}' as my_geojson FROM tiles \
        WHERE resourceinstanceid = '{1}' \
        AND nodegroupid = '{2}'".format(testdb_bc_fields["Geometric Place Expression"], uuid, testdb_bc_fields["geometry"])
        print(sql)
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(sql)
        mygeom = dict_cur.fetchone()[0]
        return(mygeom)

def get_related_resources_from_uuid(uuid):
    """
    Retrieve the related resources of an Heritage Place from its UUID

    Relationships are directed. The function looks in 'from', and in 'to' columns
    to be sure to catch the releated resources. The list is then clean (remove duplicates,
    remove the Heritage Place itself)

    :param uuid: The UUID
    :type uuid: UUID
    :return: TODO
    :Example:
    >>> my_uuid = get_uuid_from_eaid('EAMENA-0181523')
    >>> my_related_resources = get_related_resources_from_uuid(my_uuid)
    ['bcff0719-5d68-42ce-ac12-2cfc33858b06', '19e69b2c-eeee-4b1d-a8c8-7fa13a034820', '2a774cbd-d13f-41ce-8af1-292344bd4dff']
    """
    sql="SELECT resourceinstanceidfrom FROM public.resource_x_resource \
    WHERE resourceinstanceidfrom = '{0}'".format(uuid)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(sql)
    myrelatedresources_from = dict_cur.fetchall()
    sql="SELECT resourceinstanceidto FROM public.resource_x_resource \
    WHERE resourceinstanceidfrom = '{0}'".format(uuid)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(sql)
    myrelatedresources_to = dict_cur.fetchall()
    myrelatedresources_from_and_to = myrelatedresources_from + myrelatedresources_to
    myrelatedresources_flat = [x for xs in myrelatedresources_from_and_to for x in xs]
    myrelatedresources_no_duplicates = list(set(myrelatedresources_flat))
    myrelatedresources_not_the_uuid = [x for x in myrelatedresources_no_duplicates if not x == uuid]
    myrelatedresources = myrelatedresources_not_the_uuid
    return(myrelatedresources)

my_uuid = get_uuid_from_eaid('EAMENA-0181523')
# my_geom = get_geom_from_uuid(my_uuid)
# my_related_resources = get_related_resources_from_uuid(my_uuid)

my_geom = get_geom_from_uuid('2a774cbd-d13f-41ce-8af1-292344bd4dff', 'bc')
print(my_geom)

# print(my_uuid)
# print(my_geom)
# print(my_related_resources)

# - - - - - - - - - - - - -
cur.close()