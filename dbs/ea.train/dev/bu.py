from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpRequest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from arches.app.models.models import GraphModel, Node, ResourceInstance, TileModel
from arches.app.models.concept import Concept, get_preflabel_from_valueid, get_valueids_from_concept_label
from arches.app.views import search
from django.core.management.base import BaseCommand
from django.contrib.gis.geos.error import GEOSException
from eamena.bulk_uploader import HeritagePlaceBulkUploadSheet, GridSquareBulkUploadSheet
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError, NotFoundError
from geomet import wkt
import json, os, sys, logging, re, uuid, hashlib, datetime, warnings

logger = logging.getLogger(__name__)

def parse_date(datestring):

	# This function is necessary because the behaviour of dateutil.parse is unpredictable.

#	if not(isinstance(datestring, (str))):
#		return None
	datestring = datestring.split(" ")[0].replace("/", "-")
	parsed = datestring.split("-")
	if len(parsed) != 3:
		return None
	try:
		v1 = int(parsed[0])
		v2 = int(parsed[1])
		v3 = int(parsed[2])
	except:
		return None
	if ((v2 < 1) | (v2 > 12)):
		return None
	if v1 > 100: # y-m-d
		try:
			return datetime.datetime(v1, v2, v3)
		except:
			return None
	if v3 > 100: # d-m-y
		try:
			return datetime.datetime(v3, v2, v1)
		except:
			return None
	return None

