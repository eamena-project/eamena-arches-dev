# City of the Dead
> *aka* Cairo project, *aka* CoD, Unknown Heritage in the 'City of the Dead', DOCUMENTATION OF THE UNREGISTERED HERITAGE OF THE EASTERN CEMETERY IN CAIRO

## Aims

Uploading an existing database into EAMENA v4

## CoD data

<p align="center">
  <img alt="img-name" src="./www/record-ex.png" width="600">
  <br>
    <em>Detail of a CoD's project record</em>
</p>

## CoD database

A Microsoft Access DB. Once exported the tables are handled and their data re-organised using the [read_cod_tables.R](read_cod_tables.R) script

## CoD to EAMENA

CoD records gather informations that will belong both to EAMENA Heritage Places (HP, [example](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/cod/business_data/hp.csv)) and EAMENA Built Components (BC, [example](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/cod/business_data/bc.csv)). For each CoD record there is two kinds of data:

1. Textual data
2. Photographs

## Textual data

* solution

1. Values: Map CoD's values to those used in EAMENA (controled vocab), see for example [condition.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/cod/reference_data/condition.csv)

2. For a BU Upload (HP Fields): Map correspondances between CoD's project DB fieldnames with EAMENA field names, using the [mapping correspondance table](https://github.com/eamena-project/eamenaR#mapping-file) (fields: `cairo` and `cairo_type`)

<p align="center">
  <img alt="img-name" src="./www/mapping-ex.png" width="700">
  <br>
    <em>Alignement 'source' (columns `cairo` and `cairo_type`) and 'target'</em>
</p>

3. Run the [list_mapping_bu()](https://eamena-project.github.io/eamenaR/doc/list_mapping_bu) function


## Photographs

### Metadata

Match the photographs metadata with the photographs themselves

<p align="center">
  <img alt="img-name" src="./image-1.png" width="700">
  <br>
    <em>Screenshot of the 'photo' table export (`photo.xlsx`) with the metadata of the photograph DSC_2643s.jpg highlighted</em>
</p>

<p align="center">
  <img alt="img-name" src="./image-2.png" width="500">
  <br>
    <em>Screenshot of the DSC_2643s.jpg photograph</em>
</p>


### Hosting

- Manar-al-Athar (ResourceSpace / ArchDAMS server)

### TODO

Importing each photograph as an Information Resource (IR)


<*to be discussed*>


