from fileinput import close
from operator import length_hint
import re
from django.core.management.base import BaseCommand, CommandError

#imports
import csv, json
from arches.app.models.resource import Resource
from arches.app.utils.betterJSONSerializer import JSONSerializer

 
class Command(BaseCommand):
    """
    Description:
    This command a .csv file containing ResourceID and downloads all corresponding resources to jsonl

    Parameters:
    '-s': path to .csv

    Returns:
    '.jsonl': file containing all records
    """
    def add_arguments(self, parser):

        parser.add_argument("-s", "--source", action="store", dest="file_path", default="", help="File path to csv containing ResourceID's")

    def handle(self, *args, **options):
    
        #Load CSV
        resource_ids = []
        csv_path = options['file_path']

        #Open target file as a dictionary
        with open (csv_path, newline="") as csv_file:
            csv_reder = csv.DictReader(csv_file, delimiter=',')
            totalrows = 0
            for row in csv_reder:
                totalrows += 1
            print("... nb of records")
            print(totalrows)

            #Copy all ResourceID's to new array
            for row in csv_reder:
                resource_ids.append(row[ 'ResourceID'])
            print("... nb of ResourceID")
            print(len(resource_ids))


        records = self.get_resource(resource_ids)
        
        self.write_to_file(records)

    def get_resource(self, resource_ids):
        '''
        Description:
        Loads all requested objects from DB 

        Parameters:
        'resource_ids': a list of all requeried ResourceID's

        Returns:
        'records': a list of serialized Resource Objects
        '''
        records = []
        for id in resource_ids:
            if Resource.objects.filter(pk=id).exists():
                resource = Resource.objects.get(pk = id)
                resource.load_tiles()
                resource_json = JSONSerializer().serializeToPython(resource)
               # print(resource_json)
                # records.append({'resourceinstance':resource_json})
                records.append({'resourceinstance' : 
                    { 'graph_id' : resource_json['graph_id'],
                    'legacyid' : resource_json['legacyid'],
                    'displaydescription': resource_json['displaydescription'],
                    'map_popup': resource_json['map_popup'],
                    'displayname': resource_json['displayname'],
                    'resourceinstanceid' : resource_json['resourceinstanceid'],
                },
                    'tiles' : resource_json['tiles']})

        return records

    def write_to_file(self, records):

        with open('json_records.jsonl', 'w') as json_records:
            print("... write into jsonl")
            print(len(records))
            for record in records:
                json.dump(record, json_records)
                json_records.write("\n")