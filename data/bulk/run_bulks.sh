# SSH to EAMENA DB as arches user or super user
# .. 
# cd /home/$username/$project_name/$project_name/
# mkdir bulk_uploads

# change
# MANAGE="/home/$username/$project_name/manage.py"
# BUPATH="/home/$username/$project_name/$project_name/bulk_uploads/$1"
# source /home/$username/env/bin/activate

# MOVE cd /home/archesadmin/test_project/test_project/management/commands/
# modif
# from django.contrib.auth.models import User
# from django.contrib.gis.geos import GEOSGeometry
# from django.http import HttpRequest
# from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from arches.app.models.models import GraphModel, Node, ResourceInstance, TileModel
# from arches.app.models.concept import Concept, get_preflabel_from_valueid, get_valueids_from_concept_label
# from arches.app.views import search
# from django.core.management.base import BaseCommand
# from django.contrib.gis.geos.error import GEOSException
# from test_project.bulk_uploader import HeritagePlaceBulkUploadSheet, GridSquareBulkUploadSheet

# eamena -> $project_name
# HeritagePlaceBulkUploadSheet.py
# GridSquareBulkUploadSheet.py
...

# move
# local <-> remote: cd "C:\Users\Thomas Huet\Desktop\EAMENA\IT\bulks\"
cd /opt/arches/bulk_uploads
# cd /home/$username/$project_name/$project_name/bulk_uploads
BUFOLD="2022-06-16-Mohamed"
# convert (call 'python manage.py bu -w strict -o validate -g 34cfe98e-c2c0-11ea-9026-02e7594ce0a0 -s "$f" | json_pp')
./convert $BUFOLD
# virtual env (source env/bin/activate)
venv
# yes / no
cd $BUFOLD/for_import/
# BUFILE=$(ls | grep 'xlsx') # get all XLSX filenames
# python /$user_name/$project_name/manage.py packages -o import_business_data -s "AAA-f29_Kenawi.json" -ow overwrite
python /opt/arches/eamena/manage.py packages -o import_business_data -s "AAA-f26_Kenawi.json" -ow overwrite
# summary
# python /$user_name/$project_name/manage.py bu -o summary -s "AAA-f-33_Kenawi.json" | json_pp
python /opt/arches/eamena/manage.py bu -o summary -s "AAA-f27_Kenawi.json" | json_pp

