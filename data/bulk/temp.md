
## BU exchanges

The objective is to:

- exchange data between EAMENA and national instances BDs (eg: Mega-J once this database has been ported to Arches v7)
- facilitate the edition of already existing data in the EAMENA DB

```mermaid
flowchart RL
    A[(EAMENA DB)] --export as BU--> B[XLSX];
    subgraph local
    B --edit data--> B;
    end
    B --re-import--> A;
```