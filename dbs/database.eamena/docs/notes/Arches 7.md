Elasticsearch required: [8.3.3](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb)
PostgreSQL required: 14

## Download PostgreSQL

```bash
sudo sh -c 'echo "deb [http://apt.postgresql.org/pub/repos/apt](http://apt.postgresql.org/pub/repos/apt) $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

wget --quiet -O - [https://www.postgresql.org/media/keys/ACCC4CF8.asc](https://www.postgresql.org/media/keys/ACCC4CF8.asc) | sudo apt-key add -

sudo apt-get install postgresql-14 postgresql-contrib-14
sudo apt-get install postgresql-14-postgis-3
sudo apt-get install postgresql-14-postgis-3-scripts
```

### Configure PostgreSQL

```bash
sudo -u postgres psql -d postgres -c "ALTER USER postgres with encrypted password 'postgis';"
sudo echo "*:*:*:postgres:postgis" >> ~/.pgpass
sudo chmod 600 ~/.pgpass
sudo chmod 666 /etc/postgresql/14/main/postgresql.conf
sudo chmod 666 /etc/postgresql/14/main/pg_hba.conf
sudo echo "standard_conforming_strings = off" >> /etc/postgresql/14/main/postgresql.conf
sudo echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf
sudo echo "#TYPE   DATABASE  USER  CIDR-ADDRESS  METHOD" > /etc/postgresql/14/main/pg_hba.conf
sudo echo "local   all       all                 trust" >> /etc/postgresql/14/main/pg_hba.conf
sudo echo "host    all       all   127.0.0.1/32  trust" >> /etc/postgresql/14/main/pg_hba.conf
sudo echo "host    all       all   ::1/128       trust" >> /etc/postgresql/14/main/pg_hba.conf
sudo echo "host    all       all   0.0.0.0/0     md5" >> /etc/postgresql/14/main/pg_hba.conf
sudo service postgresql restart

sudo -u postgres psql -d postgres -c "CREATE EXTENSION postgis;"
sudo -u postgres createdb -E UTF8 -T template0 --locale=en_US.utf8 template_postgis
sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis'"
sudo -u postgres psql -d template_postgis -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
sudo -u postgres createdb training -T template_postgis
sudo service postgresql restart
```

## Download and run Elasticsearch

```bash
wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb"
sudo dpkg -i ./elasticsearch-8.3.3-amd64.deb
```

Edit `/etc/elasticsearch/elasticsearch.yml`, set the following

```yaml
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl:
  enabled: false
```

Then start/restart ElasticSearch

## Install Yarn

NPM required: 8.19.3 / 9.6.0
Yarn required: 1.22.19
Node.JS required: 14.17.6

```bash
sudo apt-get update
sudo apt-get install nodejs npm
sudo npm i -g n
sudo n 14.17.6
sudo npm i -g npm@latest
sudo npm i -g yarn@latest
```

## Install Dependencies if using Ubuntu

```bash
sudo apt-get install gdal-bin
```

## Install EAMENA

`git clone` the project repository
Create a virtual environment
From the environment, `python -m pip install arches==7.3`

CD into eamena, activate the virtual environment

```bash
python manage.py setup_db
python manage.py runserver 0:8000
```

In another terminal, activate the virtual environment, CD into eamena/eamena

```bash
yarn
```

Make sure `ARCHES_NAMESPACE_FOR_DATA_EXPORT` is set to the local host in `settings_local.py`

```bash
yarn build_development
```

Use PSQL to copy `auth_user` table
Import package

```bash
python manage.py packages -o load_package -s /path/to/package/
```

Import the business data, as described in [[Arches 7 Upgrade]].


