# connect
cd Desktop/EAMENA/IT/keys
ssh -i EAMENAprod.pem arches@54.155.109.226
# move
cd /opt/arches/bulk_uploads
# local <-> remote: cd "C:\Users\Thomas Huet\Desktop\EAMENA\IT\bulks\"
BUFOLD="2022-03-18a-Mohamed"
# convert
./convert $BUFOLD
cd $BUFOLD/for_import/
python /opt/arches/eamena/manage.py packages -o import_business_data -s "AAA-f-33_Kenawi.json" -ow overwrite
python /opt/arches/eamena/manage.py bu -o summary -s "AAA-f-33_Kenawi.json" | json_pp