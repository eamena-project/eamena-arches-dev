# Dev


## PostgreSQL Views

```mermaid
flowchart LR
  subgraph TOP
    direction TB
    subgraph B1
        direction RL
        i1 -->f1
    end
    subgraph B2
        direction BT
        i2 -->f2
    end
  end
  A --> TOP --> B
  B1 --> B2
```

```mermaid
flowchart LR
  subgraph EC2 [EC2 on AWS]
    subgraph PG [PostgreSQL]
      subgraph EA [Server 1 is EAMENA]
        A[tiles]
        B[resources]
      end
      subgraph VIEW [Server 2]
        C[VIEWS]
      end
  end
```