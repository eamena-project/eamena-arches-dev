The workflow will be to:

```mermaid
flowchart LR
    A[(EAMENA DB)] --search--> A;
    A --export GeoJSON URL--> B["GeoJSON file with HP Centroids (POINTS)"];
    B --import--> C[Google Earth];
    C --"map HP spatial print (POLYGONS)"--> C;
    C --export KML/KMZ--> A; 
```