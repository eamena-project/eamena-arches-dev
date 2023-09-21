# Basemaps

## Add a basemap to Arches/EAMENA


### Non Mapbox basemaps

Using the [stamen-terrain-background.json](https://github.com/eamena-project/eamena-arches-dev/blob/main/spatial/basemaps/stamen-terrain-background.json) file

1. In EAMENA backend, download the basemap definition, run

```wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/spatial/basemaps/stamen-terrain-background.json```

2. 

Register the basemaps running:

```bash
python manage.py packages -o add_mapbox_layer -j "stamen-terrain-background.json" -n "stamen-terrain-background" -b
```

see also the [stamen-watercolor example](https://github.com/archesproject/arches-map-layers/tree/master#xyz-tileset) by Arches