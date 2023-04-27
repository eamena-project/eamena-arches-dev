Paths to/from the various Arches/EAMENA incarnations.

```mermaid
flowchart
	id1((Eamena v3))-->id2[Export data as JSONL]
	id2-->id3[Split into chunks]
	id3-->id4[Convert JSONL to JSON]
	id4-->id5{Full EAMENA data}
	id5-->id6[IMPORT]
	id7[Install empty Arches v7]-->id8{Empty Arches v7}
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
	
```
