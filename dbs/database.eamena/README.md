# EAMENA DB

## Diagram

```mermaid
flowchart LR
  subgraph Arches v7
    subgraph EAMENA DB
    ea[(Eamena v4)]
    end
    subgraph internationalisation
      id6[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/internationalisation'>ar</a>];
      id7[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/internationalisation'>fr</a>];
    end 
    subgraph install
      id8[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/install'>install<br>upgrade<br>migrate</a>];
    end 
  end
  id3[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/geoserver'>GeoServer</a>] --- ea;
  id3 --- id4[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/gis/qgis'>QGIS</a>];
  subgraph local
    direction TB
    subgraph unformated data
      id9A[dataset]
    end
    subgraph formated data
      id9A -- format to Bulk Upload --> id9B[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#readme'>Bulk Upload</a>]
      id9B ---> ea;
    end
  end
  ea --- id5[<a href='https://github.com/eamena-project/eamenaR'>eamenaR</a>];
  ea --- internationalisation
  ea <--- install
```

## Contribute to the EAMENA database

There is two ways to add data to the database:

1. Request a [Contributor user account](#contributor-user-account) to add data directly into the database using the graphical user interface <https://database.eamena.org/>. See the [Contributor user account](https://eamena.web.ox.ac.uk/open-access-policy#user-contributor) on EAMENA website.
2. Submit an [unformated or formated dataset](#unformated-or-formated-dataset) in a form of a TSV, CSV or XLSX file, to the team

See the [License](https://eamena.org/database#data-use) and [Open Access policy](https://eamena.org/open-access-policy) on EAMENA website
### Unformated or formated dataset

If you want to host and expose an already prepared dataset, the latter will have to be formated for the EAMENA database: this is the [Bulk Upload procedure](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#readme). Before assigning a DOI to your dataset, and publishing it as a *data paper*, we suggest two routes:

#### **Unformated dataset** route

An unformated is our original dataset 'as-it-is', as you published it under its DOI, in data paper journal, etc., respecting only the FAIR guidelines. So, there is no need for you to reformat the columns, values, etc. You submit your dataset directly to the EAMENA team. In this case, the EAMENA team will balance the effort needed to format your dataset into a EAMENA-compliant structure and the interest of you research for the endangered archaeology *a posteriori*

#### **Formated dataset** route

A formated dataset is a Bulk Upload form, that is to say, a EAMENA databae-compliant dataset that can be uploaded directly into EAMENA via the Bulk Upload process. Following this route will improve the FAIRability (sustainibility of our database, open-access, etc.). Indeed, the process of making your compliant can already be mentioned in your *data paper* (see, and reuse, this [JOAD template](https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bibref/templates/template_joad.md)). In this case, the EAMENA team will balance the effort needed to format your dataset into a EAMENA-compliant structure and the interest of you research for the endangered archaeology *a priori*.

---

The EAMENA team is currently developping a computer routine allowing to automatise the generation of ready-made citation for the different data subset (see ["How-to-cite"](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#readme)). For the moment, we suggest that you assign a DOI to your dataset (Zenodo, etc.) and publish it as a *data paper* in a specialised journal ([JOAD](https://openarchaeologydata.metajnl.com/), [IAJ](https://archaeologydataservice.ac.uk/about/the-internet-archaeology-journal/), etc.).





