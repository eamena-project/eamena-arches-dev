# APAAME archive
> Aerial Photographic Archive for Archaeology in the Middle East archive

Work in progress: [update EAMENA's Information Resources links to APAAME](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#update-ir-apaame-links) (from the [Flickr archive](https://www.flickr.com/photos/apaame/collections) to the new [ArchDAMS platform](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/README.md#archdams-server))

## Update IR-APAAME links
> batch the update of APAAME links

The aim is to embed previews of APAAME photographs (hosted on ArchDAMS) into EAMENA Information resources using ArchDAMS Direct links (i.e. external links). The  workflow is in ~~this Jupyter NB~~ this [Python script](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/apaame2eamena_1.py)

1. [Step 1](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#wf-step-1): in EAMENA, collect Information Resources UUIDs with their APAAME ID, store them in a dataframe (`A`)
2. [Step 2](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#wf-step-2): in ArchDAMS, collect APAAME ID and the Direct URL, store them in a dataframe (`B`)
3. [Step 3](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#wf-step-3): join the dataframe `A` and `B` on the APAAME ID
4. [Step 4](https://github.com/eamena-project/eamena-arches-dev/tree/main/projects/apaame#wf-step-4): update the EAMENA Postgres DB table with ArcDAMS external links

---

1. **Step 1** <a id="wf-step-1"></a>

`A` is EAMENA. Collect all IR having a Flickr link, using this [SQL statement](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/postgres/queries#23)

| IR UUID | APAAME ID |
|----------|----------|
| c712066a-8094-11ea-a6a6-02e7594ce0a0    |  APAAME_20000906_RHB-0018   |

gives this [eamena_fickr_paths](https://docs.google.com/spreadsheets/d/1gf27xtDZZKjjGOb0rUincZU56GW_LsRlWbPn-e3HpPs/edit?usp=sharing) table

2. **Step 2** <a id="wf-step-2"></a>

`B` is ArchDAMS

A reference number (sequential, from 1 to *n*) -- the ID of the resource[^2] -- is attributed to each photograph. Here **4** in <https://apaame.arch.ox.ac.uk/pages/download.php?ref=4&size=scr&noattach=true>

<p align="center">
  <img alt="img-name" src="www/rs-ex3-APAAME.png" width="500">
  <br>
    <em>ArchDAMS Direct URL https://apaame.arch.ox.ac.uk/pages/download.php?ref=4&size=scr&noattach=true</em>
</p>

[^2]: see the RS documentation: https://www.resourcespace.com/knowledge-base/api/get_resource_path

| Reference Number | APAAME ID |
|----------|----------|
| 4    |  APAAME_20000906_RHB-0018   |

A sample of the mapping table is this [metadata_export_contributions2_20240214-12_30.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv)[^3] file. Then, the Direct URL is a simple concatenation. For example, with the [reference number **4**](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv#L6)

| Direct URL | APAAME ID |
|----------|----------|
| https://apaame.arch.ox.ac.uk/pages/download.php?ref=4&size=scr&noattach=true   |  APAAME_20000906_RHB-0018   |

[^3]: previously [resource.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/resource.csv)

3. **Step 3** <a id="wf-step-3"></a>

Join APAAME [metadata_export_contributions2_20240214-12_30.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/metadata_export_contributions2_20240214-12_30.csv) with [eamena_fickr_paths](https://docs.google.com/spreadsheets/d/1gf27xtDZZKjjGOb0rUincZU56GW_LsRlWbPn-e3HpPs/edit?usp=sharing)

| APAAME ID | IR UUID | Direct URL |
|----------|----------|----------|
| APAAME_20000906_RHB-0018   | c712066a-8094-11ea-a6a6-02e7594ce0a0   | https://apaame.arch.ox.ac.uk/pages/download.php?ref=4&size=scr&noattach=true |

The result is [eamena_apaame_match.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/eamena_apaame_match.csv)

4. **Step 4** <a id="wf-step-4"></a>

Update the EAMENA Pg database:

- read the [eamena_apaame_match.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/eamena_apaame_match.csv) file, fields: `img_url`
- find the Flickr `img_url` value in the DB (ex: `https://live.staticflickr.com/7569/15784162651_852ef747a0_o_d.jpg`)
- replace the `img_url` value in Pg with ...

see [SQL queries](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/postgres/queries#apaame-and-archdams)

### Known issues

Currently in EAMENA, in the Information Resources (IR), under the menu 'File Upload', paths to images are wrong. For example, with INFORMATION-0052511[^1], we have currently:

<p align="center">
  <img alt="img-name" src="www/img-err-path-a-INFORMATION-0052511.png" width="1000">
  <br>
    <em>Current Flickr path: `https:/live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg` in the [Flickr archive](https://www.flickr.com/photos/apaame/collections)</em>
</p>

<a id="directlk-ok"></a>Should be:

<p align="center">
  <img alt="img-name" src="www/img-err-path-INFORMATION-0052511.png" width="1000">
  <br>
    <em>Correct Flickr path: `https://live.staticflickr.com/4118/4928802850_fbab90b8ca_h.jpg`</em>
</p>

The path root is the same, `https://live.staticflickr.com/4118/4928802850` the difference is between the last digits:

| | |
|---	|---	|
| **current**   	|  49ed2fdbcb_o_d.jpg 	|
| **correct**   	|  fbab90b8ca_h.jpg 	|

Hover on the missing image gives this URL

<p align="center">
  <img alt="img-name" src="www/img-err-path-aa-INFORMATION-0052511.png" width="800">
  <br>
    <em>Hover value is: `database.eamena.org/live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg` </em>
</p>

Let's consider the Information Resource - INFORMATION-0052511. It has two photographs linked:

* APAAME_20000906_RHB-0018
* SL00/4.33 (RHB) 

<p align="center">
  <img alt="img-name" src="www/img-imagery-catalogueid-INFORMATION-0052511.png" width="500">
  <br>
    <em>File Upolad</em>
</p>

Images paths are hosted here:

<p align="center">
  <img alt="img-name" src="www/img-fileupload-aa-INFORMATION-0052511.png" width="800">
  <br>
    <em>File Upolad. The UUID of the field 'File Upload' is: `c712066a-8094-11ea-a6a6-02e7594ce0a0`</em>
</p>

The current link of Information Resource - INFORMATION-0052511 is:

```HTML
<img data-bind="attr: { src: src, alt: alt }" src="/static/img/photo_missing.png" alt="">
```
<p align="center">
  <img alt="img-name" src="www/img-photomissing-INFORMATION-0052511.png" width="400">
  <br>
    <em>Photo missing</em>
</p>

The correct link (ie, external link) is:

```HTML
<img data-bind="attr: { src: src, alt: alt }" src="https://live.staticflickr.com/4118/4928802850_fbab90b8ca_h.jpg%60" alt="">
```

<p align="center">
  <img alt="img-name" src="www/img-photo-flickrurl-ok-INFORMATION-0052511.png" width="400">
  <br>
    <em>Flickr photo from its Direct URL/external link</em>
</p>

Looking in [this dataframe](https://docs.google.com/spreadsheets/d/1-shK3M3Pl5NANWWvGuSYTgjFNpJAyi-A6uf04a8WTkM/edit#gid=1837558986) (a sample of IR having Catalog ID recorded), there are different type of paths:

* `https://live.staticflickr.com...` to the Fickr archive: APAAME only
* `https://eamena-media.s3.amazonaws.com/files/...` to the AWS S3 bucket: ⌐ APAAME
* `https://eamena-uploads-v2.s3.amazonaws.com/...` to the AWS S3 bucket (also): ⌐ APAAME


* Notes

NO: https://www.flickr.com/photos/apaame/4928802850/  
NO: https://database.eamena.org/live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg  
YES: https://live.staticflickr.com/4118/4928802850_fbab90b8ca_h.jpg%60  
YES: https://apaame.arch.ox.ac.uk/pages/download.php?ref=4&size=scr&noattach=true 


### ArchDAMS server
> APAAME Server(*work in progress*)

ArchDAMS server, or APAAME server, is a QNAP NAS Server, hosting a customisation of ResourceSpace, a Digital Asset Management (DAM) system, named ArcDAMS.

#### URL

APAAME Server: https://apaame.arch.ox.ac.uk/

#### IT stack

|           |                   |
|-----------|-------------------|
| instance 	| ArcDAMS         	|
| software 	| ResourceSpace   	|
| hardware 	| QNAP NAS server 	|

#### Struture
> Photographs 

* By Country

#### Examples

##### Ex 1


<p align="center">
  <img alt="img-name" src="www/rs-ex1-APAAME_20081029_WKSHP-0095_JPG.png" width="1000">
  <br>
    <em>APAAME_20081029_WKSHP-0095</em>
</p>

#### Other

| APAAME ID 	| description 	| notes 	| local URL 	| EAMENA record |
|-----------	|-------------	|-------	|-----	|----- |
| APAAME_19970527_DLK-0190 	| Qasr el-Hallabat | reduced size	| https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/sample/APAAME_19970527_DLK-0190-small.tif  	| INFORMATION-0005901 |

#### Notes

##### DNG

DNG photographs (raw format) are not rendered in the ArcDAMS server

<p align="center">
  <img alt="img-name" src="www/rs-ex2-APAAME_20081029_DLK-0111_dng.png" width="300">
  <br>
    <em>DNG photographs are not rendered in the ArcDAMS server</em>
</p>

see: https://groups.google.com/g/resourcespace/c/wu9FNbbVBmo


### NAS server

EAMENA NAS Server: https://eamena-nas1.arch.ox.ac.uk/cgi-bin/

#### FHS 

The main folder `APAAME Master Catalog` has been copied in a external hardrive. Its file/folder hierachical structure (FHS) is as following:

<p align="center">
  <img alt="img-name" src="www/amc-fhs-ex1.png" width="800">
  <br>
    <em>Detail of the APAAME Master Catalog FHS (XLSX file) with a maximum depth of 6 subfolders (`level6`)</em>
</p>


see the [TSV file](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/amc-fhs.tsv) or download the [XLSX file itself](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/amc-fhs.xlsx)


---

# ~~Workflow~~

~~The workflow will be to:~~
> ⚠️ outdated, see how Jeremy is preparing this workflow

```mermaid
flowchart LR
    A[(EAMENA NAS Server)] --photographs--> B[photographs];
    subgraph local
    B --Python script--> C[metadata];
    end
    B --photographs--> D[(APAAME ArcDAMS server)];
    C --metadata--> D[(APAAME ArcDAMS server)]; 
```

The transfer process uses :
  - a `Python script`, [apaame-metadata.ipynb](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame/apaame-metadata.ipynb), with the libraries `exifread` (for EXIF) and `pyavm` (for XMP), to extract metadata from :
  - a [folder](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/photos) containing one or more photographs
  - and save the metadata of these photographs in a [CSV file](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/metadata.csv).
  
# Notes

**EXIF and XMP metadata**

Here are examples of:
  -[EXIF output](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/exif_example.txt)  
  -[XMP output](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/xmp_example.txt)  

**ResourceSpace**

It is a DAM (Digital Asset Management) application

**ArchDAMS app**

Application developed by Jeremy Worth (Oxford) on a pre-existing system. Used for [Manar-Al-Athar](http://www.manar-al-athar.ox.ac.uk) and [HEIR](http://heir.arch.ox.ac.uk/pages/home.php?login=true) images archives


[^1]: The APAAME ID is: `APAAME_20000906_RHB-0018.tif`