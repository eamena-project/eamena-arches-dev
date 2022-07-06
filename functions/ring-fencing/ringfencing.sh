# Install the ring fencing function
# AWS DB 24test

# modify these variables to match your current Arches instance
PROJECT="my_project"

# all JS
cd /home/archesadmin/$PROJECT/$PROJECT/media/js/views/components/functions
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.js
# all HTM
cd /home/archesadmin/$PROJECT/$PROJECT/templates/views/components/functions/
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.htm
# all PY
cd /home/archesadmin/$PROJECT/$PROJECT/functions/
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.py
# for views
cd /home/archesadmin/$PROJECT/$PROJECT/
mkdir views # if not extist
sudo chown $username:root ./views
cd views
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/userandgroups.py
# for commands
cd /home/archesadmin/$PROJECT/$PROJECT/management/commands
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/resave_all_resrouces.py
mv ./resave_all_resrouces.py ./resave_all_resources.py # correct typo error

# register function
cd /home/archesadmin/$PROJECT
venv
python manage.py fn register --source '/home/archesadmin/$PROJECT/$PROJECT/functions/ringfencing.py'

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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# function manager
http://54.74.247.130/graph/34cfe98e-c2c0-11ea-9026-02e7594ce0a0/function_manager
nb HP = 1592
# 1
EAMENA-0187131, er-Rasm
Overall Archaeological Certainty
Overall Archaeological Certainty Value
High
