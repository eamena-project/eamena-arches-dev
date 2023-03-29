# EAMENA DB

## Timeline

DB migration process and trainings

```mermaid
gantt
    title EAMENA v4 Arches v7 training
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%m-%y
    tickInterval 7day
    section EAMENA v3
    Arches v5.2              : a0, 2023-01-01, 2023-04-24
    Arches v5.2 stopped      : milestone, m3, 2023-04-24, 1d
    section EAMENA v3 -> v4
    Arches v7.3 DB installation        : a1, 2023-03-06, 2d
    Arches v7.3 Graphs installation    : a1, 2023-03-06, 2d
    Arches v7.3 Data                   : a1, 2023-04-10, 4d
    Arches v7.3 Custom components      : a1, 2023-04-10, 4d
    section EAMENA v4
    Arches v7.3 tests                  : a1, 2023-04-17, 5d
    Arches v7.3 showcase               : a1, 2023-04-25, 1d
    Arches v7.3 public realease        : a1, 2023-05-02, 2023-10-01
    section Remote training 1
    Materials development     : a1, 2023-04-10, 4d
    Online delivery           : a1, 2023-04-15, 6d
    section In-person training
    KRG training             : a1, m3, 2023-05-09, 7d
    IST training             : a1, 2023-06-05, 7d
    AMM training             : a1, 2023-06-17, 2023-06-22

```
