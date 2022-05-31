# folder path
BUFOLD="C:/Rprojects/_coll/Kites/"
# number of different id
IDS=2
pt="${BUFOLD}pt/"
ln="${BUFOLD}ln/"
pg="${BUFOLD}pg/"
for i in {1..$IDS}
do
    echo $i
done

# echo $BUFOLD


#ogr2ogr -f "ESRI Shapefile" C:\Rprojects\_coll\Kites\shp\ln C:\Rprojects\_coll\Kites\gpkg\ln\id_2.gpkg 


# c:/Rprojects/eamena-arches-dev/functions/gpkg_to_shp.sh