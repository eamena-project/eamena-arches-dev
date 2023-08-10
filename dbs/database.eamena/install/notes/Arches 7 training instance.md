# Instalation of a training instance

## AWS EC2 instance



## Install Arches v7




* install "Install empty Arches v7"
	- `sudo apt-get install python3-psycopg2`
	- `sudo apt-get install libpq-dev`
	- install the Python package Arches `python -m pip install "arches==7.3"`
* install "Install EAMENA customisations" from the `arches/` folder
	- `git clone https://github.com/eamena-project/eamena.git`
* upload the `settings_local_.py` file and customise it
	- `ALLOWED_HOSTS = ['54.155.109.226', ...]`
	- Pg passwords
* setup DB `python manage.py setup_db`
* run `yarn` from `eamena/eamena/`
	- `yarn add jquery-validation` (see: https://community.archesproject.org/t/errors-in-yarn-build-development/1971)
	- `yarn build_production` (45 min)
* `runserver 0:8000`
* autorise port `8000` (see AWS SG 'django-dev')
* "Empty Arches v7"
* create `/opt/arches/eamena/eamena/system_settings/` folder

* `load_packages...`
	- "user 4" issue?

* If `KeyError at /add-resource/ 34cfe98e-c2c0-11ea-...` with no defaultValue on add HP:
	- run `python manage.py fix_default_values.py`
	- remove `sample_widget` from the package (`eamena/`) and the project (`arches/`)

* import business data
	- Grid Squares
	- Person/Organization
		- turn `ACTOR ID` Python function off
		- ~~[Cardinality](https://github.com/eamena-project/eamena-arches-dev/blob/7b67fe7c736d700c077981a925cead71c2e246c2/training/2022/commands.sh#L188)~~
		- ~~turn ES off?~~
	- HP
	- ~~IR~~ (no need, only 1 IR)

* install Apache
	- run `collecticstatic` to fill the `static/` folder
	- `mkdir staticfiles/`

* install Celery
	- install `django-storages==1.13.1`
	- install `boto3==1.25.3`