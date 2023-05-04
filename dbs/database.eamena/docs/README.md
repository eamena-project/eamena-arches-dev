# EAMENA 4 Install Docs

In progress. For now, see [Arches 7 Upgrade](notes/Arches%207%20Upgrade.md). 

These docs describe the process of (a) installing an empty EAMENA-customised version of Arches 7.3, and (b) copying the data from an old EAMENA v3 instance to the new database.

## Prerequisites

Arches 7.3 requires Elasticsearch [8.3.3](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb) and PostgreSQL 14 to be installed. Additionally, Arches 7 requires NPM 8.19.3 or 9.6.0 (tested and works with both), Yarn 1.22.19 and Node.JS 14.17.6. The instructions for installing and configuring all of these are linked from below.

* [Install PostgreSQL 14](prerequisites/PostgreSQL.md)
* [Install Elasticsearch 8.3.3](prerequisites/Elasticsearch.md)
* [Install NodeJS / NPM / Yarn](prerequisites/Yarn.md)

## Install Paths

Once the VM is configured correctly, follow the flow chart below in order to 

Paths to/from the various Arches/EAMENA incarnations.

```mermaid
flowchart
	id1((Eamena v3))-->id2[Export data as JSONL]
	id2-->id3[<a href='notes/Arches%207%20Upgrade.md#splitchunk'>Split into chunks</a>]
	id3-->id4[Convert JSONL to JSON]
	id4-->id5{Full EAMENA data}
	id5-->id6[IMPORT]
	id7[Install empty Arches v7]-->id25[Install EAMENA customisations]
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
	click id9 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/docs/install/Clone.md" "Clone EAMENA from Github" _blank
```

* [Cloning EAMENA from Github](install/Clone.md)




