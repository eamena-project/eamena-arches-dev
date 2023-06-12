# Dev
> scheduled developments and miscellaneous

## Images

Restore the path of images

<p align="center">
  <img alt="img-name" src="../www/images-uploaded-error.png" width="700">
  <br>
    <em>caption</em>
</p>
  
example: Search INFORMATION-0104667

## Spatial

### Collect the coordinates

*expected behaviour*: on a click in the map, lon/lat coordinates of the point are shown in the bottom-right or bottom-left of the map and can be copied in the clipboard

### Cluster of Clusters

*expected behaviour*: group in cluster or explode clusters depending on zoom-in zoom-ou

Restore the path of images

<p align="center">
  <img src="../www/arches-v7-dev-mapbox-ClustOfClust.gif" width="500">
  <br>
    <em>caption</em>
</p>
  

### Cluster zooming

*expected behaviour*: after clicking on a cluster, this cluster explode and there's an automatic zoom-in to its minimum bound rectangle. The behaviour we expect is similar to Arches v3

see: https://community.archesproject.org/t/mapbox-cluster-zooming/1964

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

## Time

### EDTF

<p align="center">
  <img alt="img-name" src="../www/time-edtf-cultural-periods.png" width="700">
  <br>
    <em>caption</em>
</p>

### Audit

Translate https://mareastats.drashsmith.com/ from PHP to Python

<p align="center">
  <img alt="img-name" src="../www/audit-data-sums.png" width="700">
  <br>
    <em>caption</em>
</p>

## Related resources
> test to add contains relation with 23test 

example: Search EAMENA-0185187
https://database.eamena.org/en/search?paging-filter=1&tiles=true&format=tilecsv&precision=6&total=336316&term-filter=%5B%7B%22context%22%3A%22%22%2C%22context_label%22%3A%22Heritage%20Place%20-%20EAMENA%20ID%22%2C%22id%22%3A0%2C%22text%22%3A%22EAMENA-0185187%22%2C%22type%22%3A%22term%22%2C%22value%22%3A%22EAMENA-0185187%22%2C%22inverted%22%3Afalse%7D%5D

## LOD
> Linked open data

See 'Related resources', try to recover the info with a SPARQL endpoint


## Quality of information

Develop a Python function to model the quality of HP (or HR) with a radar diagram

https://github.com/eamena-project/eamena-arches-5-project/blob/master/eamena/statistics/hr_quality_rec.py

## Arches v5.2 to v7.3 upgrade

### Proposed workflow
> cf. https://github.com/archesproject/arches/blob/dev/7.3.x/releases/7.3.0.md#upgrading-arches

```mermaid
flowchart LR
    A["v5.2"] --> B["v6.0.0"]
    B --> C["v6.0.1"]
    C --> D["v7.0"]
    D --> E["v7.2"]
    E --> F["v7.3"]
```

## National instances
> [Git Mermaid diagram](https://mermaid.js.org/syntax/gitgraph.html) 

Example of a Palestinian national instance with EAMENA data

```mermaid
gitGraph
       commit  tag: "Arches v7"
       branch Palestine
       commit
       commit
       commit id:"National instance"  tag: "Arches v7"
       checkout main
       commit
       commit
       commit
       commit
       commit
       commit
       checkout Palestine
       commit
       checkout main
       commit
       cherry-pick id:"National instance"
       commit
       checkout Palestine
       commit
```

## From JADIS to a new Jordanian national instance
> [Git Mermaid diagram](https://mermaid.js.org/syntax/gitgraph.html) 

```mermaid
gitGraph
       commit id: "JADIS"
       commit id: "MEGA Jordan"
       branch "Jordania"
       commit id: "Jordan Masdar" tag: "Arches v5"
       checkout main
       commit id: "XXX" tag: "Arches v7"
```


## PostgreSQL Views

Planning of Arches v7 (EAMENA v4) installation, test and release.

```mermaid
flowchart LR
  subgraph EC2 [EC2 AWS]
    direction TB
    subgraph PostgreSQL
        direction LR
        subgraph DB [Server 1]
            direction TB
            A[tiles] --- B[resources]
            B --- Z[...]
        end
        subgraph VIEWS [Server 2]
            direction TB
            C[view 1] --- Y[view ...]
        end
    end
  end
  DB -- is read by --> VIEWS
  VIEWS -- is read by --> D{{eamenaR}}:::eamenaRpkg
  D -- ODBC connection --> VIEWS
  D -- creates outputs --> E[maps<br>charts<br>listings<br>...]
  classDef eamenaRpkg fill:#e3c071
```