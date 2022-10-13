The workflow will be to:

```mermaid
flowchart LR
    A[(EAMENA DB)] --search--> A;
    A --export GeoJSON URL--> B[Create GeoJSON file];
    B --import--> C((Google Earth));
    C --"HPs POINTS -> POLYGONS"--> C;
    C --export KML/KMZ--> D{{"geom_kml()"}}; 
    subgraph eamenaR
    D --"convert KML/KMZ to GeoJSON"--> D;
    D --export--> E{{"geom_bu()"}};
    E --"TODO: format GeoJSON as a BU"--> E
    end
    E --add a new geometry-->A;
```