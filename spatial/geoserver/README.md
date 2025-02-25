# GeoServer

## EAMENA GeoServer

The EAMENA GeoServer (http://54.155.109.226:8080/geoserver) host different files

| Service  	|  URL 	|
|---	|---	|
| WFS  	|  http://54.155.109.226:8080/geoserver/ows?acceptversions=2.0.0 	|
| WMS 	|  http://54.155.109.226:8080/geoserver/ows?version=1.3.0 	|

### WFS

Web File Services

| type | Name  	|   description	| map |
|---	|---	|---	|--- |
| Grids | EAMENA_Grid_contour  	| EAMENA Grid Squares perimeter	| <img alt="img-name" src="../../www/geoserver-map-wfs-gs-contour.png" width="250"> |
| Grids | EAMENA_Grid  	|  EAMENA Grid Squares 	| <img alt="img-name" src="../../www/geoserver-map-wfs-gs.png" width="250"> |
| Grids | grids_nb_hp_230704  |  Nb of heritage places by Grid Squares (see [eamenaR](https://github.com/eamena-project/eamenaR#grids)) 	|  <img alt="img-name" src="../../www/geoserver-map-wfs-gs-nb-hp.png" width="250"> |

### WMS

Web Map Services

| type | Name  	|   description	| map |
|---	|---	|---	|--- |
| Atlas | AAA  	| Atlas Archéologique d'Algérie	| <img alt="img-name" src="../../www/geoserver-map-wms-aaa.png" width="250"> |
| Climate | Beck_KG_V1_present_0p008  	| Koppen Climate Classification ([legend](../../data/layouts/koppen_climate_class.md))	| <img alt="img-name" src="../../www/geoserver-map-wms-koppen.png" width="250"> |

## Install

Following the tutorial: https://www.youtube.com/watch?v=awR4RgJNhVU

Ubuntu 20.04 or Ubuntu 10.04

On your AWS instance, autorise the world

```
TCP/IP | 8080 | 0.0.0.0/
TCP/IP | 8080 | ::/0
```
Check your Java version, or even if Java is installed

```sh
java -version
```

If Java is not installed[^1], install it doing:

```sh
sudo apt install default-jre
```

create a geoserver/ folder and move in it

```sh
mkdir geoserver
cd geoserver
```

download the binaries (Platform Independent Binary) from https://geoserver.org, for example[^2]

```sh
wget https://sourceforge.net/projects/geoserver/files/GeoServer/2.22.1/geoserver-2.22.1-bin.zip
```

unzip the geoserver

```sh
unzip geoserver-2.22.1-bin.zip
```

Add the parent folder of the GS in the environment variables, for example[^3]

```sh
echo "export GEOSERVER_HOME=/home/archesadmin/my_project/geoserver" >> ~/.profile
. ~/.profile
```

change the ownership of the `geoserver/` folder if needed

```sh
sudo chown -R root /home/archesadmin/my_project/geoserver
```

go to the `bin/` folder

```sh
cd bin
```

run the install shell script

```sh
nohup sh startup.sh &
```

access the GS from its public IP: http://34.243.109.142:8080/geoserver
by default:
 - username = `admin`
 - password = `geoserver`


[^1]: run `java -version`. If not installed, the message will be: `Command 'java' not found, ...`
[^2]: more recent: `wget https://sourceforge.net/projects/geoserver/files/GeoServer/2.24.2/geoserver-2.24.2-bin.zip`
[^3]: echo "export GEOSERVER_HOME=/opt/arches/geoserver" >> ~/.profile

## Examples

### Erbil Citadel

* Map Sources

![alt text](image.png)


erbil-citadel

{"type": "raster", "tiles": ["http://18.203.169.24:8080/geoserver/ows?bbox={bbox-epsg-3857}&format=image/png&service=WMS&version=1.3.0&request=GetMap&srs=EPSG:3857&width=256&height=256&layers=temp:Picture2_modified_clipped&transparent=true&tiled=true"], "tileSize": 256}

* Map Layer

![alt text](image-1.png)
![alt text](image-2.png)

[{"id": "erbil-citadel", "type": "raster", "source": "erbil-citadel"}]
