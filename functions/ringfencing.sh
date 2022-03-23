# Install and work on ring fencing function
# AWS DB 23test (Masdar test)

# all JS
cd /home/archesadmin/test_project/test_project/media/js/views/components/functions
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.js
# all HTM
cd /home/archesadmin/test_project/test_project/templates/views/components/functions/
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.htm
# all PY
cd /home/archesadmin/test_project/test_project/functions/
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/ringfencing.py
# for views
cd /home/archesadmin/test_project/test_project/
mkdir views # if not extist
sudo chown $username:root ./views
cd views
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/userandgroups.py
# for commands
cd /home/archesadmin/test_project/test_project/management/commands
wget https://raw.githubusercontent.com/reubenosborne1/ringfencing-function/master/resave_all_resrouces.py
mv ./resave_all_resrouces.py ./resave_all_resources.py # correct typo error

# register function
cd /home/archesadmin/test_project
venv
python manage.py fn register --source '/home/archesadmin/test_project/test_project/functions/ringfencing.py'

# modify urls.py
cd /home/archesadmin/test_project/test_project/
vim urls.py
# insert/add 'from .views.userandgroups import getUsers' in the imports
# insert/add 'url(r"^get/users", getUsers.as_view(), name="getUsers")' in urlpatterns

# collectstatic & restart Apache
cd /home/archesadmin/test_project
venv
python manage.py collectstatic
sudo service apache2 restart

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# (optional) unregister function
cd /home/archesadmin/test_project
venv
python manage.py fn unregister --source '/home/archesadmin/test_project/test_project/functions/ringfencing.py'

# (optional) 'resave_all_resources.py'
cd /home/archesadmin/test_project/test_project/management/commands
venv
python manage.py resave_all_resources

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# function manager
# http://54.74.247.130/graph/34cfe98e-c2c0-11ea-9026-02e7594ce0a0/function_manager




