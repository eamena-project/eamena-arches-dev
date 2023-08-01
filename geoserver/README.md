# GeoServer

<p align="center">
  <img alt="img-name" src="../www/gis-qgis-geoserver-example.png" width="300">
  <br>
    <em>Screenshot of the QGIS project with connected to the GeoServer: grids (WFS) and the 'Atlas Archéologique d'Algérie'</em>
</p>


EAMENA GeoServer (http://54.155.109.226:8080/geoserver) host different files

| Service  	|  URL 	|
|---	|---	|
| WFS  	|  http://54.155.109.226:8080/geoserver/ows?acceptversions=2.0.0 	|
| WMS 	|  http://54.155.109.226:8080/geoserver/ows?version=1.3.0 	|

## WFS

Web File Services

| type | Name  	|   description	| map |
|---	|---	|---	|--- |
| Grids | EAMENA_Grid_contour  	| EAMENA Grid Squares perimeter	| <img alt="img-name" src="../www/geoserver-map-wfs-gs-contour.png" width="250"> |
| Grids | EAMENA_Grid  	|  EAMENA Grid Squares 	| <img alt="img-name" src="../www/geoserver-map-wfs-gs.png" width="250"> |
| Grids | grids_nb_hp_230704  |  Nb of heritage places by Grid Squares (see eamenaR) 	|  <img alt="img-name" src="../www/geoserver-map-wfs-gs-nb-hp.png" width="250"> |

## WMS

Web Map Services

| type | Name  	|   description	| map |
|---	|---	|---	|--- |
| Atlas | AAA  	| Atlas Archéologique d'Algérie	| <img alt="img-name" src="../www/geoserver-map-wms-aaa.png" width="250"> |
| Climate | Beck_KG_V1_present_0p008  	| Koppen Climate Classification	| <img alt="img-name" src="../www/geoserver-map-wms-koppen.png" width="250"> |