class Command(BaseCommand):
	"""
	Commands for managing the import of EAMENA BUS files

	"""

	def __init__(self):

		self.__idcache = {}
		self.__graphcache = {}

	def __create_res(self, graphid, legacy_id=''):

		id = legacy_id
		if id == '':
			id = str(uuid.uuid4())
		item = {}
		item['resourceinstance'] = {
			"resourceinstanceid" : id, "graph_id" : str(graphid), "legacyid" : id}
		item['tiles'] = []
		return item

	def __create_tile(self, resid, nodegroupid, parent=None):

		ret = {}
		required_datatypes = ['date', 'concept']
		ret['parenttile_id'] = None
		ret['provisionaledits'] = None
		ret['sortorder'] = 0
		ret['tileid'] = str(uuid.uuid4())
		ret['nodegroup_id'] = nodegroupid
		ret['resourceinstance_id'] = resid
		ret['data'] = {}
		for node in Node.objects.filter(nodegroup_id=nodegroupid):
			if node.datatype in required_datatypes:
				node_uuid = str(node.nodeid)
				ret['data'][node_uuid] = None
		if parent:
			ret['parenttile_id'] = parent
		return ret

	def __error(self, ref, text, info=''):

		self.errors.append([ref, text, info])

	def __warn(self, ref, text, info=''):

		self.warnings.append([ref, text, info])

	def __get_prerequisites(self, data, options):

		nodes = {}
		new_resources = {}
		for node in Node.objects.filter(graph__graphid=options['graph'], datatype='resource-instance').all():
			value = {"nodeid": str(node.nodeid), "name": node.name, "datatype": str(node.datatype), "key": (re.sub(r'[^A-Z_]+', '_', node.name.replace(' ', '_').upper().strip('_'))), "config": node.config}
			nodes[value['nodeid']] = value

		for resource in data:
			if 'tiles' in resource:
				tiles = resource['tiles']
				resource['tiles'] = []
				for tile in tiles:
					if 'data' in tile:
						for ko in tile['data']:
							key = str(ko)
							if key in nodes:
								target_graphs = nodes[key]['config']['graphs']
								id = ''
								for target_graph in target_graphs:
									ri = self.__resourceinstance_from_eamenaid(tile['data'][key], target_graph['graphid'])
									if not(ri is None):
										id = str(ri.resourceinstanceid)
								if len(id) == 0:
									hash = hashlib.md5((str(tile['data'][key]) + '_' + str(target_graph['graphid'])).encode('utf8')).hexdigest()
									new_resources[hash] = {"text": tile['data'][key], "graph": target_graph['graphid']}
					resource['tiles'].append(tile)

		ret = []
		for ko in new_resources.keys():

			key = str(ko)
			item = new_resources[key]
			res = self.__create_res(item['graph'])

			if item['graph'] == '77d18973-7428-11ea-b4d0-02e7594ce0a0':
				tile = self.__create_tile(res['resourceinstance']['resourceinstanceid'], 'b3628db0-742d-11ea-b4d0-02e7594ce0a0')
				tile['data']['b3628db0-742d-11ea-b4d0-02e7594ce0a0'] = item['text']
				res['tiles'].append(tile)

				ret.append(res)

			if item['graph'] == 'e98e1cee-c38b-11ea-9026-02e7594ce0a0':
				tile = self.__create_tile(res['resourceinstance']['resourceinstanceid'], 'e98e1cfe-c38b-11ea-9026-02e7594ce0a0')
				tile['data']['e98e1cfe-c38b-11ea-9026-02e7594ce0a0'] = item['text']
				tile['data']['e98e1d0b-c38b-11ea-9026-02e7594ce0a0'] = None
				tile['data']['e98e1d0c-c38b-11ea-9026-02e7594ce0a0'] = None
				tile['data']['e98e1d0e-c38b-11ea-9026-02e7594ce0a0'] = None
				tile['data']['e98e1d08-c38b-11ea-9026-02e7594ce0a0'] = None
				res['tiles'].append(tile)

				ret.append(res)

		return ret

	def __map_resources(self, data, options, uid=''):

		passed_uid = uid

		if isinstance(data, (dict)):

			if '_' in data:
				passed_uid = data['_']
				del(data['_'])

		nodes = {}
		ret = []
		for node in Node.objects.filter(graph__graphid=options['graph']).all():
			value = {"nodeid": str(node.nodeid), "name": node.name, "datatype": str(node.datatype), "key": (re.sub(r'[^A-Z_]+', '_', node.name.replace(' ', '_').upper().strip('_'))), "config": node.config}
			nodes[value['nodeid']] = value

		for resource in data:
			if 'resourceinstance' in resource:
				if '_' in resource['resourceinstance']:
					passed_uid = resource['resourceinstance']['_']
					del(resource['resourceinstance']['_'])
			if 'tiles' in resource:
				tiles = resource['tiles']
				resource['tiles'] = []
				for tile in tiles:
					if 'data' in tile:
						for ko in tile['data']:
							key = str(ko)
							if key in nodes:

								if tile['data'][key] is None:
									continue

								if nodes[key]['datatype'] == 'date':
									date_object = parse_date(tile['data'][key])
									if date_object is None:
										self.__error(passed_uid, 'Cannot parse date string: "' + str(tile['data'][key]) + '"')
									else:
										new_date_string = date_object.strftime('%Y-%m-%d')
										tile['data'][key] = new_date_string

								if nodes[key]['datatype'] == 'concept-list':
									if not(isinstance(tile['data'][key], (dict, list))):
										tile['data'][key] = [tile['data'][key]]

								if nodes[key]['datatype'] == 'geojson-feature-collection':
									if isinstance(tile['data'][key], (str)):
										geojson_data = self.__geojson_from_wkt(tile['data'][key])
										if isinstance(geojson_data, (dict)):
											if 'features' in geojson_data:
												for feature in geojson_data['features']:
													if 'geometry' in feature:
														try:
															geom_collection = GEOSGeometry(json.dumps(feature['geometry']))
														except GEOSException:
															self.__error(passed_uid, "Invalid geometry.", "The geometry is syntactically correct, but the shape is not supported by Arches. Please simplify and try again.")
													else:
														self.__error(passed_uid, "Invalid geometry.", "FeatureCollection is missing a geometry.")

											tile['data'][key] = geojson_data
											tile['data'][key]['features'][0]['properties']['nodeId'] = str(key)
										else:
											self.__error(passed_uid, "Invalid geometry.", "Please check your geometry data is in the WKT format, all co-ordinates are two-dimensional, and no co-ordinates are duplicated.")

								if nodes[key]['datatype'] == 'resource-instance':
									target_graphs = nodes[key]['config']['graphs']
									id = ''
									for target_graph in target_graphs:
										ri = self.__resourceinstance_from_eamenaid(tile['data'][key], target_graph['graphid'])
										if not(ri is None):
											id = str(ri.resourceinstanceid)
											tile['data'][key] = [{
												"ontologyProperty": target_graph['ontologyProperty'],
												"inverseOntologyProperty": target_graph['inverseOntologyProperty'],
												"resourceId": id,
												"resourceXresourceId": str(uuid.uuid4())
											}]
									if len(id) == 0:
										help_text = []
										for target_graph in target_graphs:
											help_text.append(self.__modelname_from_uuid(target_graph['graphid']))
										self.__error(passed_uid, "Cannot resolve linked resource: '" + str(tile['data'][key]) + "' is not in the database.", "Expecting: " + (', '.join(help_text)))

								if nodes[key]['datatype'] == 'resource-instance-list':
									target_graphs = nodes[key]['config']['graphs']
									id = ''
									for target_graph in target_graphs:
										ri = self.__resourceinstance_from_eamenaid(tile['data'][key], target_graph['graphid'])
										if not(ri is None):
											id = str(ri.resourceinstanceid)
											tile['data'][key] = [{
												"ontologyProperty": target_graph['ontologyProperty'],
												"inverseOntologyProperty": target_graph['inverseOntologyProperty'],
												"resourceId": id,
												"resourceXresourceId": str(uuid.uuid4())
											}]
									if len(id) == 0:
										help_text = []
										for target_graph in target_graphs:
											help_text.append(self.__modelname_from_uuid(target_graph['graphid']))
										self.__error(passed_uid, "Cannot resolve linked resource: '" + str(tile['data'][key]) + "' is not in the database.", "Expecting: " + (', '.join(help_text)))
					resource['tiles'].append(tile)
			ret.append(resource)

		return ret

	def add_arguments(self, parser):

		parser.add_argument(
			"-o",
			"--operation",
			action="store",
			dest="operation",
			default="",
			choices=[
				"list_nodes",
				"convert",
				"translate",
				"validate",
				"unflatten",
				"prerequisites",
				"annotate",
				"summary",
				"undo"
			],
			help="Operation Type; 'list_nodes'=Lists all the valid nodes in a graph.'convert'=Converts an XLSX bulk upload sheet into Arches JSON. 'validate'=Inspects an XLSX bulk upload sheet and lists errors. 'unflatten'=Dumps the intermediate data format, in the correct structure but without validating concepts.'prerequisites'=Returns an Arches JSON file containing all the prerequisite objects (grid ids, etc) that do not already exist in the database.'annotate'=Takes an Arches import file and outputs the same file but with extra properties (which are ignored by Arches) describing the field names and concepts, making the file much easier for a human to read.'summary'=Returns a list of UUIDs of imported items, and their EAMENA IDs.'undo'=Takes a generated Arches JSON business data file as an input, and deletes all UUIDs referenced within, effectively undoing a bulk upload."
		)

		parser.add_argument(
			"-w",
			"--warnings",
			action="store",
			dest="warn_mode",
			default="warn",
			choices=["warn", "ignore", "strict"],
			help="Warn mode; 'warn'=Write warnings to STDERR, but ultimately ignore them. 'ignore'=Silently ignore warnings altogether. 'strict'=Treat warnings as errors, and stop if any are encountered."
		)

		parser.add_argument(
			"-a",
			"--append",
			action="store",
			dest="append_mode",
			default="new",
			choices=["new", "append"],
			help="Append mode; 'new'=Don't append, generate new UUIDs for items 'append'=Append data to existing records, using UNIQUEID as an identifier."
		)

		parser.add_argument(
			"-s", "--source", action="store", dest="source", default="", help="BUS file for processing.",
		)

		parser.add_argument(
			"-d", "--dest_dir", action="store", dest="dest_dir", default="", help="Directory where you want to save exported files. Omitting this argument dumps to STDOUT."
		)

		parser.add_argument(
			"-g",
			"--graph",
			action="store",
			dest="graph",
			default=False,
			help="The graphid of the resources you would like to import/convert.",
		)

	def __modelname_from_uuid(self, graphid):

		if len(self.__graphcache) == 0:
			for g in GraphModel.objects.all():
				id = str(g.graphid)
				name = str(g.name)
				self.__graphcache[id] = name
		if graphid in self.__graphcache:
			return self.__graphcache[graphid]
		return None

	def __eamenaid_from_resourceinstance(self, resourceinstanceid):

		eamena_tile_uuid = '34cfe992-c2c0-11ea-9026-02e7594ce0a0'

		try:
			tile = TileModel.objects.get(nodegroup__nodegroupid=eamena_tile_uuid, resourceinstance_id=str(resourceinstanceid))
		except:
			return ''
		data = tile.data
		if eamena_tile_uuid in data:
			return data[eamena_tile_uuid]
		return ''

	def __resourceinstance_from_eamenaid(self, eamenaid, graphid, quick=False):

		key = str(graphid) + '_' + str(eamenaid)
		if key in self.__idcache:
			return self.__idcache[key]
		ret = self.__resourceinstance_from_eamenaid_es(eamenaid, graphid)
		if not(ret is None):
			self.__idcache[key] = ret
			return ret
		if quick:
			return None # Looking this up in the ORM is really slow, so we have the option to just end the search here.
		ret = self.__resourceinstance_from_eamenaid_orm(eamenaid, graphid)
		if not(ret is None):
			self.__idcache[key] = ret
			for tile in TileModel.objects.filter(resourceinstance=ret):
				for ko in tile.data.keys():
					k = str(ko)
					if isinstance(tile.data[k], (str)):
						v = str(tile.data[k])
						if v == eamenaid:
							return ret
		self.__idcache[key] = None
		return None

	def __resourceinstance_from_eamenaid_orm(self, eamenaid, graphid):

		try:
			rm = GraphModel.objects.get(graphid=graphid)
		except:
			return None
		try:
			ret = ResourceInstance.objects.get(graph_id=rm.graphid, tilemodel__data__icontains=eamenaid)
		except ResourceInstance.DoesNotExist:
			ret = None
		except ResourceInstance.MultipleObjectsReturned:
			ret = ResourceInstance.objects.filter(graph_id=rm.graphid, tilemodel__data__icontains=eamenaid).first()
		return ret

	def __resourceinstance_from_eamenaid_es(self, eamenaid, graphid):

		try:
			rm = GraphModel.objects.get(graphid=graphid)
		except:
			return None

		request = HttpRequest()
		request.user = User.objects.get(username='admin')
		request.path = '/'
		request.GET = {"paging-filter":"1","tiles":"true","format":"tilecsv","precision":"6","total":"1","term-filter":"[{\"inverted\":false,\"type\":\"string\",\"context\":\"\",\"context_label\":\"\",\"id\":\"" + eamenaid + "\",\"text\":\"" + eamenaid + "\",\"value\":\"" + eamenaid + "\"}]","resource-type-filter":"[{\"graphid\":\"" + str(rm.graphid) + "\",\"name\":\"" + str(rm.name) + "\",\"inverted\":false}]"}
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			response = search.search_results(request)
		results = json.loads(response.content)
		ret = None

		for hit in results['results']['hits']['hits']:
			hitid = str(hit['_id'])
			hiteamenaid = str(hit['_source']['displayname'])
			if hiteamenaid == eamenaid:
				try:
					ret = ResourceInstance.objects.get(resourceinstanceid=hitid, graph_id=rm.graphid)
				except:
					ret = None
			if not(ret is None):
				return ret

		return ret


	def __make_temp_index(self, es, index):
		ret = str(uuid.uuid4())
		try:
			es.get(index=index, id=ret)
			ret = self.__make_temp_uuid() # Keep iterating until we get one that errors
		except NotFoundError:
			pass
		return ret

	def __test_geojson_es(self, gj):
		if not(self.__test_geojson_recurse(gj)):
			return False
		es = Elasticsearch()
		id = self.__make_temp_index(es, 'eamena_resources')
		doc = {'resourceinstanceid': id, 'geometries': [{'geom': gj}]}
		try:
			es.index(index='eamena_resources', doc_type='_doc', body=doc, id=id)
		except RequestError:
			return False
		es.delete(index='eamena_resources', id=id)
		return True

	def __test_geojson_recurse(self, gj):
		if isinstance(gj, (dict)):
			ret = True
			for keyo in gj.keys():
				key = str(keyo)
				ret = ret & (self.__test_geojson_recurse(gj[key]))
			return ret
		elif isinstance(gj, (list)):
			floats = 0
			for item in gj:
				if isinstance(item, (float)):
					floats = floats + 1
			if len(gj) == floats:
				if floats == 2:
					if gj[1] > 180.0:
						return False
					if gj[1] < -90.0:
						return False
					if gj[0] > 360.0:
						return False
					if gj[0] < -180.0:
						return False
					return True
				else:
					return False
			last_coords = ''
			for item in gj:
				if not(isinstance(item, (list))):
					continue
				if len(item) != 2:
					continue
				itemser = json.dumps(item)
				if itemser == last_coords:
					return False
				last_coords = itemser
			ret = True
			for item in gj:
				ret = ret & (self.__test_geojson_recurse(item))
			return ret
		else:
			return True

	def __geojson_from_wkt(self, text):

		try:
			geom = wkt.loads(text)
		except:
			geom = []
		if len(geom) == 0:
			try:
				geom = wkt.loads("POINT(" + text + ")")
			except:
				geom = []
		if len(geom) == 0:
			return text
		else:
			if self.__test_geojson_recurse(geom):
				geom = {"type": "FeatureCollection", "features": [{ "type": "Feature", "properties": {"nodeId": None}, "geometry": geom }]}
				if self.__test_geojson_es(geom):
					return geom
				else:
					return text
			else:
				return text

	def __replace_node_uuids(self, data, nodes, uid=''):

		passed_uid = uid

		if isinstance(data, (dict)):

			if '_' in data:
				passed_uid = data['_']

			ret = {}
			for keyobj in data.keys():
				key = str(keyobj)
				node_name = key
				value = data[key]
				values = []
				if keyobj in nodes:
					key = str(keyobj)
					if 'name' in nodes[key]:
						node_name = nodes[key]['name']
					if 'values' in nodes[key]:
						values = nodes[key]['values']
					key = nodes[key]['nodeid']
				if len(values) == 0:
					ret[key] = self.__replace_node_uuids(value, nodes, passed_uid)
				else:
					if isinstance(value, (list)):
						for i in range(0, len(value)):
							if isinstance(value[i], (str)):
								replaced = False
								for potential_value in values:
									if potential_value['label'].casefold() == value[i].casefold():
										if potential_value['label'] != value[i]:
											self.__warn(passed_uid, "Invalid concept value '" + str(value[i]) + "'", "Did you mean '" + str(potential_value['label']) + "'?")
										value[i] = potential_value['valueid']
										replaced = True
								if not(replaced):
									error_text = 'Invalid concept value "' + str(value) + '" for "' + str(node_name) + '".'
									error_help = ''
									if len(values) > 0:
										values_string = []
										for value_string in values:
											values_string.append("'" + value_string['label'] + "'")
										error_help = error_help + 'Valid values: ' + (', '.join(values_string)) + '.'
										# error_help = error_help + '\n' + json.dumps(data)
									self.__error(passed_uid, error_text, error_help)
							if isinstance(value[i], (dict)):
								value[i] = self.__replace_node_uuids(value[i], nodes, passed_uid)
					else:
						replaced = False
						oldvalue = value
						for potential_value in values:
							if isinstance(value, (str)):
								if potential_value['label'].casefold().strip() == value.casefold().strip():
									if potential_value['label'] != value:
										self.__warn(passed_uid, "Invalid concept value '" + str(value) + "'", "Did you mean '" + str(potential_value['label']) + "'?")
									value = potential_value['valueid']
									replaced = True
						if oldvalue == value:
							if isinstance(value, (str)):
								potential_values = get_valueids_from_concept_label(value)
								if len(potential_values) == 1:
									value = potential_values[0]['id']
									replaced = True
						if not(replaced):
							error_text = 'Invalid concept value "' + str(value) + '" for "' + str(node_name) + '".'
							error_help = ''
							if len(values) > 0:
								values_string = []
								for value_string in values:
									values_string.append("'" + value_string['label'] + "'")
								error_help = error_help + 'Valid values: ' + (', '.join(values_string)) + '.'
								#error_help = error_help + '\n' + json.dumps(data)
							self.__error(passed_uid, error_text, error_help)
					ret[key] = value
			return ret

		if isinstance(data, (list)):

			ret = []
			for item in data:
				ret.append(self.__replace_node_uuids(item, nodes, passed_uid))
			return ret

		return data

	def __recursive_data_conversion(self, data, type, parent, resid, rm):

		ret = []

		if isinstance(data, (str)):
			tile = self.__create_tile(resid, type, parent)
			tile['data'][type] = data
			ret.append(tile)

		if isinstance(data, (list)):
			for item in data:
				for tile in self.__recursive_data_conversion(item, type, parent, resid, rm):
					ret.append(tile)

		if isinstance(data, (dict)):
			tile = self.__create_tile(resid, type, parent)
			for key in data.keys():
				k = str(key)
				if not(isinstance(data[k], (dict, list))):
					tile['data'][k] = data[k]
			tile_parent = tile['tileid']
			ret.append(tile)
			for key in data.keys():
				k = str(key)
				if isinstance(data[k], (dict, list)):
					for tile in self.__recursive_data_conversion(data[k], k, tile_parent, resid, rm):
						ret.append(tile)

		return ret

	def __convert_translated_data(self, data, options):

		append_mode = options['append_mode']
		try:
			rm = GraphModel.objects.get(graphid=options['graph'])
		except GraphModel.DoesNotExist:
			rm = None

		ret = []
		for item in data:

			legacyid = ''
			if append_mode == 'append':
				if '_' in item:
					uid = item['_']
					resid = self.__resourceinstance_from_eamenaid(uid, rm.graphid, quick=True)
					if resid is None:
						self.__error(uid, 'Cannot resolve existing EAMENA ID', 'In append mode, the UNIQUEID column must contain a valid EAMENA ID, so the system knows which resource should be appended.')
						continue
					legacyid = str(resid.resourceinstanceid)
				else:
					self.__error('', 'Missing UNIQUEID', '')
					continue

			res = self.__create_res(rm.graphid, legacyid)
			resid = res['resourceinstance']['resourceinstanceid']
			if '_' in item:
				res['resourceinstance']['_'] = item['_']
			for nodegroupidkey in item.keys():
				nodegroupid = str(nodegroupidkey)
				if isinstance(item[nodegroupid], (list)):
					for subitem in item[nodegroupid]:
						for tile in self.__recursive_data_conversion(subitem, str(nodegroupid), None, resid, rm):
							res['tiles'].append(tile)
				if isinstance(item[nodegroupid], (dict)):
					for subtile in self.__recursive_data_conversion(item[nodegroupid], str(nodegroupid), None, resid, rm):
						res['tiles'].append(subtile)

			ret.append(res)

		return ret

	def __convert_translated_grid_square(self, data, options):

		try:
			rm = GraphModel.objects.get(graphid=options['graph'])
		except GraphModel.DoesNotExist:
			rm = None

		ret = []
		for item in data:

			grid_id = ''
			grid_uuid = ''
			if 'GRID_ID' in item[0]:
				grid_id = item[0]['GRID_ID']
			if 'GRID ID' in item[0]:
				grid_id = item[0]['GRID ID']
			if 'Grid ID' in item[0]:
				grid_id = item[0]['Grid ID']
			if grid_id == '':
				continue
			ri = self.__resourceinstance_from_eamenaid(grid_id, str(rm.graphid))
			if not(ri is None):
				grid_uuid = str(ri.resourceinstanceid)

			if grid_uuid == '':
				res = self.__create_res(rm.graphid)
				resid = res['resourceinstance']['resourceinstanceid']
				for nodegroupidkey in item[0].keys():
					nodegroupid = str(nodegroupidkey)
					oldnodegroupid = nodegroupid
					if nodegroupid == 'Grid ID':
						nodegroupid = 'b3628db0-742d-11ea-b4d0-02e7594ce0a0' # EAMENA Grid ID
					tile = self.__create_tile(resid, nodegroupid)
					tiledata = item[0][oldnodegroupid]
					if tiledata.startswith('POLYGON'):
						tiledata = self.__geojson_from_wkt(tiledata)
					tile['data'][nodegroupid] = tiledata
					res['tiles'].append(tile)
			else:
				res = self.__create_res(rm.graphid, grid_uuid)
				resid = res['resourceinstance']['resourceinstanceid']
				for nodegroupidkey in item[0].keys():
					nodegroupid = str(nodegroupidkey)
					if nodegroupid == 'Grid ID':
						continue # Don't add the grid ID if it already exists
					tile = self.__create_tile(resid, nodegroupid)
					tiledata = item[0][nodegroupid]
					if tiledata.startswith('POLYGON'):
						tiledata = self.__geojson_from_wkt(tiledata)
					tile['data'][nodegroupid] = tiledata
					res['tiles'].append(tile)

			ret.append(res)

		return ret

	def __translate_grid_square(self, options):

		nodes = {}
		for node in self.__list_nodes(options):
			key = node['key']

			nodes[key] = node

		data = self.__replace_node_uuids(self.__unflatten(options), nodes)

		return data

	def __translate_heritage_place(self, options):

		nodes = {}
		disturbance_date_ids = ['34cfea92-c2c0-11ea-9026-02e7594ce0a0', '34cfea7f-c2c0-11ea-9026-02e7594ce0a0', '34cfea65-c2c0-11ea-9026-02e7594ce0a0', '34cfea7a-c2c0-11ea-9026-02e7594ce0a0']
		for node in self.__list_nodes(options):
			key = node['key']

			# This next block of code is for correcting spelling mis-matches and other differences between the resource model and the BUS

			# There are two sections of the data structure with identical titles, but only one seems to be used. So we ignore the other one.
			if ((key.startswith('DISTURBANCE_DATE_')) & (not(node['nodeid'] in disturbance_date_ids))):
				continue

			# This next bit looks for common mis-spellings in certain concept fields.
			if ((key == 'COUNTRY_TYPE') & ('values' in node)):
				for potential_value in node['values']:
					if potential_value['label'] == 'Iran (Islamic Republic of)':
						node['values'].append({"label": "Iran", "conceptid": potential_value['conceptid'], "valueid": potential_value['valueid']})
			if ((key == 'ASSESSMENT_ACTIVITY_TYPE') & ('values' in node)):
				for potential_value in node['values']:
					if potential_value['label'] == 'Desk-based Assessment':
						node['values'].append({"label": "Desk Based Assessment", "conceptid": potential_value['conceptid'], "valueid": potential_value['valueid']})
			if ((key == 'EFFECT_TYPE') & ('values' in node)):
				for potential_value in node['values']:
					if potential_value['label'] == 'Erosion/Deterioration':
						node['values'].append({"label": "Erosion/Deterioration (micro-bio)", "conceptid": potential_value['conceptid'], "valueid": potential_value['valueid']})
			if ((key == 'TIDAL_RANGE') & ('values' in node)):
				for potential_value in node['values']:
					if potential_value['label'] == 'Mesotidal (2-4m)':
						node['values'].append({"label": "Mesotidal (2-4 m)", "conceptid": potential_value['conceptid'], "valueid": potential_value['valueid']})
			if ((key == 'FETCH_TYPE') & ('values' in node)):
				for potential_value in node['values']:
					if potential_value['label'] == 'Moderately exposed (10-100km)':
						node['values'].append({"label": "Moderately exposed (10-100 km)", "conceptid": potential_value['conceptid'], "valueid": potential_value['valueid']})

			# This next section looks for common mis-spellings in column headers.

			nodes[key] = node

			if key == 'GEOMETRY':
				nodes['GEOMETRIES'] = node
			if key == 'TIDAL_RANGE':
				nodes['TIDAL_ENERGY'] = node
			if key == 'THREAT_CAUSE_TYPE':
				nodes['THREAT_TYPE'] = node
			if key == 'RESTRICTED_ACCESS_RECORD_DESIGNATION':
				nodes['ACCESS'] = node
			if key == 'LOCATION_CERTAINTY':
				nodes['SITE_LOCATION_CERTAINTY'] = node
			if key == 'OVERALL_CONDITION_STATE_TYPE':
				nodes['OVERALL_CONDITION_STATE'] = node
			if key == 'OVERALL_SITE_SHAPE_TYPE':
				nodes['SITE_OVERALL_SHAPE_TYPE'] = node
			if key == 'DESCRIPTION_ASSIGNMENT':
				nodes['RESOURCE_DESCRIPTION'] = node
			if key == 'HERITAGE_PLACE_FUNCTION_BELIEF':
				nodes['HERITAGE_RESOURCE_CLASSIFICATION'] = node
			if key == 'CULTURAL_SUB_PERIOD_CERTAINTY':
				nodes['CULTURAL_SUBPERIOD_CERTAINTY'] = node
			if key == 'CULTURAL_SUB_PERIOD_TYPE':
				nodes['CULTURAL_SUBPERIOD_TYPE'] = node
			if key == 'SITE_FEATURE_INTERPRETATION_NUMBER_TYPE':
				nodes['SITE_FEATURE_INTERPRETATION_NUMBER'] = node
			if key == 'GOOGLE_EARTH_ASSESSMENT':
				nodes['GE_ASSESSMENT_YES_NO_'] = node
			if key == 'ARCHAEOLOGICAL_FROM_DATE':
				nodes['ARCHAEOLOGICAL_DATE_FROM__CAL_'] = node
			if key == 'ARCHAEOLOGICAL_TO_DATE':
				nodes['ARCHAEOLOGICAL_DATE_TO__CAL_'] = node
			if key == 'ADMINISTRATIVE_DIVISION':
				nodes['ADMINISTRATIVE_SUBDIVISION'] = node
			if key == 'ADMINISTRATIVE_DIVISION_TYPE':
				nodes['ADMINISTRATIVE_SUBDIVISION_TYPE'] = node
			if key == 'MINIMUM_DEPTH_MAX_ELEVATION':
				nodes['MINIMUM_DEPTH_MAX_ELEVATION_M_'] = node
			if key == 'MAXIMUM_DEPTH_MIN_ELEVATION':
				nodes['MAXIMUM_DEPTH_MIN_ELEVATION_M_'] = node
			if key == 'SITE_FEATURE_FORM_TYPE_BELIEF':
				nodes['SITE_FEATURE_FORM'] = node
			if key == 'SITE_FEATURE_INTERPRETATION_BELIEF':
				nodes['SITE_FEATURE_INTERPRETATION'] = node
			if key == 'CULTURAL_PERIOD_BELIEF':
				nodes['PERIODIZATION'] = node
			if key == 'CULTURAL_SUB_PERIOD_BELIEF':
				nodes['CULTURAL_SUBPERIOD'] = node
			if key == 'SITE_FEATURE_ASSIGNMENT':
				nodes['SITE_FEATURES'] = node
			if key == 'ARCHAEOLOGICAL_TIMESPACE':
				nodes['ABSOLUTE_CHRONOLOGY'] = node
			if key == 'DAMAGE_OBSERVATION':
				nodes['EFFECTS'] = node
			if key == 'DISTURBANCE_EVENT':
				nodes['DISTURBANCES'] = node
			if key == 'THREAT_INFERENCE_MAKING':
				nodes['THREATS'] = node

			if key == 'INFORMATION_RESOURCE':
				nodes['INFORMATION_RESOURCE_USED'] = node
			if key == 'BUILT_COMPONENT':
				nodes['BUILT_COMPONENT_RELATED_RESOURCE'] = node
			if key == 'HERITAGE_PLACE_RESOURCE_INSTANCE':
				nodes['HP_RELATED_RESOURCE'] = node
			if key == 'RELATED_GEOARCHAEOLOGY_PALAEOLANDSCAPE':
				nodes['RELATED_GEOARCH_PALAEO'] = node
			if key == 'DETAILED_CONDITION_ASSESSMENTS':
				nodes['RELATED_DETAILED_CONDITION_RESOURCE'] = node

			if key.endswith('___ACTOR'):
				nodes[key.replace('___ACTOR', '')] = node

		data = self.__replace_node_uuids(self.__unflatten(options), nodes)

		return data

	def __list_nodes(self, options):

		data = []

		try:
			rm = GraphModel.objects.get(graphid=options['graph'])
		except GraphModel.DoesNotExist:
			rm = None

		if rm is None:
			self.__error("", "Invalid or missing graph UUID. Use --graph")
		else:
			for node in Node.objects.filter(graph=rm):
				value = {"nodeid": str(node.nodeid), "name": node.name, "datatype": str(node.datatype), "key": (re.sub(r'[^A-Z_]+', '_', node.name.replace(' ', '_').upper().strip('_')))}
				if ((value['datatype'] == 'concept') or (value['datatype'] == 'concept-list')):
					if 'rdmCollection' in node.config:
						conceptid = node.config['rdmCollection']
						if not(conceptid is None):
							values = Concept().get_e55_domain(conceptid)
							value['values'] = []
							for item in values:
								valueobj = get_preflabel_from_valueid(item['id'], 'en')
								valueid = valueobj['id']
								label = get_preflabel_from_valueid(valueid, 'en')
								value['values'].append({'valueid': valueid, 'conceptid': item['conceptid'], 'label': label['value']})
								for child in Concept().get_child_concepts(item['conceptid']):
									value['values'].append({'valueid': child[2], 'conceptid': child[0], 'label': child[1]})
				data.append(value)

		return data

	def __unflatten(self, options):

		data = []

		if not(options['source']):

			self.__error("", "Need an input file; use --source")

		elif os.path.exists(options['source']):

			try:
				rm = GraphModel.objects.get(graphid=options['graph'])
			except GraphModel.DoesNotExist:
				rm = None

			if rm is None:
				self.__error("", "Invalid or missing graph UUID. Use --graph")
			elif rm.name == 'Heritage Place':
				expected_nodes = ['UNIQUEID', 'ASSESSMENT_INVESTIGATOR___ACTOR', 'INVESTIGATOR_ROLE_TYPE', 'ASSESSMENT_ACTIVITY_TYPE', 'ASSESSMENT_ACTIVITY_DATE', 'GE_ASSESSMENT_YES_NO_', 'GE_IMAGERY_ACQUISITION_DATE', 'INFORMATION_RESOURCE_USED', 'INFORMATION_RESOURCE_ACQUISITION_DATE', 'RESOURCE_NAME', 'NAME_TYPE', 'HERITAGE_PLACE_TYPE', 'GENERAL_DESCRIPTION_TYPE', 'GENERAL_DESCRIPTION', 'HERITAGE_PLACE_FUNCTION', 'HERITAGE_PLACE_FUNCTION_CERTAINTY', 'DESIGNATION', 'DESIGNATION_FROM_DATE', 'DESIGNATION_TO_DATE', 'GEOMETRIC_PLACE_EXPRESSION', 'GEOMETRY_QUALIFIER', 'SITE_LOCATION_CERTAINTY', 'GEOMETRY_EXTENT_CERTAINTY', 'SITE_OVERALL_SHAPE_TYPE', 'GRID_ID', 'COUNTRY_TYPE', 'CADASTRAL_REFERENCE', 'RESOURCE_ORIENTATION', 'ADDRESS', 'ADDRESS_TYPE', 'ADMINISTRATIVE_SUBDIVISION', 'ADMINISTRATIVE_SUBDIVISION_TYPE', 'OVERALL_ARCHAEOLOGICAL_CERTAINTY_VALUE', 'OVERALL_SITE_MORPHOLOGY_TYPE', 'CULTURAL_PERIOD_TYPE', 'CULTURAL_PERIOD_CERTAINTY', 'CULTURAL_SUBPERIOD_TYPE', 'CULTURAL_SUBPERIOD_CERTAINTY', 'DATE_INFERENCE_MAKING_ACTOR', 'ARCHAEOLOGICAL_DATE_FROM__CAL_', 'ARCHAEOLOGICAL_DATE_TO__CAL_', 'BP_DATE_FROM', 'BP_DATE_TO', 'AH_DATE_FROM', 'AH_DATE_TO', 'SH_DATE_FROM', 'SH_DATE_TO', 'SITE_FEATURE_FORM_TYPE', 'SITE_FEATURE_FORM_TYPE_CERTAINTY', 'SITE_FEATURE_SHAPE_TYPE', 'SITE_FEATURE_ARRANGEMENT_TYPE', 'SITE_FEATURE_NUMBER_TYPE', 'SITE_FEATURE_INTERPRETATION_TYPE', 'SITE_FEATURE_INTERPRETATION_NUMBER', 'SITE_FEATURE_INTERPRETATION_CERTAINTY', 'BUILT_COMPONENT_RELATED_RESOURCE', 'HP_RELATED_RESOURCE', 'MATERIAL_CLASS', 'MATERIAL_TYPE', 'CONSTRUCTION_TECHNIQUE', 'MEASUREMENT_NUMBER', 'MEASUREMENT_UNIT', 'DIMENSION_TYPE', 'MEASUREMENT_SOURCE_TYPE', 'RELATED_GEOARCH_PALAEO', 'OVERALL_CONDITION_STATE', 'DAMAGE_EXTENT_TYPE', 'DISTURBANCE_CAUSE_CATEGORY_TYPE', 'DISTURBANCE_CAUSE_TYPE', 'DISTURBANCE_CAUSE_CERTAINTY', 'DISTURBANCE_DATE_FROM', 'DISTURBANCE_DATE_TO', 'DISTURBANCE_DATE_OCCURRED_BEFORE', 'DISTURBANCE_DATE_OCCURRED_ON', 'DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME', 'EFFECT_TYPE', 'EFFECT_CERTAINTY', 'THREAT_CATEGORY', 'THREAT_TYPE', 'THREAT_PROBABILITY', 'THREAT_INFERENCE_MAKING_ASSESSOR_NAME', 'INTERVENTION_ACTIVITY_TYPE', 'RECOMMENDATION_TYPE', 'PRIORITY_TYPE', 'RELATED_DETAILED_CONDITION_RESOURCE', 'TOPOGRAPHY_TYPE', 'LAND_COVER_TYPE', 'LAND_COVER_ASSESSMENT_DATE', 'SURFICIAL_GEOLOGY_TYPE', 'DEPOSITIONAL_PROCESS', 'BEDROCK_GEOLOGY', 'FETCH_TYPE', 'WAVE_CLIMATE', 'TIDAL_ENERGY', 'MINIMUM_DEPTH_MAX_ELEVATION_M_', 'MAXIMUM_DEPTH_MIN_ELEVATION_M_', 'DATUM_TYPE', 'DATUM_DESCRIPTION_EPSG_CODE', 'RESTRICTED_ACCESS_RECORD_DESIGNATION']
				sheet = HeritagePlaceBulkUploadSheet(options['source'])
				for ch in sheet.columns():
					if ch == '':
						continue
					if ch in expected_nodes:
						continue
					self.__warn('', 'Unexpected column header: "' + str(ch) + '"', 'Please check you are using the correct version of the Heritage Place bulk upload template.')
				for i in range(0, sheet.count()):
					data.append(sheet.data(i))
				for error in sheet.errors():
					self.__warn(error[0], error[1], error[2])
			elif rm.name == 'Grid Square':
				sheet = GridSquareBulkUploadSheet(options['source'])
				for i in range(0, sheet.count()):
					data.append(sheet.data(i))
			else:
				self.__error("", "No bulk upload sheet for graph " + rm.name)
		else:
			self.__error("", "Could not open the file: " + str(options['source']))

		return data

	def __check_translated_data(self, data):

		if isinstance(data, (list)):

			ret = True
			for item in data:
				ret = ret & self.__check_translated_data(item)
			return ret

		if isinstance(data, (dict)):

			ret = True
			for keyobj in data.keys():
				key = str(keyobj)
				if key == '_':
					continue
				try:
					uo = uuid.UUID(key)
				except ValueError:
					self.__error("", '"' + key + '" is an invalid column value.')
					ret = False
			return ret

		return True

	def handle(self, *args, **options):

		data = []
		self.errors = []
		self.warnings = []

		warn_mode = 'warn'

		if options['dest_dir']:
			if not(os.path.exists(options['dest_dir'])):
				self.__error("", "Output path not found: " + options['dest_dir'])
			elif not(os.path.isdir(options['dest_dir'])):
				self.__error("", "Output path is not a directory: " + options['dest_dir'])

		if options['warn_mode'] != '':

			warn_mode = options['warn_mode']

		if options['operation'] == '':

			self.__error("", "No operation selected. Use --operation")

		if options['operation'] == 'convert':

			try:
				rm = GraphModel.objects.get(graphid=options['graph'])
			except GraphModel.DoesNotExist:
				rm = None

			if rm is None:
				self.__error("", "Invalid or missing graph UUID. Use --graph")
				model_name = ''
			else:
				model_name = str(rm.name)

			if model_name == 'Heritage Place':

				translated_data = self.__translate_heritage_place(options)
				if self.__check_translated_data(translated_data):
					resources = self.__convert_translated_data(translated_data, options)
					mapped_resources = self.__map_resources(resources, options)
					business_data = {"resources": mapped_resources}
					data = {"business_data": business_data}

			if model_name == 'Grid Square':

				translated_data = self.__translate_grid_square(options)
