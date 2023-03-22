# EAMENA DB

## Timeline

```mermaid
gantt
    title EAMENA database
    dateFormat  YYYY-MM-DD
    section EAMENA v3
    Arches v5.2              : a0, 2022-11-01, 90d
    Arches v5.2 stopped      : milestone, m3, 2023-04-10, 4d
    section EAMENA v3 -> v4
    Arches v7.3 DB installation        : a1, 2023-03-06, 2d
    Arches v7.3 Graphs installation    : a1, 2023-03-06, 2d
    Arches v7.3 Data                   : a1, 2023-04-10, 4d
    Arches v7.3 Custom components      : a1, 2023-04-10, 4d
    Arches v7.3 Reindexing             : a1, 2023-04-15, 2d
    Arches v7.3 DNS change             : a1, 2023-04-17, 1d
    section EAMENA v4
    Arches v7.3 tests                  : a1, 2023-04-17, 5d
    Arches v7.3 published              : a1, 2023-04-24, 2025-01-01
    section Trainings
    KRG training             : milestone, m3, 2023-05-09, 7d
    IST training             : milestone, m3, 2023-06-06, 7d
    AMM training             : milestone, m3, 2023-06-17, 7d
```

## Upgrade Arches v5.2 to v7

Needed updates

```mermaid
flowchart LR
    A(Pg 12.12) --> B(Pg 14);
    C(Postgis 3.1.1) --- D(Postgis 3);
    E(ElasticSearch 7.1.1) --> F(ElasticSearch 8.3.1);
```
legend:  
`---` no upgrade  
`-->` upgrade
