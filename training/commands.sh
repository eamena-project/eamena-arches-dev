## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## main Linux commands
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
cd                    # change directory
chmod                 #
ls                    # list folder and files
man function_name     #
pwd                   # current directory
source                #


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## use environmental variable to navigate into the directory
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# add the project name in a 'permanent' environmental variable
cd /etc
sudo vim environment
# replace 'xxx' by the country name &
# add line: project_name="xxxx_project"

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# replace $project_name by the name of your project
# root of the project (APP_ROOT)
cd /home/archesadmin/$project_name/$project_name    # PuTTY
/home/archesadmin/$project_name/$project_name       # FileZilla (Remote site)

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## main configuration files
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# settings.py and settings_local.py
cd /home/archesadmin/$project_name/$project_name    # PuTTY
/home/archesadmin/$project_name/$project_name       # FileZilla (Remote site)

# 000-default.conf
cd /etc/apache2/sites-available                     # PuTTY
/etc/apache2/sites-available                        # FileZilla (Remote site)

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## understanding Python
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ubuntu@ip-172-31-46-153:~$ cd /home/archesadmin/
# activate Python virtual environment
ubuntu@ip-172-31-46-153:/home/archesadmin$ source env/bin/activate
# got to settings.py directory
(env) ubuntu@ip-172-31-46-153:/home/archesadmin$ cd jordan_project/jordan_project/
# run Python
(env) ubuntu@ip-172-31-46-153:/home/archesadmin/jordan_project/jordan_project$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## understanding APP_ROOT
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ubuntu@ip-172-31-46-153:~$ cd /home/archesadmin/
# activate Python virtual environment
ubuntu@ip-172-31-46-153:/home/archesadmin$ source env/bin/activate
# got to settings.py directory
(env) ubuntu@ip-172-31-46-153:/home/archesadmin$ cd jordan_project/jordan_project/
# run Python
(env) ubuntu@ip-172-31-46-153:/home/archesadmin/jordan_project/jordan_project$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os, inspect
# APP_ROOT (https://github.com/eamena-oxford/eamena-arches-dev/blob/f05af3a8d851bed41724e1717d1d986a93b72a65/training/JordanMasdar/files/settings.py#L16)
>>> APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
>>> print(APP_ROOT)
/home/archesadmin/jordan_project/jordan_project
# the APP_ROOT is '/home/archesadmin/jordan_project/jordan_project'
# >>> MEDIA_URL = '/files/'
# >>> MEDIA_ROOT =  os.path.join(APP_ROOT)
# >>> print(MEDIA_ROOT)