#				if self.__check_translated_data(translated_data):
				resources = self.__convert_translated_grid_square(translated_data, options)
				business_data = {"resources": resources}
				data = {"business_data": business_data}

#				data = []
#				for item in self.__unflatten(options):
#					grid_id = ''
#					grid_uuid = ''
#					if 'GRID_ID' in item[0]:
#						grid_id = item[0]['GRID_ID']
#					if 'GRID ID' in item[0]:
#						grid_id = item[0]['GRID ID']
#					if 'Grid ID' in item[0]:
#						grid_id = item[0]['Grid ID']
#					if grid_id == '':
#						continue
#					if not('GRID_SQUARE_GEOMETRIC_PLACE_EXPRESSION' in item[0]):
#						continue
#					ri = self.__resourceinstance_from_eamenaid(grid_id, str(rm.graphid))
#					if not(ri is None):
#						grid_uuid = str(ri.resourceinstanceid)
#					data.append([grid_uuid, grid_id, item[0]['GRID_SQUARE_GEOMETRIC_PLACE_EXPRESSION']])

		if options['operation'] == 'validate':

			translated_data = self.__translate_heritage_place(options)
			if self.__check_translated_data(translated_data):
				resources = self.__convert_translated_data(translated_data, options)
				mapped_resources = self.__map_resources(resources, options)
				business_data = {"resources": mapped_resources}

			if warn_mode != 'ignore':

				self.errors = self.errors + self.warnings
				self.warnings = []

			convert = lambda text: int(text) if text.isdigit() else text.lower()
			natsort_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key[0]) ]
			data = self.errors
			data.sort(key=natsort_key)
			self.errors = []

		if options['operation'] == 'prerequisites':

			translated_data = self.__translate_heritage_place(options)
			resources = self.__convert_translated_data(translated_data, options)
			prerequisites = self.__get_prerequisites(resources, options)
			business_data = {"resources": prerequisites}
			data = {"business_data": business_data}

		if options['operation'] == 'unflatten':

			data = self.__unflatten(options)

		if options['operation'] == 'translate':

			try:
				rm = GraphModel.objects.get(graphid=options['graph'])
			except GraphModel.DoesNotExist:
				rm = None

			if rm is None:
				self.__error("", "Invalid or missing graph UUID. Use --graph")
				model_name = ''
			else:
				model_name = str(rm.name)

			if model_name == 'Heritage Place':
				data = self.__translate_heritage_place(options)

			if model_name == 'Grid Square':
				data = self.__translate_grid_square(options)

			for i in range(0, len(data)):
				if '_' in (data[i]):
					del(data[i]['_'])

		if options['operation'] == 'list_nodes':

			data = self.__list_nodes(options)

		if options['operation'] == 'annotate':

			fn = options['source']
			fp = open(fn, 'r')
			data = json.loads('\n'.join(fp.readlines()))
			fp.close()
			nodes = self.__list_nodes(options)

			for r in range(0, len(data['business_data']['resources'])):
				for t in range(0, len(data['business_data']['resources'][r]['tiles'])):

					tileid = data['business_data']['resources'][r]['tiles'][t]['tileid']
					nodegroup_id = data['business_data']['resources'][r]['tiles'][t]['nodegroup_id']
					resourceinstance_id = data['business_data']['resources'][r]['tiles'][t]['resourceinstance_id']

					nodegroup_id_comment = ''
					resourceinstance_id_comment = ''
					data_fields = []
					for node in nodes:
						if node['nodeid'] == nodegroup_id:
							nodegroup_id_comment = node['name']
						if node['nodeid'] == resourceinstance_id:
							resourceinstance_id_comment = node['name']
						for ko in data['business_data']['resources'][r]['tiles'][t]['data'].keys():
							key = str(ko)
							if node['nodeid'] == key:
								data_fields.append(node['name'])

					if len(nodegroup_id_comment) > 0:
						data['business_data']['resources'][r]['tiles'][t]['nodegroup_name'] = nodegroup_id_comment
					if len(resourceinstance_id_comment) > 0:
						data['business_data']['resources'][r]['tiles'][t]['resourceinstance_name'] = resourceinstance_id_comment
					if len(data_fields) > 0:
						data['business_data']['resources'][r]['tiles'][t]['data_fields'] = data_fields

		if options['operation'] == 'summary':

			fn = options['source']
			fp = open(fn, 'r')
			data = json.loads('\n'.join(fp.readlines()))
			fp.close()

			if not('business_data' in data):
				self.__error('', "Not a valid business data file.", str(fn))
			else:
				if not('resources' in data['business_data']):
					self.__error('', "Not a valid business data file.", str(fn))

			ret = []
			if len(self.errors) == 0:

				for item in data['business_data']['resources']:
					if not('resourceinstance' in item):
						continue
					if not('resourceinstanceid' in item['resourceinstance']):
						continue
					id = str(item['resourceinstance']['resourceinstanceid'])
					eid = self.__eamenaid_from_resourceinstance(id)
					if len(eid) == 0:
						continue
					ret.append({"uuid": id, "eamenaid": eid})

			data = ret

		if options['operation'] == 'undo':

			fn = options['source']
			fp = open(fn, 'r')
			data = json.loads('\n'.join(fp.readlines()))
			fp.close()

			if not('business_data' in data):
				self.__error('', "Not a valid business data file.", str(fn))
			else:
				if not('resources' in data['business_data']):
					self.__error('', "Not a valid business data file.", str(fn))

			uuids = []
			if len(self.errors) == 0:

				for item in data['business_data']['resources']:
					if not('resourceinstance' in item):
						continue
					if not('resourceinstanceid' in item['resourceinstance']):
						continue
					id = str(item['resourceinstance']['resourceinstanceid'])
					uuids.append(id)

			if len(uuids) > 0:
				sys.stderr.write("Attempting to delete " + str(len(uuids)) + " resources.\n")

			attempts = 0
			processed = 0
			deleted_res = 0
			deleted_tiles = 0
			deleted_indices = 0

			es = Elasticsearch()
			for id in uuids:
				try:
					ri = ResourceInstance.objects.get(resourceinstanceid=id)
				except (ValidationError, ObjectDoesNotExist):
					ri = None
				if ri is None:
					continue
				attempts = attempts + 1
				deleted_items, delete_report = ri.delete()
				if deleted_items > 0:
					processed = processed + 1
					deleted_res = deleted_res + delete_report['models.ResourceInstance']
					deleted_tiles = deleted_tiles + delete_report['models.TileModel']
					try:
						index_report = es.delete(index='eamena_resources', id=id)
					except:
						index_report = {'result': 'exception'}
					if 'result' in index_report:
						if index_report['result'] == 'deleted':
							deleted_indices = deleted_indices + 1

			if len(uuids) > 0:
				sys.stderr.write("Resources for Removal: " + str(attempts) + ", Resources Deleted: " + str(deleted_res) + ", Tiles Deleted: " + str(deleted_tiles) + ", Indices deleted: " + str(deleted_indices) + "\n")
				sys.stderr.write("Resources not found: " + str(len(uuids) - processed) + "\n")

			data = [processed, deleted_res, deleted_tiles]

		if warn_mode == 'strict':

			self.errors = self.errors + self.warnings
			self.warnings = []

		if len(self.errors) > 0:

			for error in self.errors:
				sys.stderr.write(error[1] + '\n')
				if len(error[2]) > 0:
					sys.stderr.write(error[2] + '\n')
				sys.stderr.write('\n')

			if warn_mode != 'ignore':
				for warning in self.warnings:
					sys.stderr.write(warning[1] + '\n')
					if len(warning[2]) > 0:
						sys.stderr.write(warning[2] + '\n')
					sys.stderr.write('\n')

		else:

			if warn_mode != 'ignore':
				for warning in self.warnings:
					sys.stderr.write(warning[1] + '\n')
					if len(warning[2]) > 0:
						sys.stderr.write(warning[2] + '\n')
					sys.stderr.write('\n')

			if options['dest_dir']:
				fp = open(os.path.join(options['dest_dir'], os.path.basename(options['source']) + '.json'), 'w')
				fp.write(json.dumps(data))
				fp.close()
			else:
				if options['operation'] != 'undo':
					print(json.dumps(data))
