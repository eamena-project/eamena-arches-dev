<p align="center">
  <img alt="img-name" src="www/APAAME_20211026_RHB-0705.png" width="300">
  <br>
    <em>APAAME_20211026_RHB-0705.DNG</em>
</p>



# Transfer of the APAAME archive to an ArcDAMS platform

The objective is to move the APAAME photographs archive stored on the [EAMENA NAS Server](https://eamena-nas1.arch.ox.ac.uk/cgi-bin/) to a dedicated NAS server hosting an ArcDAMS application (APAAME NAS Server).  

## Flickr images

In the IR, under the menu 'File Upload', paths to images are wrong. For example, with INFORMATION-0052511[^1], we have currently:

<p align="center">
  <img alt="img-name" src="www/img-err-path-a-INFORMATION-0052511.png" width="1000">
  <br>
    <em>Current Flickr path: `https:/live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg` </em>
</p>

Hover on the missing image gives this URL

<p align="center">
  <img alt="img-name" src="www/img-err-path-aa-INFORMATION-0052511.png" width="800">
  <br>
    <em>Hover value is: `database.eamena.org/live.staticflickr.com/4118/4928802850_49ed2fdbcb_o_d.jpg` </em>
</p>

Should be:

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

[link](doc/sql.md#id_catalog")

---

## Workflow

The workflow will be to:
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
  - a `Python script`, [apaame-metadata.py](https://github.com/eamena-project/eamena-arches-dev/blob/main/functions/Python/apaame-metadata.py), with the libraries `exifread` (for EXIF) and `pyavm` (for XMP), to extract metadata from :
  - a [folder](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/photos) containing one or more photographs
  - and save the metadata of these photographs in a [CSV file](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/metadata.csv).
  
## Notes

**EXIF and XMP metadata**

Here are examples of:
  -[EXIF output](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/exif_example.txt)  
  -[XMP output](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/apaame-photos/xmp_example.txt)  

**ArchDAMS app**

Application developed by Jeremy Worth (Oxford) on a pre-existing system. Used for [Manar-Al-Athar](http://www.manar-al-athar.ox.ac.uk) and [HEIR](http://heir.arch.ox.ac.uk/pages/home.php?login=true) images archives


[^1]: The APAAME ID is: `APAAME_20000906_RHB-0018.tif`