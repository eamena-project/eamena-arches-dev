# Dev

## Mermaid Git Diagram

```mermaid
%%{init: { 'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'showBranches': false}} }%%
gitGraph
       commit id: "JADIS"
       commit id: "MEGA Jordan"
       branch "Arches v5"
       commit id: "Jordan Masdar"
       checkout main
       commit id: "XXX"
```


## PostgreSQL Views

Planning of Arches v7 (EAMENA v4) installation, test and release.

```mermaid
flowchart LR
  subgraph EC2 [EC2 AWS]
    direction TB
    subgraph PostgreSQL
        direction LR
        subgraph DB [Server 1]
            direction TB
            A[tiles] --- B[resources]
            B --- Z[...]
        end
        subgraph VIEWS [Server 2]
            direction TB
            C[view 1] --- Y[view ...]
        end
    end
  end
  DB -- is read by --> VIEWS
  VIEWS -- is read by --> D{{eamenaR}}:::eamenaRpkg
  D -- ODBC connection --> VIEWS
  D -- creates outputs --> E[maps<br>charts<br>listings<br>...]
  classDef eamenaRpkg fill:#e3c071
```