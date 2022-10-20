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

[geom_kml()](https://via.placeholder.com/150/e7deca/000000?Text=geom_kml())
```

https://via.placeholder.com/150/e7deca/000000?Text=geom_kml()





- ![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png) `#f03c15`  
- ![#e7deca](https://via.placeholder.com/15/f03c15/e7deca.png) `#e7deca`  
<span style="color:'#e7deca'">eamenaR function</span>

