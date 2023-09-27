# Dev

Scheduled IT developments for the EAMENA DB and miscellaneous. Test on [EA training instance](https://github.com/eamena-project/eamena-arches-dev/tree/main/dev#instance-ea)

## Instance

### EA
> EA training instance

```
Host EA-training-instance
  HostName 34.244.241.250
  IdentityFile "C:/Users/Thomas Huet/Desktop/EAMENA/IT/keys/EA_training.pem"
  User ubuntu
```

## Arches

### Card permission

*expected behaviour*: hide coordinates to Guest users withou hiding the map (zoom-in can be limited)

see: https://community.archesproject.org/t/card-permission/1675/1

## Postgres

### DB Read (only)

*expected behaviour*: give users access to query the Postgres database using functions [eamenaR](https://github.com/eamena-project/eamenaR#eamenar-) package in READ only mode ([example](https://github.com/eamena-project/eamenaR/blob/107bd73656180f34c06880df36ea5aa601f859b5/R/ref_hps.R#L75-L107))

*hints*: create Postgres views, change the Potgres default configuration file (renammed) [pg_hba_old.conf](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/postgres/pg_hba_old.conf) to a new file [pg_hba.conf](https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/postgres/pg_hba.conf). 

see: https://community.archesproject.org/t/give-access-to-a-custom-postgresql-view/1900/1

---

## Spatial

Development on Mapbox

### Clusters

#### Cluster zooming

*expected behaviour*: after clicking on a cluster, this cluster explode and there's an automatic zoom-in to its minimum bound rectangle. The behaviour we expect is similar to Arches v3

see: https://community.archesproject.org/t/mapbox-cluster-zooming/1964


#### Cluster of Clusters

*expected behaviour*: group in cluster or explode clusters depending on zoom-in zoom-ou

<p align="center">
  <img src="../www/arches-v7-dev-mapbox-ClustOfClust.gif" width="600">
  <br>
    <em>caption</em>
</p>

see: https://community.archesproject.org/t/mapbox-cluster-grouping/1999/1


### Reverse geocoding

*expected behaviour*: be able to find a place (zoom-in) from its coordinates 

<p align="center">
  <img src="../www/arches-v7-dev-mapbox-revgeocod.gif" width="300">
  <br>
    <em>caption</em>
</p>

see: https://community.archesproject.org/t/reverse-geocoding-zoom-in-from-coordinates/1852

### search by different type of coordinates


<p align="center">
  <img src="../www/megaj-search-coordinates.png" width="500">
  <br>
    <em>caption</em>
</p>

### Collect the coordinates

*expected behaviour*: on a click in the map, lon/lat coordinates of the point are shown in the bottom-right or bottom-left of the map and can be copied in the clipboard

---


## BU exchanges

[Bulk Upload](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk) exchanges. Objectives are:

- [1️)](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#eamena-%EF%B8%8F-eamena-workflow) facilitate the edition of already existing data in the EAMENA DB;
- [2)](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#eamena-%EF%B8%8F-other-db-workflow) exchange data between EAMENA and national instances BDs;

### EAMENA ↔️ EAMENA workflow

For selected HPs

```mermaid
flowchart RL
    A[(EAMENA Arches v7)] --1. export data as BU--> B[XLSX];
    A --3. remove data--> A;
    subgraph local
    B --2. edit data--> B;
    end
    B --4. re-import--> A;
```

### EAMENA ↔️ Other DB workflow

To exchange data between different Arches-based databases (eg: Mega-J once this database has been ported to Arches v7), the workflow will be to:

```mermaid
flowchart LR
    A[(EAMENA Arches v7)] --export as BU--> B[XLSX BU];
    C[(Mega-J Arches v7)] --export as BU--> D[XLSX BU];
    B --> E[XLSX BU merged];
    D --> E;
    E --check duplicated--> E;
```

In this example, the merged XLSX dataset will be sorted and/or filtered by toponyms, coordinates, or any relevant fields to group rows refering to the same HPs. Then two cases can occur:

1. total matching/perfect duplicates: one of them is removed
2. partial matching: the *n* rows are merged in a single record (ie, with the same UNIQUEID), like this (see ID 5):

<div align = "center">

| UNIQUEID | Assessment.Investigator.-.Actor | Investigator.Role.Type   | Assessment.Activity.Type | Assessment.Activity.Date | GE.Assessment(Yes/No) | Resource.Name | Name.Type             |
|----------|---------------------------------|--------------------------|--------------------------|--------------------------|-----------------------|---------------|-----------------------|
| ...      | ...                             | ...                      | ...                      | ...                      | ...                   | ...           | ...                   |
| 4        | Mohamed Kenawi                  | EAMENA Project Staff     | Desk-based Assessment    | 2022-10-05               | Yes                   |               |                       |
| 5        | Martin Sterry                   | **MEGA-J Project Staff** |                          | 2028-09-12               |                       | AAA f.37.5    | Alternative Reference |
| 5        | Mohamed Kenawi                  | **EAMENA Project Staff** | Desk-based Assessment    | 2022-10-05               | Yes                   | Metkaouak     | Toponym               |
| ...      | ...                             | ...                      | ...                      | ...                      | ...                   | ...           | ...                   |

Example of a merged XLSX BU record resulting from the merge of EAMENA (bolded) and Mega-J (bolded) BUs

</div>

Once done, the merged BU will be returned to the databases.

```mermaid
flowchart LR
    E[XLSX BU merged] -- back to EAMENA --> A[(EAMENA Arches v7)];
    E -- back to Mega-J --> C[(Mega-J Arches v7)];
```


---

## Images

Restore the path of images

<p align="center">
  <img alt="img-name" src="../www/images-uploaded-error.png" width="700">
  <br>
    <em>caption</em>
</p>
  
example: Search INFORMATION-0104667

---

## Audit

### Basic statistics

Translate Ash's statistics https://mareastats.drashsmith.com/ from PHP to Python

<p align="center">
  <img alt="img-name" src="../www/audit-data-sums.png" width="400">
  <br>
    <em>EAMENA DB statistics</em>
</p>

### Data quality

Check the completness of data. Python function to model the quality of HP with a radar diagram based on the groups appearing in the BU file (different levels of data agregation and summing):

| | | |
|-|-|-|
|ASSESSMENT SUMMARY| |Assessment Investigator - Actor|
| | |Investigator Role Type|
| |ASSESSMENT ACTIVITY|Assessment Activity Type|
| | |Assessment Activity Date|
| | |GE Assessment(Yes/No)|
| | |GE Imagery Acquisition Date|
| | |Information Resource Used|
| | |Information Resource Acquisition Date|
|RESOURCE SUMMARY|RESOURCE NAME|Resource Name|
| | |Name Type|
| | |Heritage Place Type|
| |RESOURCE DESCRIPTION|General Description Type|
| | |General Description|
| |HERITAGE RESOURCE CLASSIFICATION|Heritage Place Function|
| | |Heritage Place Function Certainty|
| |DESIGNATION|Designation|
| | |Designation From Date|
| | |Designation To Date|
|GEOMETRIES| |Geometric Place Expression|
| | |Geometry Qualifier|
| | |Site Location Certainty|
| | |Geometry Extent Certainty|
|GEOGRAPHY| |Site Overall Shape Type|
| | |Grid ID|
| | |Country Type|
| | |Cadastral Reference|
| | |Resource Orientation|
| |ADDRESS|Address|
| | |Address Type|
| |ADMINISTRATIVE SUBDIVISION|Administrative Subdivision|
| | |Administrative Subdivision Type|
|ARCHAEOLOGICAL ASSESSMENT| |Overall Archaeological Certainty Value|
| | |Overall Site Morphology Type|
| |PERIODIZATION|Cultural Period Type|
| | |Cultural Period Certainty|
| | |Cultural Subperiod Type|
| | |Cultural Subperiod Certainty|
| | |Date Inference Making Actor|
| |ABSOLUTE CHRONOLOGY|Archaeological Date From (cal)|
| | |Archaeological Date to (cal)|
| | |BP Date From|
| | |BP Date To|
| | |AH Date From|
| | |AH Date To|
| | |SH Date From|
| | |SH Date To|
| |SITE FEATURES & INTERPRETATIONS|Site Feature Form Type|
| | |Site Feature Form Type Certainty|
| | |Site Feature Shape Type|
| | |Site Feature Arrangement Type|
| | |Site Feature Number Type|
| | |Site Feature Interpretation Type |
| | |Site Feature Interpretation Number|
| | |Site Feature Interpretation Certainty|
| | |Built Component Related Resource|
| | |HP Related Resource|
| |MATERIAL|Material Class|
| | |Material Type|
| | |Construction Technique|
| |Measurements|Measurement Number|
| | |Measurement Unit|
| | |Dimension Type|
| | |Measurement Source Type|
| | |Related Geoarch/Palaeo|
|CONDITION ASSESSMENT| |Overall Condition State|
| | |Damage Extent Type|
| |DISTURBANCES|Disturbance Cause Category Type|
| | |Disturbance Cause Type|
| | |Disturbance Cause Certainty|
| | |Disturbance Date From|
| | |Disturbance Date To|
| | |Disturbance Date Occurred Before|
| | |Disturbance Date Occurred On|
| | |Disturbance Cause Assignment Assessor Name|
| | |Effect Type|
| | |Effect Certainty|
| |THREATS|Threat Category|
| | |Threat Type|
| | |Threat Probability|
| | |Threat Inference Making Assessor Name|
| |RECOMMENDATION PLAN|Intervention Activity Type|
| | |Recommendation Type|
| | |Priority Type|
| | |Related Detailed Condition Resource|
|ENVIRONMENT ASSESSMENT| |Topography Type|
| |LAND COVER|Land Cover Type|
| | |Land Cover Assessment Date|
| |SURFICIAL GEOLOGY|Surficial Geology Type|
| | |Depositional Process|
| | |Bedrock Geology|
| |MARINE ENVIRONMENT|Fetch Type|
| | |Wave Climate|
| | |Tidal Energy|
| |DEPTH/ELEVATION|Minimum Depth/Max Elevation(m)|
| | |Maximum Depth/Min Elevation(m)|
| | |Datum Type|
| | |Datum Description/EPSG code|
|ACCESS| |Restricted Access Record Designation|

Create a GUI in <https://colab.research.google.com/>, or equivalent, to let a user request on a UUID (HP's uuid, or BU's uuid)

~~https://github.com/eamena-project/eamena-arches-5-project/blob/master/eamena/statistics/hr_quality_rec.py~~
