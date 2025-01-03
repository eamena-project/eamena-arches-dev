# EAMENA DB
> EAMENA v4 on Arches v7.4, `database.eamena.org`


This `database.eamena` folder contains data on the online [database.eamena.org](https://database.eamena.org/) DB: [plugins dev and documentation](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/citation), [customization templates](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/custom), [data management processes](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data) and [reference data](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data), 
) [internationalisation (i18n)](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/i18n), [installation guidelines](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/install), [postgres backend and queries](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/postgres), [users permission tiers](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/users).


## Diagram

```mermaid
flowchart
  subgraph Arches v7
    subgraph EAMENA DB
      ea[(Eamena v4)];
      subgraph reference-data
        idr1[ERD];
        idr2[MDS];
        idr3[Fields, groups<br>and values];
      end
    end
    subgraph internationalisation
      id6[ar];
      id7[fr];
    end 
    subgraph install
      id8[install<br>upgrade<br>migrate];
    end 
  end
  id3[GeoServer] --- ea;
  id3 --- id4[QGIS];
  subgraph local
    direction TB
    subgraph unformated data
      id9A[dataset]
    end
    subgraph formated data
      direction TB
      id9A -- Bulk Upload formatting --> id9B[BU];
      id9B -- Bulk Upload --> ea;
      ea -- Bulk Retrieve --> id9B;
    end
  end
  subgraph eamena-functions
    direction LR
    subgraph functions
      idf1[mds.py]
    end
    subgraph Jupyter NB
      idf2[citation_generator.ipynb] -- read --> idf1
    end
  end
  subgraph Google Colab
    idg1[citation_generator.ipynb] -- is mirrored --> idf2
  end
  ea -- GeoJSON URL --> idf1
  ea --- id5[eamenaR];
  ea --- internationalisation
  ea --- reference-data
  ea <--- install

  click idr1 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#erd" _blank
  click idr2 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#mds" _blank
  click idr3 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data#groups-of-fields-fields-and-field-values-descriptions" _blank
  click id6 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/internationalisation" _blank
  click id7 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/internationalisation" _blank
  click id8 "https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/install" _blank
  click id3 "https://github.com/eamena-project/eamena-arches-dev/tree/main/geoserver" _blank
  click id4 "https://github.com/eamena-project/eamena-arches-dev/tree/main/gis/qgis" _blank
  click idf1 "https://github.com/eamena-project/eamena-functions/blob/main/mds/mds.py" _blank
  click idf2 "https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb" _blank
  click idg1 "https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb" _blank
  click id5 "https://github.com/eamena-project/eamenaR" _blank
  click id9B "https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#readme" _blank
```


## Contribute to the EAMENA database

There is two ways to add your data to the database:

1. Request a [*Contributor* user account](https://eamena.web.ox.ac.uk/open-access-policy#user-contributor) to add data directly into the database using the graphical user interface <https://database.eamena.org/>.
2. Submit an [unformated or formated dataset](#unformated-or-formated-dataset) in a form of a TSV, CSV or XLSX file, to the team

If you aim to submit your data to EAMENA as an [unformated or formated dataset](#unformated-or-formated-dataset), .

### Unformated or formated dataset

If you want to host a dataset on EAMENA, this dataset will have first to be formated for the EAMENA database: this is the [Bulk Upload procedure](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#readme). The EAMENA team will evaluate the interest of your data for the research on endangered archaeology and, if your dataset need to be reformat into a EAMENA-compliant structure ("unformated dataset"), the effort needed to prepare your dataset.
Alongside with your data you will create an **Information Resource** referencing your dataset. 

<p align="center">
  <img alt="img-name" src="../../www/arches-ea-v4-rm.png" width="250">
  <br>
    <em>Create a new resource in the Ressource Model <b>Information Resource</b>, see for example: <a href = "https://github.com/eamena-project/eamena-arches-dev/blob/main/www/arches-ea-v4-rm-ir-ex2.pdf">GlobalKites ANR project</a></em>
</p>

Before assigning a DOI to your dataset, and maybe publishing it as a *data paper*, we suggest two routes:

#### **Unformated dataset** route

An "unformated dataset" is our original dataset 'as-it-is', as you published it under its DOI ([Zenodo](https://zenodo.org/), [OSF](https://help.osf.io/article/220-create-dois), [Inist-CNRS](https://www.inist.fr/nos-actualites/datacite-accompagne-doi/), etc.), in *data paper* journal ([JOAD](https://openarchaeologydata.metajnl.com/), [IAJ](https://archaeologydataservice.ac.uk/about/the-internet-archaeology-journal/), etc.), etc., respecting only the FAIR guidelines. 

There is no need for you to align the columns names, map the values, etc. with the EAMENA format. You submit your dataset directly to the EAMENA team. 

#### **Formated dataset** route

A "formated dataset" is a Bulk Upload form, that is to say, a EAMENA databae-compliant dataset that can be uploaded directly into EAMENA via the Bulk Upload process. Following this route will improve the FAIRability[^1]. Indeed, making your compliant to a open-access and open-source database and long term repository using CIDOC-CRM onlogy[^2] can already be mentioned in your *data paper* (see, improve and reuse, this [JOAD template](https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bibref/templates/template_joad.md)).

You will need to align the columns names, map the values, etc., with the EAMENA format. We can provide tools (see the [eamaneR](https://github.com/eamena-project/eamenaR#bu) pakage) and help to make this process as simple and easy as possible.

---

Our team is currently developping a computer routine allowing to automatise the generation of ready-made citation for the different data subset (see ["How-to-cite"](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#readme)). For the moment, we suggest that you assign a DOI to your dataset (Zenodo, etc.) and publish it as a *data paper* in a specialised journal ([JOAD](https://openarchaeologydata.metajnl.com/), [IAJ](https://archaeologydataservice.ac.uk/about/the-internet-archaeology-journal/), etc.). See also the [License](https://eamena.org/database#data-use) and [Open Access policy](https://eamena.org/open-access-policy) on EAMENA website


[^1]: Findable, Accessible, Interoperable, Reusable. See <https://www.go-fair.org/>
[^2]: CIDOC Conceptual Reference Model is the ISO 21127:2014. See: <https://www.cidoc-crm.org/>

