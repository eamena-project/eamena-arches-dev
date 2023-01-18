# Install the ring fencing function
# AWS DB 24test

# the ring fencing has been created by Knowlegde Integration
# it was imported from https://github.com//reubenosborne1/ringfencing-function

# modify this variable to match your current Arches instance name
PROJECT="my_project"

# all JS
cd /home/archesadmin/$PROJECT/$PROJECT/media/js/views/components/functions
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/functions/ring-fencing/files/ringfencing.js
# all HTM
cd /home/archesadmin/$PROJECT/$PROJECT/templates/views/components/functions/
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/functions/ring-fencing/files/ringfencing.htm
# all PY
cd /home/archesadmin/$PROJECT/$PROJECT/functions/
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/functions/ring-fencing/files/ringfencing.py
# for views
cd /home/archesadmin/$PROJECT/$PROJECT/
mkdir views # if not extist
sudo chown $username:root ./views
cd views
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/functions/ring-fencing/files/userandgroups.py
# for commands
cd /home/archesadmin/$PROJECT/$PROJECT/management/commands
wget https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/functions/ring-fencing/files/resave_all_resources.py

# register the function in the Pg 'functions' table
cd /home/archesadmin/$PROJECT
venv
python manage.py fn register --source '/home/archesadmin/'$PROJECT'/'$PROJECT'/functions/ringfencing.py'

# modify urls.py
cd /home/archesadmin/$PROJECT/$PROJECT/
vim urls.py
# insert/add 'from .views.userandgroups import getUsers' in the imports
# insert/add 'url(r"^get/users", getUsers.as_view(), name="getUsers")' in urlpatterns

# collectstatic & restart Apache
cd /home/archesadmin/$PROJECT
venv
python manage.py collectstatic
sudo service apache2 restart

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# (optional) unregister function
cd /home/archesadmin/$PROJECT
venv
python manage.py fn unregister --source '/home/archesadmin/$PROJECT/$PROJECT/functions/ringfencing.py'

# (optional) 'resave_all_resources.py'
cd /home/archesadmin/$PROJECT/$PROJECT/management/commands
venv
python manage.py resave_all_resources
