The workflow will be to:

```mermaid
flowchart LR
    A[(EAMENA DB)] --search--> A;
    A --export GeoJSON URL--> B[GeoJSON file HPs as POINTS];
    B --import--> C{Google Earth};
    C --"HPs as POLYGONS"--> C;
    C --export KML/KMZ--> D{{"geom_kml()"}}; 
    D --add a new geometry--> A;
```