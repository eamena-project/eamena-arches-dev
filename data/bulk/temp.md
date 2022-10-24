

```mermaid
flowchart LR
    A[(EAMENA DB)] --1. export as GeoJSON--> C("geojson_kml()"):::eamenaRfunction;
    C --2. export as KML file--> B((Google Earth));
    B --3. create POLYGON geometries--> B;
    B --4. export as KML/KMZ--> C;
    C -.5. add new GeoJSON geometries.-> A;
    classDef eamenaRfunction fill:#e7deca;
```
