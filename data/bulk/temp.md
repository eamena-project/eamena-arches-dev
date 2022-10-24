

```mermaid
flowchart LR
    A[structured file<br><em>source</em>] ----> B("list_mapping_bu()"):::eamenaRfunction;;
    B --uses mapping file--> B;
    B --export--> C[BU file<br><em>target</em>];
    classDef eamenaRfunction fill:#e7deca;
```


any structured file (source) ➡️ ***eamenaR*** mapping function + mapping file ➡️ bulk upload file (target)
