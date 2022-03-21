# work on ring fencing function
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

# register function
cd /home/archesadmin/test_project
venv
python manage.py fn register --source '/home/archesadmin/test_project/test_project/functions/ringfencing.py'



