The workflow will be to:

```mermaid
flowchart LR
    A[(EAMENA DB)] --search--> A;
    A --export GeoJSON URL--> B[Create GeoJSON file];
    B --import--> C((Google Earth));
    C --"HPs POINTS are turned to POLYGONS"--> C;
    subgraph eamenaR
    C --export KML/KMZ--> D{{"geom_kml()"}}; 
    end
    D --add a new geometry--> A;
```