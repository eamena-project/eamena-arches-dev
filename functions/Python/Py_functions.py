from _conn import conn
from Py_sources import testdb_hp_fields, testdb_bc_fields
import os
import urllib.request, geojson, subprocess
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

def get_geom_from_uuid(uuid, restyp):
    """
    Retrieve the geometry of an Heritage Place from its UUID

    Select the GeoJSON object in the tiledata field. Read equivalences between field names and UUID from the Python source file
    :param uuid: The UUID
    :param restyp: The type of resource, 'hp' for 'Heritage Place', or 'bc' for 'Built Component'
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
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(sql)
        mygeom = dict_cur.fetchone()[0]
        return(mygeom)
    if(restyp == 'bc'):
        sql="SELECT tiledata->>'{0}' as my_geojson FROM tiles \
        WHERE resourceinstanceid = '{1}' \
        AND nodegroupid = '{2}'".format(testdb_bc_fields["Geometric Place Expression"], uuid, testdb_bc_fields["geometry"])
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(sql)
        mygeom = dict_cur.fetchone()[0]
        return(mygeom)

def get_related_resources_from_uuid(uuid):
    """
    Retrieve the UUID of related resources of an Heritage Place

    Relationships are directed. The function looks in 'from', and in 'to' columns
    to be sure to catch the releated resources. The list is then clean (remove duplicates,
    remove the Heritage Place itself)

    :param uuid: The UUID of the Heritage Place
    :type uuid: UUID
    :return: A list of the UUID of the related resources
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

def export_geom_from_urlgeojson(url_geojson = 'http://34.244.135.144/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=3&resource-type-filter=%5B%7B%22graphid%22%3A%226c4f0703-c381-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Built%20Component%22%2C%22inverted%22%3Afalse%7D%5D',
out_geom_format = "geojson", out_geom_name = "out_geom", out_geom_dir = os.getcwd() + "\\data\\test\\"):
    """
        Create a geom (SHP or GeoJSON) from a 'url geojson' obtained from a EAMENA-like DB

        :param url_geojson: The 'url geojson' from EAMENA-like
        :param out_geom_format: The format of the geometry to create, 'geojson' or 'shp'
        :param out_geom_name: The name of the geometry to create
        :param out_geom_dir: The name of the output directory
        :type url_geojson: string, URL
        :type out_geom_format: string
        :type out_geom_name: string
        :type out_geom_dir: string
        :return: a new file (SHP or GeoJSON)
        :Example:
        >>> export_geom_from_urlgeojson('http://34.244.135.144/api/search/export_results?...')
        # export 'out_geom.geojson'
    """

    # url_geojson= 'http://34.244.135.144/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&total=3&resource-type-filter=%5B%7B%22graphid%22%3A%226c4f0703-c381-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Built%20Component%22%2C%22inverted%22%3Afalse%7D%5D'
    response = urllib.request.urlopen(url_geojson)
    data = geojson.loads(response.read())

    out_geom = out_geom_dir + out_geom_name + "." + out_geom_format

    with open(out_geom, 'w') as f:
        geojson.dump(data, f)
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', out_geom]
    subprocess.Popen(args)
    print("File "+ out_geom_name + "." + out_geom_format + " created!")

