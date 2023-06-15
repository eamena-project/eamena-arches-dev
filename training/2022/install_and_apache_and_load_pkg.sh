#!/bin/bash

username="archesadmin"
arches_version="origin/stable/5.2.x"

# your project name, replace 'xxxx' by your country name
project_name="xxxx_project"

# replace 'xx.xx.xx.xx' by the IPv4 Public address of your host
my_host="xx.xx.xx.xx"

cd /home/$username

apt update
apt -y install software-properties-common
echo | add-apt-repository ppa:deadsnakes/ppa # add enter
apt -y install python3.8
apt-get -y install python3.8-venv python3.8-dev

apt-get -y install git

git clone https://github.com/archesproject/arches.git

python3.8 -m venv env
source env/bin/activate

# setup arches
cd arches
git checkout $arches_version
yes | bash arches/install/ubuntu_setup.sh

pip install wheel
pip install -e .
pip install -r arches/install/requirements.txt

yarn

cd /home/$username/

arches-project create $project_name
cd $project_name
yes | python manage.py setup_db

python manage.py packages -o load_package -s https://github.com/eamena-oxford/eamena-arches-package.git

apt-get -y install apache2
apt -y install apache2-dev python3-dev
pip install mod_wsgi

conf="# If you have mod_wsgi installed in your python virtual environment, paste the text generated
# by 'mod_wsgi-express module-config' here, *before* the VirtualHost is defined.

LoadModule wsgi_module "/home/$username/env/lib/python3.8/site-packages/mod_wsgi/server/mod_wsgi-py38.cpython-38-x86_64-linux-gnu.so"
WSGIPythonHome "/home/$username/env/"

<VirtualHost *:80>

    WSGIDaemonProcess arches python-path=/home/$username/$project_name
    WSGIScriptAlias / /home/$username/$project_name/$project_name/wsgi.py process-group=arches

    WSGIPassAuthorization on

    <Directory /home/$username/$project_name>
        Require all granted
    </Directory>

    Alias /static/ /home/$username/$project_name/$project_name/static/
    <Directory /home/$username/$project_name/$project_name/static/>
        Require all granted
    </Directory>

    Alias /files/uploadedfiles/ /home/$username/$project_name/$project_name/uploadedfiles/
    <Directory /home/$username/$project_name/$project_name/uploadedfiles/>
        Require all granted
    </Directory>

    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    ErrorLog /var/log/apache2/error-arches.log
    CustomLog /var/log/apache2/access-arches.log combined

</VirtualHost>"

echo "$conf" > /etc/apache2/sites-available/000-default.conf

service apache2 reload

mkdir -p /home/$username/$project_name/$project_name/static/
mkdir -p /home/$username/$project_name/$project_name/uploadedfiles/


static_vars="STATIC_ROOT = os.path.join(APP_ROOT, 'static')
STATIC_URL = '/static/'
"
echo "$static_vars" >> /home/$username/$project_name/$project_name/settings.py

allowed_hosts="ALLOWED_HOSTS = ['$my_host']"
echo "$allowed_hosts" >> /home/$username/$project_name/$project_name/settings.py

cd /home/$username/$project_name/

yes | python manage.py collectstatic

chown $username -R /home/$username/env
chown $username -R /home/$username/arches
chown $username -R /home/$username/$project_name

chmod 664 /home/$username/$project_name/$project_name/arches.log
chgrp www-data /home/$username/$project_name/$project_name/arches.log

chmod 775 /home/$username/$project_name/$project_name/uploadedfiles
chgrp www-data /home/$username/$project_name/$project_name/uploadedfiles

chmod 775 /home/$username/$project_name/$project_name
chgrp www-data /home/$username/$project_name/$project_name

chmod 775 -R /home/$username/$project_name/$project_name/static
chgrp www-data -R /home/$username/$project_name/$project_name/static

service apache2 restart
