# Dev

## Arches v5.2 to v7.3 upgrade

### Proposed workflow
> cf. https://github.com/archesproject/arches/blob/dev/7.3.x/releases/7.3.0.md#upgrading-arches

```mermaid
flowchart LR
    A["v7.0"] --> B["v7.2"]
    B --> C["v7.3"]
```

## National instances
> [Git Mermaid diagram](https://mermaid.js.org/syntax/gitgraph.html) 

Example of a Palestinian national instance with EAMENA data

```mermaid
gitGraph
       commit  tag: "Arches v7"
       branch Palestine
       commit
       commit
       commit id:"National instance"  tag: "Arches v7"
       checkout main
       commit
       commit
       commit
       commit
       commit
       commit
       checkout Palestine
       commit
       checkout main
       commit
       cherry-pick id:"National instance"
       commit
       checkout Palestine
       commit
```

## From JADIS to a new Jordanian national instance
> [Git Mermaid diagram](https://mermaid.js.org/syntax/gitgraph.html) 

```mermaid
gitGraph
       commit id: "JADIS"
       commit id: "MEGA Jordan"
       branch "Jordania"
       commit id: "Jordan Masdar" tag: "Arches v5"
       checkout main
       commit id: "XXX" tag: "Arches v7"
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