# === create an arches user and switch to ===
sudo adduser arches
sudo usermod -aG sudo arches
su arches

# === make an arches folder in /opt ====
sudo mkdir /opt/arches/
sudo chown arches /opt/arches

# === INSTALL PREREQUISITES ===
# === === 1) Python and ENV === ===
sudo apt-get update
sudo apt-get install python3-virtualenv
sudo apt-get install virtualenv
cd /opt/arches
virtualenv --python=/usr/bin/python3 ENV
source ENV/bin/activate

# === === 2) Elasticsearch === ===
cd ~
mkdir arches_install_files
cd arches_install_files
# wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-arm64.deb" # AWS
# sudo dpkg -i ./elasticsearch-8.3.3-arm64.deb
wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb" # WD local
sudo dpkg -i ./elasticsearch-8.3.3-amd64.deb

# === === === manually edit the elasticsearch configuration file, replacing ALL security settings with the following uncommented text === === ===
sudo nano /etc/elasticsearch/elasticsearch.yml
# xpack.security.enabled: false
# xpack.security.enrollment.enabled: false
# xpack.security.transport.ssl.enabled: false
# xpack.security.http.ssl:
#   enabled: false
sudo systemctl restart elasticsearch

# === === 3) Postgres === ===
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-14 postgresql-contrib-14
sudo apt-get install postgresql-14-postgis-3
sudo apt-get install postgresql-14-postgis-3-scripts
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
sudo -u postgres createdb -E UTF8 -T template0 --locale=en_US.utf8 template_postgis # I had to change the locale to C.utf* after running locale -a
sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis'"
sudo -u postgres psql -d template_postgis -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
sudo -u postgres psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
sudo -u postgres createdb training -T template_postgis
sudo service postgresql restart

# === === 3) NodeJS, NPM, Yarn === ===
sudo apt-get install nodejs npm
sudo npm i -g n
sudo n 14.17.6
sudo npm i -g npm@9.6.0
sudo npm i -g yarn@1.22.19

# === === 4) Apache === ===
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
# === === === manually create an apache config file 'arches.conf' then run the following === === ===
sudo a2ensite arches.conf
sudo a2dissite 000-default.conf
sudo a2enmod rewrite
sudo apache2ctl configtest
sudo systemctl restart apache2
cd /opt
sudo chmod 755 -R arches

# === === 5) Celery === ===
sudo apt-get install rabbitmq-server
sudo apt-get install rabbit
sudo rabbitmqctl add_vhost arches
sudo rabbitmqctl add_user arches
# (use 5wQf3J3JRUktFRW for password)
sudo rabbitmqctl set_permissions -p arches arches ".*" ".*" ".*"
sudo systemctl restart rabbitmq-server
sudo systemctl status rabbitmq-server
sudo nano /etc/systemd/system/celery.service
# copy the following uncommented text into file
# [Unit]
# Description=EAMENA Celery Broker Service
# After=rabbitmq-server.service

# [Service]
# User=arches
# Group=arches
# WorkingDirectory=/opt/arches/eamena
# ExecStart=/opt/arches/ENV/bin/python /opt/arches/eamena/manage.py celery start
# Environment="PATH=/opt/arches/ENV/bin:$PATH"
# Restart=always
# KillSignal=SIGINT

# [Install]
# WantedBy=multi-user.target

# === INSTALL ARCHES ===
sudo apt-get install python3-psycopg2
sudo apt-get install libpq-dev
python -m pip install "arches==7.3"

# === CLONE EAMENA GIT PROJECT/PACKAGE ===
cd /opt/arches
git clone https://github.com/eamena-project/eamena.git
# can now start celery
sudo systemctl enable celery
sudo systemctl start celery
sudo systemctl status celery

