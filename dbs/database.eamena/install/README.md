# Installation
> Installation, upgrade and migration

* Arches v7: [README](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/docs)

## DB migration process timeline

EAMENA v5.2 to v7.3 migration process timeline

```mermaid
gantt
    title EAMENA v4 Arches v7 training
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%m
    tickInterval 7day
    section EAMENA v3
    Arches v5.2              : a0, 2023-01-01, 2023-04-24
    Arches v5.2 stopped      : a0, 2023-04-28, 2023-05-09
    section EAMENA v3 -> v4
    Arches v7.3 DB installation        : a1, 2023-03-06, 2d
    Arches v7.3 Graphs installation    : a1, 2023-03-06, 2d
    Arches v7.3 Data                   : a1, 2023-04-10, 4d
    Arches v7.3 Custom components      : a1, 2023-04-10, 4d
    section EAMENA v4
    Arches v7.3 tests                  : a1, 2023-04-17, 5d
    Arches v7.3 showcase               : a1, 2023-04-25, 1d
    Arches v7.3 public realease        : a1, 2023-05-09, 2023-10-01
```