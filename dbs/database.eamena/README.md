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

1. Request a [Contributor user account](https://eamena.web.ox.ac.uk/open-access-policy#user-contributor) to add data directly into the database
2. Submit an unformated (your original dataset) or a formated dataset (a Bulk Upload) to the team

See the [License](https://eamena.org/database#data-use) and [Open Access policy](https://eamena.org/open-access-policy) on EAMENA website

### Contributor user account

See the [Contributor user account](https://eamena.web.ox.ac.uk/open-access-policy#user-contributor) on EAMENA website.

### Unformated and formated dataset

This is the Bulk Upload procedure, in any cases your dataset will have to be formated for the EAMENA database. The EAMENA team is currently developping a computer routine allowing to automatise the generation of ready-made citation for the different data subset (see ["How-to-cite"](https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bibref#readme)). For the moment, we suggest that you assign a DOI to your dataset (Zenodo, etc.) and publish it as a *data paper* in a specialised journal ([JOAD](https://openarchaeologydata.metajnl.com/), [IAJ](https://archaeologydataservice.ac.uk/about/the-internet-archaeology-journal/), etc.).
Before assigning a DOI to your dataset, and publishing it as a *data paper*, we suggest two routes:

1. **Unformated dataset** route: publish your dataset 'as-it-is', respecting only the FAIR guidelines. So, there is no need for you to reformat the columns, values, etc.
2. **Formated dataset** route: publish your dataset as a EAMENA-compliant dataset that can be uploaded directly into EAMENA via the Bulk Upload process. Following this route will improve the FAIRability of your data (sustainibility of our database, open-access, etc.)

In both cases, the EAMENA team will balance the effort needed to format your dataset into a EAMENA-compliant structure and the interest of you research for the endangered archaeology. If your dataset complies to EAMENA policies, we will:

* review your dataset
* make it properly citable





