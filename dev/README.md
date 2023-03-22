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
  subgraph EC2
    direction TB
    subgraph Server 1 EAMENA DB
        direction TB
        A[tiles] <--> B[resources]
    end
    subgraph Server 2 VIEWS
        direction TB
        C[view 1]
    end
  end
  A --> EC2 --> B
  B1 --> B2
```

```mermaid
flowchart LR
  subgraph EC2
    direction TB
    subgraph PostgreSQL
        direction LR
        subgraph Server 1 EAMENA DB
            direction TB
            A[tiles] <---> B[resources]
        end
        subgraph Server 2 VIEWS
            direction TB
            C[view 1] --> A & B  
        end
    end
  end
  A --> EC2 --> B
  B1 --> B2
```


```mermaid
flowchart LR
  subgraph [EC2 on AWS]
    direction RL
    subgraph [PostgreSQL]
      direction RL
      subgraph [Server 1 is EAMENA]
        direction RL
          A[tiles]
          B[resources]
      end
      subgraph [Server 2]
        direction RL
          C[VIEWS]
      end
    end
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