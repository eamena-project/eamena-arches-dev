

```mermaid
flowchart LR
    A[(EAMENA DB)] --1. export as GeoJSON--> C("geojson_kml()"):::eamenaRfunction;
    C --KML file--> B((Google Earth));
    B --2. create POLYGON geometries--> B;
    B --3. export as KML/KMZ--> C;
    C -.4. add new GeoJSON geometries.-> A;
    classDef eamenaRfunction fill:#e7deca;
```
