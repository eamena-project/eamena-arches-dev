# Dev

Scheduled developments and miscellaneous

## Mapbox

Development on Mapbox

### Cluster zooming

*expected behaviour*: after clicking on a cluster, this cluster explode and there's an automatic zoom-in to its minimum bound rectangle. The behaviour we expect is similar to Arches v3

see: https://community.archesproject.org/t/mapbox-cluster-zooming/1964

### Collect the coordinates

*expected behaviour*: on a click in the map, lon/lat coordinates of the point are shown in the bottom-right or bottom-left of the map and can be copied in the clipboard

### Cluster of Clusters

*expected behaviour*: group in cluster or explode clusters depending on zoom-in zoom-ou

<p align="center">
  <img src="../www/arches-v7-dev-mapbox-ClustOfClust.gif" width="500">
  <br>
    <em>caption</em>
</p>

### Reverse geocoding

*expected behaviour*: be able to find a place (zoom-in) from its coordinates 

<p align="center">
  <img src="../www/arches-v7-dev-mapbox-revgeocod.gif" width="500">
  <br>
    <em>caption</em>
</p>

see: https://community.archesproject.org/t/reverse-geocoding-zoom-in-from-coordinates/1852

### Zoom level

+ Keep the same level of zoom when clicking on the 'map' button 

<p align="center">
  <img alt="img-name" src="../www/zoom-map-same-zoom.png" width="700">
  <br>
    <em>caption</em>
</p>

Today when click on the 'map' button, there's a de-zoom

example: Search 'Suq Sirmayatiya (Market)' = [EAMENA-0166083](https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&precision=6&total=336316&term-filter=%5B%7B%22inverted%22%3Afalse%2C%22type%22%3A%22string%22%2C%22context%22%3A%22%22%2C%22context_label%22%3A%22%22%2C%22id%22%3A%22Suq%20Sirmayatiya%20(Market)%22%2C%22text%22%3A%22Suq%20Sirmayatiya%20(Market)%22%2C%22value%22%3A%22Suq%20Sirmayatiya%20(Market)%22%7D%5D)

---

## Images

Restore the path of images

<p align="center">
  <img alt="img-name" src="../www/images-uploaded-error.png" width="700">
  <br>
    <em>caption</em>
</p>
  
example: Search INFORMATION-0104667

---

## Audit

### Translate https://mareastats.drashsmith.com/ from PHP to Python

<p align="center">
  <img alt="img-name" src="../www/audit-data-sums.png" width="400">
  <br>
    <em>caption</em>
</p>

### Data completness

Develop a Python function to model the quality of HP (or HR) with a radar diagram

https://github.com/eamena-project/eamena-arches-5-project/blob/master/eamena/statistics/hr_quality_rec.py
