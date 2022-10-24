

```mermaid
flowchart LR
    A[(EAMENA DB)] --export GeoJSON--> B("eamenaR"):::eamenaRpkg;
    B --data management--> B;
    B --data conversion--> C((third part app));
    C --import--> B;
    B --re-import--> A;
    B --creates--> D[maps<br>charts<br>listings<br>...]
    classDef eamenaRpkg fill:#e3c071;
```

