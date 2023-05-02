### Export Existing Business Data

On the EAMENA VM on AWS...
```bash
python eamena/manage.py packages -o export_business_data -f jsonl -g [graph_id] -d [dest_directory]
```

For the following `graph_id`s
```
f6235ff1-f992-11e9-b345-06f597a7d5ce
5297fa9e-8e16-11ea-a6a6-02e7594ce0a0
e98e1cee-c38b-11ea-9026-02e7594ce0a0
6c4f0703-c381-11ea-9026-02e7594ce0a0
35b99cb7-379a-11ea-9989-06f597a7d5ce
77d18973-7428-11ea-b4d0-02e7594ce0a0
34cfe98e-c2c0-11ea-9026-02e7594ce0a0
```

FTP the resulting files to the Arches 7 instance. The JSONL exporter I wrote and installed in the EAMENA Arches 5 instance automatically converts the JSON to the I18n-compatible format required by Arches 7.

On the local instance, split the Heritage Place and Information Resource files, as they're too big to import in one go...
```bash
for f in `ls Heritage_Place_*.jsonl`;
do
        split -l 10000 -d $f Heritage_Place_
        rm $f
done
for f in `ls Information_Resource_*.jsonl`;
do
        split -l 10000 -d $f Information_Resource__
        rm $f
done
```

Now run [[JSONL2JSON]] on all the files. JSON import is far quicker than JSONL import because it runs from RAM. As we split the files in the previous step, all the import files are now small enough to import in this way.
```bash
for f in `ls Heritage_Place_*`
do
        python jsonl2json.py $f > $f.json
        rm $f
done
for f in `ls Information_Resource_*`
do
        python jsonl2json.py $f > $f.json
        rm $f
done

for f in `ls *.jsonl`
do
        g=`echo $f | sed 's/l$//'`
        python jsonl2json.py $f > $g
        rm $f
done
```

### Upgrade Arches to 7.3

Back up the production instance and stop Apache and Celery.

```bash
sudo systemctl stop apache2
sudo systemctl stop celery
```

Delete the old instance (`arches` and `eamena` directories, and run `drop.sql` on the database.) Install PostgreSQL and Elasticsearch, and create a new virtual environment at `/opt/arches/ENV`, as described in the [[Arches 7]] install instructions. Ensure all the dependencies from `requirements.txt` are installed into the virtual environment using `pip`. Now clone the EAMENA Github repository into `/opt/arches/eamena`.

Activate the virtual environment and set up the database.

```bash
python eamena/manage.py setup_db
```
Now import the EAMENA package

```shell
python eamena/manage.py packages -o load_package -s eamena/eamena/pkg
```

This will get you to the state of having a working, but empty, Arches 7 database. Test by using the `runserver` command...

```shell
python eamena/manage.py runserver 0:8000
```

### Import Business Data

Next, disable triggers on the database with `alter table tiles disable trigger all;` and ensure that `BYPASS_UNIQUE_CONSTRAINT_TILE_VALIDATION` and `BYPASS_REQUIRED_VALUE_TILE_VALIDATION` are both set to `True` within `settings.py`. Also, ensure the incrementor function is disabled within all the models from the Arches 7 UI. Then, with the VENV activated...
```bash
for f in `find import | grep Person-Org`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Grid_Square`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Built_Component`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Detailed_Condition_Assessment`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Geoarchaeology`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Information_Resource`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done

for f in `find import | grep Heritage_Place`
do
        python eamena/manage.py packages -pi -o import_business_data -ow overwrite -s "$f"
done
```
Re-enable the database triggers, and reset settings.py to its original values. 

## Arches Function Settings

The function settings are not included in the package, and need to be changed for the import anyway. On the production system the resource models need to be configured as follows...

* Person / Organisation
	* Incrementor
		* Card Name: `ACTOR ID`
		* Prefix: `ACTOR-`
	* Define Resource Descriptors
		* Display Name: `Appellation`
		* Display Description: `Appellation`
		* Primary Description Template: `<Appellation>`
		* Map Pop-Up: `Appellation`

* Grid Square
	* Incrementor - **DISABLED**
	* Define Resource Descriptors
		* Display Name: `Grid Square Identification`
		* Display Description: `Grid Square Identification`
		* Primary Description Template: `<Grid ID>`
		* Map Pop-Up: `Grid Square Identification` / `<Grid ID>, <Grid Square Geometry>`

* Heritage Place
	* Incrementor
		* Card Name: `EAMENA ID`
		* Prefix: `EAMENA-`
	* Define Resource Descriptors
		* Display Name: `EAMENA ID`
		* Display Description: `Name`
		* Primary Description Template: `<Resource Name>`
		* Map Pop-Up: `Name`
* Information Resource
	* Incrementor
		* Card Name: `INFORMATION ID`
		* Prefix: `INFORMATION-`
	* Define Resource Descriptors
		* Display Name: `INFORMATION ID`
		* Display Description: `Resource Type`
		* Primary Description Template: `<Resource Type>`
		* Map Pop-Up: `INFORMATION ID`

* Geoarchaeology
	* Incrementor
		* Card Name: `GEOARCH ID_new` / Node to update: `GEOARCH ID`
		* Prefix: `GEOARCH-`
	* Define Resource Descriptors
		* Display Name: `GEOARCH ID_new`
		* Display Description: `GEOARCH ID_new`
		* Primary Description Template: `<GEOARCH ID>`
		* Map Pop-Up: `GEOARCH ID_new`

* Built Component
	* Incrementor
		* Card Name: `COMPONENT ID`
		* Prefix: `COMPONENT-`
	* Define Resource Descriptors
		* Display Name: `COMPONENT ID`
		* Display Description: `Built Component Observation`
		* Primary Description Template: `<Component Type>`
		* Map Pop-Up: `COMPONENT ID`

* Detailed Condition Assessment
	* Incrementor
		* Card Name: `CONDITION ID`
		* Prefix: `CONDITION-`
	* Define Resource Descriptors
		* Display Name: `CONDITION ID`
		* Display Description: `Assessment Summary`
		* Primary Description Template: `<Heritage Place> <Assessment Activity Date>`
		* Map Pop-Up: `CONDITION ID`

