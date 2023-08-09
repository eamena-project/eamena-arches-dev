# Installation
> Installation, upgrade and migration

## EAMENA 4 Install Docs

In progress. For now, see [Arches 7 Upgrade](notes/Arches%207%20Upgrade.md). 

These docs describe the process of (a) installing an empty EAMENA-customised version of Arches 7.3, and (b) copying the data from an old EAMENA v3 (Arches v5.2) instance to the new database.

### Prerequisites

Arches 7.3 requires Elasticsearch [8.3.3](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb) and PostgreSQL 14 to be installed. Additionally, Arches 7 requires NPM 8.19.3 or 9.6.0 (tested and works with both), Yarn 1.22.19 and Node.JS 14.17.6. The instructions for installing and configuring all of these are linked from below.

Install:

* [PostgreSQL 14](prerequisites/PostgreSQL.md)
* [Elasticsearch 8.3.3](prerequisites/Elasticsearch.md)
* [NodeJS / NPM / Yarn](prerequisites/Yarn.md)
* [Celery](prerequisites/Celery.md)
* [Apache](prerequisites/Apache.md)

### Install Paths

Once the VM is configured correctly, follow the flow chart below in order to 

Paths to/from the various Arches/EAMENA incarnations.

```mermaid
flowchart
	id1((Eamena v3))-->id2[Export data as JSONL]
	id2-->id3[Split into chunks]
	id3-->id4[Convert JSONL to JSON]
	id4-->id5{Full EAMENA data}
	id5-->id6[IMPORT]
	id7[ <a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/install#install-empty-arches-v7'> Install empty Arches v7 </a>]-->id25[ <a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/install#install-eamena-customisations'>Install EAMENA customisations</a> ]
	id25-->id8{Empty Arches v7}
	id9[Clone EAMENA from Github]-->id8
	id8-->id6
	id6-->id10{Unindexed EAMENA v4}
	id10-->id11[Duplicate PostGreSQL DB]
	id10-->id12[INDEX]
	id12-->id13((Eamena v4))
	id2-->id14[Remove un-needed data]
	id6-->id15{Unindexed full clone}
	id11-->id15
	id15-->id16[INDEX]
	id16-->id17((Full Clone))
	id18{Unindexed partial clone}-->id19[INDEX]
	id19-->id20((Partial Clone))
	id14-->id21[Convert JSONL to JSON]
	id21-->id22{Partial EAMENA data}
	id15-->id23[Remove un-needed data]
	id8-->id24[IMPORT]
	id22-->id24
	id23-->id18
	id24-->id18
	style id1 fill:#CFFFCF
	style id2 fill:#CFFFCF
	style id3 fill:#CFFFCF
	style id4 fill:#CFFFCF
	style id5 fill:#CFFFCF
	style id6 fill:#CFCFFF
	style id7 fill:#CFFFCF
	style id8 fill:#CFFFCF
	style id9 fill:#FFFFFF
	style id10 fill:#CFCFFF
	style id11 fill:#FFFFFF
	style id12 fill:#CFCFFF
	style id13 fill:#CFCFFF
	style id14 fill:#FFFFFF
	style id15 fill:#FFFFFF
	style id16 fill:#FFFFFF
	style id17 fill:#FFFFFF
	style id18 fill:#FFFFFF
	style id19 fill:#FFFFFF
	style id20 fill:#FFFFFF
	style id21 fill:#FFFFFF
	style id22 fill:#FFFFFF
	style id23 fill:#FFFFFF
	style id24 fill:#FFFFFF
	style id25 fill:#CFFFCF
```

## Install empty Arches v7

```Bash
sudo apt-get install python3-psycopg2
sudo apt-get install libpq-dev
```

Install the Arches Python package:

```Bash
python -m pip install "arches==7.3"
```

## Install EAMENA customisations

From the `arches/` folder, run:

```Bash
git clone https://github.com/eamena-project/eamena.git
```

## Others

* [Cloning EAMENA from Github](install/Clone.md)

| Task | 3->5 | 5->7 |
|------|-------|-------|
| Export data structures from old database  | Up | Up |
| Install new version of Arches on a test box  | Up | Up |
| Develop/convert data structures in new database  | Up | Up |
| Develop/convert EAMENA customisations  | Up | Up |
| Export a subset of data from old database  | Down | Up |
| Determine changes to be made to data  | Down | Up |
| Write automated scripts to convert data  | Down | Up |
| Convert a subset of data using test script  | Down | Up |
| Install correct version of Python, Django, PostgreSQL, etc | Down | Up |
| Install new database on AWS   | Down | Up |
| Install new data structures into new database  | Down | Up |
| Apply EAMENA customisations to the database  | Down | Up |
| Export complete data from old database (test run) | Down | Up |
| Import complete data into new database (test run) | Down | Up |
| Export complete data from old database   | Down | Down |
| Import complete data into new database   | Down | Down |
| Perform the 'switch' (eg server certificates, domain name, etc)   | Down | Down |


### Still to do (2023-05-09)

#### If time isn't tight
* Upgrade to 7.4 (currently 7.3)
* A few more partial export/imports using the AWS server.
* Some heavy stress testing


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