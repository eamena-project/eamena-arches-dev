# SSH to EAMENA DB
# .. 
# move
cd /opt/arches/bulk_uploads
# local <-> remote: cd "C:\Users\Thomas Huet\Desktop\EAMENA\IT\bulks\"
BUFOLD="2022-03-23-Michael"
# convert
./convert $BUFOLD
cd $BUFOLD/for_import/
# BUFILE=$(ls | grep 'xlsx') # get all XLSX filenames
python /opt/arches/eamena/manage.py packages -o import_business_data -s "AAA-f-33_Kenawi.json" -ow overwrite
python /opt/arches/eamena/manage.py bu -o summary -s "AAA-f-33_Kenawi.json" | json_pp

