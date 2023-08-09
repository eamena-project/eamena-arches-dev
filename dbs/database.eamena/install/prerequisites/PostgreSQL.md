Arches 7 requires **PostgreSQL 14**. This requires an upgrade from the PostgreSQL 12 for which EAMENA v3 was designed, although EAMENA v3 will happily work with PostgreSQL 14. Most of these instructions are adapted from the official Arches [Ubuntu install script](https://github.com/archesproject/arches/blob/master/arches/install/ubuntu_setup.sh).

## Download PostgreSQL

```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

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
