# EAMENA DB
> EAMENA v4 on Arches v7.4

[reference data](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data)


## Diagram

<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.14.0/mermaid.min.js"></script>
<h2>FlowChart</h2>
<div class="mermaid">
  graph LR
  A -- text --> B --> Stackoverflow -- msg --> myLabel2
  click Stackoverflow "https://stackoverflow.com/" "some desc when mouse hover" _blank
  click myLabel2 "https://stackoverflow.com/" "some desc when mouse hover"
</div>

<h2>classDiagram</h2>
<div class="mermaid">
  %% https://github.com/mermaid-js/mermaid/blob/cbe3a9159db4d5e67d270fe701cd63de1510f6ee/docs/directives.md?plain=1#L10-L48
  %%{init: {'theme': 'forest'}}%%
  classDiagram
    class myCls {
      attr type
      method()
    }
    %% ↓ must set: securityLevel=loose %% default para: clsID
    click myCls call myFunc() "desc."

    class myCls2
    click myCls2 call myFunc('hello world') "desc."

    class myClsUseLink {
      +field1
    }

    link myClsUseLink "https://www.github.com" "This is a link"
</div>

<h2>Gantt</h2>
<div class="mermaid">
  gantt
  dateFormat HH:mm
  axisFormat %H:%M
  try to click me : gotoSO, 19:00, 5min
  %% click : debug, after gotoSO,  5min  --> error, click is "keyword"
  clickMe : debug, after gotoSO,  5min
  endNode : milestone, m, 20:00, 0min
  click gotoSO href "https://stackoverflow.com/"
  click debug call myFunc()
  %% NOTE: not working on github
</div>

<script>
  mermaid.initialize({
    securityLevel: 'loose', // strict, loose, antiscript, sandbox // // https://github.com/mermaid-js/mermaid/blob/b141f24068e9c5f6979706383a29db6380ffdf31/docs/usage.md?plain=1#L114-L117
  });

  function myFunc(arg) {
    console.log(arg)
  }
</script>

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
      direction TB
      id9A -- Bulk Upload formatting --> id9B[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/data/bulk#readme'>BU</a>];
      id9B -- Bulk Upload --> ea;
      ea -- Bulk Retrieve --> id9B;
    end
  end
  subgraph eamena-functions
    direction LR
    subgraph functions
      idf1[<a href='https://github.com/eamena-project/eamena-functions/blob/main/mds/mds.py'>mds.py</a>]
    end
    subgraph Jupyter NB
      idf2[<a href='https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb'>citation_generator.ipynb</a>] -- read --> idf1
    end
  end
  subgraph Google Colab
    idg1[<a href='https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb'>citation_generator.ipynb</a>] -- is mirrored --> idf2
  end
  ea -- <a href='query#url'>GeoJSON URL</a> --> idf1
  ea --- id5[<a href='https://github.com/eamena-project/eamenaR'>eamenaR</a>];
  ea --- internationalisation
  ea <--- install
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

