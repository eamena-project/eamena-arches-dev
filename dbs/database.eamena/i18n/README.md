# i18n
> Internationalisation (i18n) and localisation (l10n)


## Convert thesauri and messages

Example of translation from English (`en`) to a target language (`ar`, `fr`, etc.), using the [skos2excel](https://github.com/zoometh/skos2excel) and [po2excel](https://github.com/zoometh/po2excel) tools

| thesauri | messages |
|----------|----------|
| Thesauri are controlled vocabularies describing the ressources | Messages are the texts displayed on the screen describing tabs, menus, etc., for navigation purposes |
| ![](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/master/www/rdm-thesauri-eamena.png) | ![](https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/master/www/arches-v7-internationalisation-fr.png )|
| translation with `skos2excel.py`, base: `EAMEANA.xml` | translation with `po2excel`, base: `django.po` |

### bases

The templates (so-called `base`) of these files are in the folder [bases/](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/i18n/data/bases)

* `EAMEANA.xml` (snippet)

```XML
...
<skos:Concept rdf:about="https://database.eamena.org/89fab53f-ce9d-4c0b-8ef9-d01d2899ef97">
<skos:prefLabel xml:lang="ar">{"id": "5264b031-4580-4a9c-91f2-be5d0b184da5", "value": "\u062e\u0648\u0631 \u0623\u0648 \u0645\u0635\u0628 \u0627\u0644\u0646\u0647\u0631"}</skos:prefLabel>
<skos:inScheme rdf:resource="https://database.eamena.org/4a98075d-815f-327b-be0e-518b32f7623b"/>
<skos:prefLabel xml:lang="en-us">{"id": "78fd12f7-000e-4f26-8861-360018aa40ee", "value": "Estuary"}</skos:prefLabel>
<dcterms:identifier xml:lang="en">{"id": "046d03a4-e76e-4713-aaf9-546a9f344458", "value": "https://database.eamena.org/concepts/89fab53f-ce9d-4c0b-8ef9-d01d2899ef97"}</dcterms:identifier>
</skos:Concept>
</skos:narrower>
...
```

* `django.po` (snippet)

```Python
...
#: app/datatypes/datatypes.py:564
#, python-brace-format
msgid "{value} is an invalid date format"
msgstr ""
...
```

## l10n
> Localisation

### en -> ckb

Example of translation to Central Kurdish (Sorani) (`ckb`)

#### thesauri
> ⚠️ possible typo issues with `EAMENA.xml` see [here](https://github.com/eamena-project/eamena/issues/1#issue-2225163630)

Example for the EAMENA.xml file, and translation of the DB thesauri to Central Kurdish (Sorani) (`ckb`), using the [skos2excel.py](https://github.com/zoometh/skos2excel) script

1. Convert [EAMENA.xml](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml) to [xxx_ckb.xlsx]() using the `skos2excel.py` script:

```sh
py skos2excel.py ./data/EAMENA.xml ./data/xxx_ckb.xlsx -lang ckb -f xlsx 
```

✅ Proofreading of the XLSX automatic translation. 

2. Convert (back) the [kurdish_thesaurus.xlsx]() concepts to [EAMENA.xml]() using the `excel2skos.py` script:

```sh
py C:/Rprojects/skos2excel/excel2skos.py C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/kurdish_thesaurus.xlsx C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/EAMENA.xml --base C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/bases/EAMENA.xml
```

3. Import in the DB

On the DB:

RDM > Tools > Import Thesauri > *select* `EAMENA.xml`

<p align="center">
  <img src='https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/master/www/rdm-thesauri-import.png' width = "700px">
  <br>
    <em>RDM import thesauri</em>
</p>


#### Messages

Example for the EAMENA.xml file, and translation of the DB messages to Central Kurdish (Sorani) (`ckb`), using the [po2excel.py](https://github.com/zoometh/po2excel) script

1. Convert [django.po](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/data/django.po) to [django_ckb.xlsx]() using the `skos2excel.py` script:

```sh
py po2excel.py django.po django_ckb.xlsx --format xlsx
```

✅ Proofreading of the XLSX automatic translation. 

2. Convert (back) the [kurdish_database_menu_terms.xlsx]() concepts to [django.po]() using the `excel2po.py` script:

```sh
py C:/Rprojects/po2excel/excel2po.py C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/kurdish_database_menu_terms.xlsx C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/django.po -lang ckb --base C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/bases/django.po
```

3. Import in the DB and update the DB (see: messages import)



### en -> fr

Example for the `EAMENA.xml` file, and translation to French (`fr`), using the [skos2excel](https://github.com/ads04r/skos2excel) tools

1. Convert [EAMENA.xml](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml) to [EAMENA_fr.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.xlsx) (See the corresponding [TSV file](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.tsv)) using the `skos2excel.py` script:

```sh
py skos2excel.py ./data/EAMENA.xml ./data/EAMENA_fr.xlsx -lang fr -f xlsx 
```

Proofreading of the automatic translation. 

2. Convert (back) the [EAMENA_fr.xlsx](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/i18n/EAMENA_fr.xlsx) concepts to [EAMENA_fr.xml](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr.xml) using the `excel2skos.py` script:

```sh
py excel2skos.py ./data/EAMENA_fr.xlsx ./data/EAMENA_fr.xml -b ./data/EAMENA.xml
```

see also[^1]

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

Restart Apache

```sh
(ENV) root@ip-172-31-32-122:/opt/arches/eamena# sudo service apache2 restart
```

* frontend:

RDM > Tools > Import Thesauri

## Import messages


```sh
sudo su
cd /opt/arches/
source ENV/bin/activate
```

Create the new language folders, here `ckb`, and move in: 

```sh
mkdir /opt/arches/ENV/lib/python3.10/site-packages/arches/locale/ckb
mkdir /opt/arches/ENV/lib/python3.10/site-packages/arches/locale/ckb/LC_MESSAGES
cd /opt/arches/ENV/lib/python3.10/site-packages/arches/locale/ckb/LC_MESSAGES
```

Import the `django.po` in it `LC_MESSAGES/`:

```sh
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/ckb/django.po
```

Convert the PO file (Portable Object) to a MO file (Machine Object)

```sh
msgfmt -o django.mo django.po
```

Change files ownerships and permissions

```sh
# files ownership
chown arches:arches django.po
chown arches:arches django.mo
# files permissions
chmod 755 djang*
```

Now to update the language switcher;

1. Make sure the `settings.py` new language is registered (here, `ckb`):

```py
...
LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
    ('ckb', _('Central Kurdish (Sorani)')),
]
...
```

2. Run `build_development`

```sh
cd /opt/arches/eamena/eamena/
yarn build_development &
```

3. Run `collectstatic`

```sh
cd /opt/arches/eamena
python manage.py collectstatic
```

4. Restart Apache2

```sh
service apache2 restart
```

5. Update or create the Django Admin / Languages


<p align="center">
  <img alt="img-name" src="https://raw.githubusercontent.com/zoometh/skos2excel/master/www/arches-v7-i18n-django-lang.png" width="1100">
  <br>
</p>



## Other

Agricultural:

* Collections: https://github.com/eamena-project/eamena/blob/master/eamena/pkg/reference_data/collections/collections.xml#L2432
* Concepts:

<p align="center">
  <img alt="img-name" src="../../../www/arches-ea-v4-data-ref-concepts-agricultural.png" width="1100">
  <br>
</p>

- ? Import `django_ckb.po` into the DB (`/opt/arches/ENV/lib/python3.8/site-packages/arches/locale`), see: `makemessages`
- ? Import to transifex

## Documentation

- Arches documentation - [localizing-arches](https://arches.readthedocs.io/en/stable/developing/advanced/localizing-arches/#localizing-arches)


## Errors

### Import errors

On:

```sh
python manage.py packages -o import_reference_data -s '/opt/arches/eamena/eamena/pkg/reference_data/concepts/EAMENA.xml'
```

... gives this message (ORPHANS)

```
operation: import_reference_data
2024-02-21 03:21:17,255 arches.app.utils.skos WARNING  
The SKOS file "EAMENA.xml" appears to have orphaned concepts.
```

Probable source of the issue: https://github.com/eamena-project/eamena/issues/1

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

- Arabic `ar`: <a href='https://github.com/eamena-project/arches/blob/master/arches/locale/ar/LC_MESSAGES/django.po'>ar</a>
- French `fr`: <a href='https://github.com/eamena-project/arches/blob/master/arches/locale/fr/LC_MESSAGES/django.po'>fr</a>
- Central Kurdish (Sorani) `ckb`: TODO

These changes will be then proposed (Pull request) to Arches' source code

<p align="center">
  <img alt="img-name" src="../../../www/arches-ea-github-pr.png" width="1100">
  <br>
    <em>Pull request to change <a href='https://github.com/archesproject/arches/blob/master/arches/locale/fr/LC_MESSAGES/django.po'>Arches French PO file content</a></em>
</p>


---

[^1]: ```py C:/Rprojects/skos2excel/skos2excel.py C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr_2.xlsx -lang fr -f xlsx``` and  ```py C:/Rprojects/skos2excel/excel2skos.py C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr_2.xlsx C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/EAMENA_fr_2.xml -b C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/concepts/EAMENA.xml```


