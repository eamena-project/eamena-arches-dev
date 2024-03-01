# i18n
> Internationalisation

## Convert thesauri
> ⚠️ the `skos2excel.py` file should be run on Collections (`collections.xml`), not on thesauri

Example for the EAMENA.xml file, and translation to French (`fr`), using the [skos2excel](https://github.com/ads04r/skos2excel) tools

1. Convert [EAMENA.xml](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml) to [EAMENA_fr.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.xlsx) (See the corresponding [TSV file](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.tsv)) using the `skos2excel.py` script:

```sh
py skos2excel.py ./data/EAMENA.xml ./data/EAMENA_fr.xlsx -lang fr -f xlsx 
```

Proofreading of the automtic translation. 

2. Convert (back) the [EAMENA_fr.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.xlsx) concepts to [EAMENA_fr.xml](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr.xml) using the `excel2skos.py` script:

```sh
py excel2skos.py ./data/EAMENA_fr.xlsx ./data/EAMENA_fr.xml -b ./data/EAMENA.xml
```

3. On the DB 

* SSH, backend:

Change directory

```sh
cd /opt/arches/eamena/eamena/pkg/reference_data/concepts
```

Import from GitHub

```sh
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr.xml
```

Rename the old file and new file

```sh
sudo mv EAMENA.xml EAMENA_old.xml
sudo mv EAMENA_fr.xml EAMENA.xml
```

activate ENV, and run `import_reference_data` ...

```sh
python manage.py packages -o import_reference_data -s '/opt/arches/eamena/eamena/pkg/reference_data/concepts/EAMENA.xml'
```

... gives this message (ORPHANS)

```
operation: import_reference_data
2024-02-21 03:21:17,255 arches.app.utils.skos WARNING  
The SKOS file "EAMENA.xml" appears to have orphaned concepts.
```

Restart Apache

```sh
(ENV) root@ip-172-31-32-122:/opt/arches/eamena# sudo service apache2 restart
```

* frontend:

RDM > Tools > Import Thesauri

## Errors

### Import errors

Imported, with errors (ORPHANS)

<p align="center">
  <img src='https://raw.githubusercontent.com/zoometh/skos2excel/master/www/err-orphans.png' width = "700px">
  <br>
    <em>French, Arabic and English... but with orphans</em>
</p>

### Delete errors

RDM > Tools > Delete Thesauri doesn't work


### Translation errors

There could have errors in the translations:

<p align="center">
  <img alt="img-name" src="../../../www/arches-v7-internationalisation-error-fr.png" width="500">
  <img alt="img-name" src="../../../www/arches-v7-internationalisation-error-fr-1.png" width="500">
  <br>
    <em>The English `Close` [the windows] has been wrongly translated to `Proche` in French</em>
</p>

If you find any errors in the translations, please update these files:

- Arabic: <a href='https://github.com/eamena-project/arches/blob/master/arches/locale/ar/LC_MESSAGES/django.po'>ar</a>
- French: <a href='https://github.com/eamena-project/arches/blob/master/arches/locale/fr/LC_MESSAGES/django.po'>fr</a>

These changes will be then proposed (Pull request) to Arches' source code

<p align="center">
  <img alt="img-name" src="../../../www/arches-ea-github-pr.png" width="1100">
  <br>
    <em>Pull request to change <a href='https://github.com/archesproject/arches/blob/master/arches/locale/fr/LC_MESSAGES/django.po'>Arches French PO file content</a></em>
</p>


## Other

Agricultural:

* Collections: https://github.com/eamena-project/eamena/blob/master/eamena/pkg/reference_data/collections/collections.xml#L2432
* Concepts:

<p align="center">
  <img alt="img-name" src="../../../www/arches-ea-v4-data-ref-concepts-agricultural.png" width="1100">
  <br>
</p>

