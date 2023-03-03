

```mermaid
flowchart LR
    A[structured file<br><em>source</em>] ----> B("list_mapping_bu()"):::eamenaRfunction;;
    B --uses mapping file--> B;
    B --export--> C[BU file<br><em>target</em>];
    classDef eamenaRfunction fill:#e7deca;
```


any structured file (source) ➡️ ***eamenaR*** mapping function + mapping file ➡️ bulk upload file (target)


```{mermaid}
flowchart LR
subgraph ide1 [Arches];
A[(EAMENA<br>DB)];
end;
A <--data<br>exchange--> B{{"eamenaR"}}:::eamenaRpkg;
B --data<br>analysis & management--> B;
B <--data<br>exchange--> C((3<sup>rd</sup> part<br>app));
B --"output"--> D[maps<br>charts<br>listings<br>...];
classDef eamenaRpkg fill:#e3c071;
```
