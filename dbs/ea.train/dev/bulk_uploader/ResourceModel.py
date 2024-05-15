import json, uuid, re, urllib.request

class ResourceModel:

	def __init__(self, rm_file, legacy_uuid=''):

		fp = open(rm_file, 'r')
		jsondata = json.loads('\n'.join(fp.readlines()))
		fp.close()

		self.id = jsondata['graph'][0]['graphid']
		self.resid = legacy_uuid
		if legacy_uuid == '':
			self.resid = str(uuid.uuid4())
		self.name = jsondata['graph'][0]['name']
		self.nodes = {}
		self.tiles = []
		for node in jsondata['graph'][0]['nodes']:
			nodeid = node['nodeid']
			for nodegroup in jsondata['graph'][0]['nodegroups']:
				if nodegroup['nodegroupid'] != node['nodegroup_id']:
					continue
				node['nodegroup'] = nodegroup
				break
			self.nodes[nodeid] = node

	def get_node_datatype(self, nodeid):

		if not(nodeid in self.nodes):
			return ''
		return self.nodes[nodeid]['datatype']

	def get_rdm(self):

		return {}

	def get_node_rdm_collection(self, nodeid):

		if not(nodeid in self.nodes):
			return ''
		node = self.nodes[nodeid]
		if not('config' in node):
			return ''
		if not('rdmCollection' in node['config']):
			return ''
		return node['config']['rdmCollection']

	def get_node_nodegroup(self, nodeid):

		if not(nodeid in self.nodes):
			return ''
		return self.nodes[nodeid]['nodegroup_id']

	def get_nodegroup_index(self, nodegroupid):

		for i in range(0, len(self.tiles)):
			if self.tiles[i]['nodegroup_id'] == nodegroupid:
				return i
		if not(nodegroupid in self.nodes):
			return -1
		node = self.nodes[nodegroupid]
		if not('nodegroup' in node):
			self.tiles.append(self.create_tile(nodegroupid))
			return (len(self.tiles) - 1)
		if not('parentnodegroup_id' in node['nodegroup']):
			self.tiles.append(self.create_tile(nodegroupid))
			return (len(self.tiles) - 1)
		if node['nodegroup']['parentnodegroup_id'] is None:
			self.tiles.append(self.create_tile(nodegroupid))
			return (len(self.tiles) - 1)
		parentid = node['nodegroup']['parentnodegroup_id']
		parent = self.get_nodegroup_index(parentid)
		if parent < 0:
			self.tiles.append(self.create_tile(nodegroupid))
			return (len(self.tiles) - 1)
		parenttile = self.tiles[parent]
		self.tiles.append(self.create_tile(nodegroupid, parenttile['tileid']))
		return (len(self.tiles) - 1)

	def create_tile(self, nodegroupid, parent=None):

		ret = {}
		ret['parenttile_id'] = None
		ret['provisionaledits'] = None
		ret['sortorder'] = 0
		ret['tileid'] = str(uuid.uuid4())
		ret['nodegroup_id'] = nodegroupid
		ret['resourceinstance_id'] = self.resid
		ret['data'] = {}
		if parent:
			ret['parenttile_id'] = parent
		return ret

	def add(self, id, value):

		nodegroupid = self.get_node_nodegroup(id)
		ix = self.get_nodegroup_index(nodegroupid)
		if not('data' in self.tiles[ix]):
			self.tiles[ix]['data'] = {}
		if id in self.tiles[ix]['data']:
			if ((isinstance(value, list)) and (isinstance(self.tiles[ix]['data'][id], list))):
				self.tiles[ix]['data'][id] = self.tiles[ix]['data'][id] + value
				return self.tiles[ix]
		if id in self.tiles[ix]['data']:
			# Called if we're adding a subsequent new sub-tile
			newtile = self.create_tile(self.tiles[ix]['nodegroup_id'], self.tiles[ix]['parenttile_id'])
			newtile['data'][id] = value
			self.tiles.append(newtile)
			return newtile
		else:
			# Called if we're adding a new value to an existing card, or the first new sub-tile
			self.tiles[ix]['data'][id] = value
			return self.tiles[ix]

	def dump_json(self):

		item = {}
		item['resourceinstance'] = {
			"resourceinstanceid" : self.resid, "graph_id" : self.id, "legacyid" : self.resid}
		item['tiles'] = self.tiles

		business_data = {"resources": []}
		business_data['resources'].append(item)
		return json.dumps({"business_data": business_data})

	def dump_jsonl(self):

		item = {}
		item['resourceinstance'] = {
			"resourceinstanceid" : self.resid, "graph_id" : self.id, "legacyid" : self.resid}
		item['tiles'] = self.tiles

		return json.dumps(item)