# === DELETE ALL BUSINESS DATA ===
rm /opt/arches/eamena/eamena/pkg/business_data/files/*

# === MOVE THE CUSTOMISED settings_local.py INTO THE PROJECT FOLDER
cp /mnt/c/Users/mlpq35/Downloads/l_drive/krg_arches_data/wsl/settings_local.py /opt/arches/eamena/eamena/settings_local.py

# === MOVE THE CONVERTED System_Settings.json file INTO THE PROJECT SYSTEM SETTINGS FOLDER
cd /opt/arches/eamena
python manage.py convert_json_57 -s /opt/arches/eamena/eamena/pkg/system_settings/System_Settings.json > /opt/arches/eamena/eamena/pkg/system_settings/System_Settings_conv.json
rm /opt/arches/eamena/eamena/pkg/system_settings/System_Settings.json
mkdir /opt/arches/eamena/eamena/system_settings
mv /opt/arches/eamena/eamena/pkg/system_settings/System_Settings_conv.json /opt/arches/eamena/eamena/system_settings/System_Settings.json
rm /opt/arches/eamena/eamena/system_settings/pkg/System_Settings_conv.json
cp /opt/arches/eamena/eamena/system_settings/System_Settings.json /opt/arches/eamena/eamena/pkg/system_settings/System_Settings.json
# this needs testing to make sure it works - choose Y for overwrite settings

# === LOAD THE PACKAGE ===
cd /opt/arches/eamena
python manage.py packages -o load_package -s /opt/arches/eamena/eamena/pkg/ -db

# === BUILD DEVELOPMENT FRONTEND ===
cd /opt/arches/eamena/eamena
cp /mnt/c/Users/mlpq35/Downloads/l_drive/krg_arches_data/wsl/package.json package.json # WD local
# download and extract media.tar and staticfiles.tar to /opt/arches/media and /opt/arches/eamena/eamena/staticfiles
# mkdir /opt/arches/media
# cd /opt/arches/media
# tar -xvf /mnt/c/Users/mlpq35/Downloads/l_drive/krg_arches_data/wsl/media.tar
# mkdir /opt/arches/eamena/eamena/staticfiles
# cd /opt/arches/eamena/eamena/staticfiles
# tar -xvf /mnt/c/Users/mlpq35/Downloads/l_drive/krg_arches_data/wsl/staticfiles.tar
mkdir /opt/arches/media
cd /opt/arches/media
tar -xvf /home/arches/arches_install_files/media.tar
mkdir /opt/arches/eamena/eamena/staticfiles
cd /opt/arches/eamena/eamena/staticfiles
tar -xvf /home/arches/arches_install_files/staticfiles.tar

# === === Install and run Yarn === ===
python /opt/arches/eamena/manage.py runserver # on separate terminal
cd /opt/arches/eamena/eamena
yarn install
yarn build_development

# === FIX DEFAULT VALUES ERROR ===
cd /opt/arches/eamena
python manage.py fix_default_value

# === CHECK IT WORKS! ===
python manage.py runserver

# === LOAD GRIDS ===
python manage.py packages -o import_business_data -s /home/arches/arches_install_files/GS.csv -ow overwrite
python manage.py es reindex_database

/home/arches/arches_install_files/GS.csv

# === BULK UPLOADER ===
# upload the original template file /opt/arches/bus_templates/34cfe98e-c2c0-11ea-9026-02e7594ce0a0.xlsx
pip install geomet

# === === Test it works using the backend === ===
# upload a known working BU template (file.xlsx)
python /opt/arches/eamena/manage.py bu -w strict -o validate -g 34cfe98e-c2c0-11ea-9026-02e7594ce0a0 -s <file.xlsx>

# ==
# upload database-eamena.orf.conf to /etc/apache2/sites_available
# # you may want to change ownership to arches of sites_available
sudo a2dissite *.conf
sudo a2ensite database.eamena.org
sudo a2enmod rewrite
sudo apache2ctl configtest
sudo systemctl restart apache2
cd /opt
sudo chmod 755 -R arches