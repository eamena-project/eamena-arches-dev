
import folium

m = folium.Map(location=[24, 34], zoom_start=3)
folium.GeoJson(
    'C:/Rprojects/eamena-arches-dev/data/grids/EAMENA_Grid_contour.geojson',
    name='geojson'
).add_to(m)
m.save('C:/Rprojects/eamena-arches-dev/data/grids/EAMENA_Grid_contour.html')