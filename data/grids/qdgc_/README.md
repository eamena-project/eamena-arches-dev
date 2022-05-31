QDGC
====
> cloned from https://github.com/ragnvald/qdgc and adapted

This project supports the production and distribution of QDGC files. It provides a setup which allows for swift production of spatial data within a PostGIS database. It also provides tools to pull data off from the online database and into a geopackage file for distribution.

You will find tools and relevant templates in the folder [scripts](https://github.com/eamena-oxford/eamena-arches-dev/tree/main/data/grids/qdgc_/scripts) to produce PostGreSQL/PostGIS functions to create grids (with Psql and PL/Python)

## Initialise a PostGIS database and a spatial table

Initialize a default PostGIS database named `qdgc`
Create a spatial table `tbl_countries` with the boundaries of one or many countries (eg: https://geodata.lib.utexas.edu/catalog/stanford-pd162rb5652). This table should have a name column (`name`) which is being used for selecting the approprate country polygon.

## Create functions

Run the following scripts in a PostGIS database version 3.1 or above from the query tool
- `create_function_qdgc_getqdgc.sql`
- `create_function_qdgc_getlonlat.sql`
- `create_function_qdgc_getrecursivestring.sql`
- `create_function_qdgc_fillqdgc.sql`

## Calculate the grid

run a SQL command: `select qdgc_fillqdgc(`'*country_name*',*level*,*conseq*`);`
  
eg. `select qdgc_fillqdgc('Afghanistan',2,0);`

* *country_name*  
  
eg. Afghanistan

* *level*  
  
[1-5]: 1 means the produced table `tbl_qdgc` will be emptied before you run it. 2 is the scaled used by the [EAMENA DB](https://database.eamena.org/en/). 5 is the maximum QDGC level you want to produce.

* *conseg*  
  
If you want to do several consecutive queries the next queries will have to carry the argument 0.

# Creator notes

Why did I code these tools? Information on the distribution of animal populations is essential for conservation planning and management. Unfortunately, shared coordinate-level data may have the potential to compromise sensitive species and generalized data are often shared instead to facilitate knowledge discovery and communication regarding species distributions. Sharing of generalized data is, unfortunately, often ad hoc and lacks scalable conventions that permit consistent sharing at larger scales and varying resolutions. 

One common convention in African applications is the Quarter Degree Grid Cells (QDGC) system. However, the current standard does not support unique references across the Equator and Prime Meridian. We present a method for extending QDGC nomenclature to support unique references at a continental scale for Africa. 

The extended QDGC provides an instrument for sharing generalized biodiversity data where laws, regulations or other formal considerations prevent or prohibit distribution of coordinate-level information. We recommend how the extended QDGC may be used as a standard, scalable solution for exchange of biodiversity information through development of tools for the conversion and presentation of multi-scale data at a variety of resolutions. In doing so, the extended QDGC represents an important alternative to existing approaches for generalized mapping and can help planners and researchers address conservation issues more efficiently.
