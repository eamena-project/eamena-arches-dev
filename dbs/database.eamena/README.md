# EAMENA DB

## Timeline

```mermaid
gantt
    title Arches v5.2 to v7
    dateFormat  YYYY-MM-DD
    section EAMENA
    EAMENA Arches v5.2       : a0, 2022-11-01, 90d
    section Arches v7
    Installation v7.1.1      : a1, 2022-12-01, 30d
    Test with EAMENA data    : milestone, m1, 2022-12-05, 10d
    Installation v7.1.x      : after a1, 30d
    Test with EAMENA data    : milestone, m2, 2023-01-05, 10d
```

## Upgrade Arches v5.2 to v7

Needed updates

```mermaid
flowchart LR
    A(Pg 12.12) --- B(Pg 12);
    C(Postgis 3.1.1) --- D(Postgis 3);
    E(ElasticSearch 7.1.1) --> F(ElasticSearch 7.4);
```
legend:
`---` no upgrade  
`-->` upgrade