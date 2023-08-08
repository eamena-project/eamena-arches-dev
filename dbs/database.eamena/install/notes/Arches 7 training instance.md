# Instalation of a training instance

## AWS EC2 instance

Ubuntu 22
r6g.large
IP: 54.247.46.210

Host EA-training-instance
  HostName 54.247.46.210
  IdentityFile "C:/Users/Thomas Huet/Desktop/EAMENA/IT/keys/EA_training.pem"
  User ubuntu

## Install Arches v7

* create 'arches' user in `opt/arches`

* sudo apt-get update

* install [Postgres](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/install/prerequisites/PostgreSQL.md#download-postgresql)

* install [ElasticSearch](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/install/prerequisites/Elasticsearch.md)

https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/install/prerequisites/elasticsearch.yml

* install [Yarn](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/install/prerequisites/Yarn.md)

* install Python VE
	- `sudo apt-get install python3-virtualenv`
	- `sudo apt-get install virtualenv`
	- create `ENV/`
	- as arches user, run: `virtualenv --python=/usr/bin/python3 ENV`
	- activate the VE `source ENV/bib/activate`
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

* If `KeyError at /add-resource/ 34cfe98e-c2c0-11ea-...` on add HP:
	- run `python manage.py fix_default_values.py`
	- remove `sample_widget` from the package (`eamena/`) and the project (`arches/`)