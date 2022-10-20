## Integrating Google Earth geometries

Most of the geometries in EAMENA are POINTS (Center Point). The objective is to acquire new geometries created in Google Earth and to add them to already existing records in EAMENA.

```mermaid
flowchart LR
    A[(EAMENA DB)] --1. export as GeoJSON--> B[GeoJSON file];
    B((Google Earth)) --2. create POLYGON geometries--> B;
    B --3. export as KML/KMZ--> C("geom_kml()"):::eamenaRfunction;
    C --4. add new GeoJSON geometries--> A;
    classDef eamenaRfunction fill:#e7deca;
```

[#e7deca](https://via.placeholder.com/150/e7deca/000000?Text=geom_kml.png) geom_kml()

$\colorbox{#e7deca}{{\color{black}{eamenaR functions}}}$: [geom_kml()](https://eamena-oxford.github.io/eamenaR/doc/geojson_kml)

$\colorbox{brown}{{\color{black}{xxx}}}$


- ![#e7deca](https://via.placeholder.com/15/f03c15/e7deca.png) `#e7deca`  

