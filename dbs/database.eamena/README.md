# EAMENA DB


## Related Computer Applications



```mermaid
flowchart LR
  subgraph Arches v7
    subgraph EAMENA
    ea[(Eamena v4)]
    end
    subgraph [<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/internationalisation'>internationalisation</a>]
      id6[<a href='https://github.com/eamena-project/arches/blob/master/arches/locale/ar/LC_MESSAGES/django.po'>ar</a>];
      id7[<a href='https://github.com/eamena-project/arches/blob/master/arches/locale/fr/LC_MESSAGES/django.po'>fr</a>];
    end 
  end
  id3[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/geoserver'>GeoServer</a>] --- ea;
  id3 --- id4[<a href='https://github.com/eamena-project/eamena-arches-dev/tree/main/gis/qgis'>QGIS</a>];
  ea --- id5[<a href='https://github.com/eamena-project/eamenaR'>eamenaR</a>];
  ea --- internationalisation
```



