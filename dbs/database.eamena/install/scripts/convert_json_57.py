from django.core.management.base import BaseCommand
from arches.app.models.system_settings import settings
from arches.app.search.base_index import get_index
from arches.app.search.mappings import (
    prepare_terms_index,
    prepare_concepts_index,
    delete_terms_index,
    delete_concepts_index,
    prepare_search_index,
    delete_search_index,
    delete_resource_relations_index,
)
from arches.app.models import models
import arches.app.utils.index_database as index_database_util
import logging, sys, os, json, re

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Converts Arches JSON from v5 to v7 (adds multi-language support for strings)

    """

    def add_arguments(self, parser):

        parser.add_argument("-s", "--source", action="store", dest="input_file", default="", help="Input file, exported from Arches 5")

    def datatype(self, nodeid):

        if nodeid in self.cache:
            return self.cache[nodeid]
        try:
            ret = str(models.Node.objects.get(nodeid=nodeid).datatype)
        except:
            ret = ''
        self.cache[nodeid] = ret

        return ret

    def handle(self, *args, **options):

        arabic_regex = r'[ء-ي]+'

        self.cache = {}
        input_file = options['input_file']
        if len(input_file) == 0:
            sys.stderr.write("Need an input file.\n");
            sys.exit(1)

        if not os.path.exists(input_file):
            sys.stderr.write("Input file doesn't exist.\n");
            sys.exit(1)

        with open(input_file, 'r') as fp:
            data = json.load(fp)

        ret = {}
        if 'business_data' in data:
            for k in data['business_data'].keys():
                kk = str(k)
                if kk != 'resources':
                    ret[kk] = data['business_data'][kk]
                    continue
                ris = []
                for item in data['business_data']['resources']:
                    ri = {}
                    for k2 in item.keys():
                        kk2 = str(k2)
                        if kk2 != 'tiles':
                            ri[kk2] = item[kk2]
                            continue
                        ri['tiles'] = []
                        for tile in item['tiles']:
                            for nodeidobj in tile['data'].keys():
                                nodeid = str(nodeidobj)
                                if not isinstance(tile['data'][nodeid], (str)):
                                    continue
                                if self.datatype(nodeid) != 'string':
                                    continue
                                if re.match(arabic_regex, tile['data'][nodeid]) is None:
                                    tile['data'][nodeid] = {"en": {"direction": "ltr", "value": tile['data'][nodeid]}}
                                else:
                                    tile['data'][nodeid] = {"ar": {"direction": "rtl", "value": tile['data'][nodeid]}}
                            ri['tiles'].append(tile)
                    ris.append(ri)
                ret['resources'] = ris

        print(json.dumps({'business_data': ret}, indent=4))