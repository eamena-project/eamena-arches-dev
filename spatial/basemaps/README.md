# Basemaps

## Add base maps to Arches/EAMENA

Using the [stamen-terrain-background.json]() file, run:

```bash
python manage.py packages -o add_mapbox_layer -j "stamen-terrain-background.json" -n "stamen-terrain-background" -b
```