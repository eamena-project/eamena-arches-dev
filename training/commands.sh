## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##
#                                                                                 #
#                                                                                 #
# Welcome to the Aches/EAMENA Database Manager training part 2                    #
# This document resume some Linux and Python commands for the install of an       #
# Arches database management platform with a EAMENA-like project                  #
#                                                                                 #
#                                                  credit:         EAMENA project #
#                                                  year  :                 2022   #
#                                                                                 #
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## main Linux commands
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
.                             # current directory
..                            # parent directory
>>                            # redirects output to a file, append at the end
cat                           # print the content of a file
cd                            # change directory
chgrp                         # change files/folder group
chmod                         # change files/folders access permission
chown                         # change files/folder owner
exit                          # exit the current location
logout                        # terminate the SSH connection
ls                            # list folder and files
ls -a                         # list hidden and visible folders and files
ls -l                         # list folders and files + permissions + owners (visible)
ls -la                        # list folders and files + permissions + owners (hidden and visible)
man command_name              # command documentation
pwd                           # current directory
q                             # quit
source                        # read and execute the content of a file
sudo                          # do as superuser
su user_name                  # change user
# for services like Apache, ElasticSearch, PostgreSQL, etc. ($servicename) - - -
service $servicename start    # start service
service $servicename stop     # start service
service $servicename restart  # restart service
service $servicename status   # check status (active/inactive)


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Connect via SSH
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# connect via Windows command, PowerShell terminal, etc.                        # PowerShell

# mv to the folder containing the private keys
cd 'C:\Users\Thomas Huet\Desktop\EAMENA\IT\keys'
# launch the SSH connection (ex: 'Palestine Masdar II' hosted on AWS)
ssh -i PalestineMasdarII.pem ubuntu@34.242.117.242

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Prerequisites and Arches/EAMENA install
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Project specifications, Arches dabatabase and EAMENA package install          # PuTTY

# move to home/ directory
cd /home
# switch to su
sudo su
# create archesadmin user to install arches under it
adduser archesadmin
# ... choose a password, ex: 'arches'
# ... (opt)
# grant sudo privileges to archesadmin
usermod -aG sudo archesadmin
# move to archesadmin account
cd /home/archesadmin/
# move to GitHub, copy the URL of the raw version of the install script, and download it
wget https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/training/install_and_apache_and_load_pkg.sh
# ... see: https://github.com/eamena-oxford/eamena-arches-dev/blob/main/training/install_and_apache_and_load_pkg.sh
# edit 'install_and_apache_and_load_pkg.sh' file with an editor (ex: vim) in sudo mode
vim install_and_apache_and_load_pkg.sh
# insert  (ESC + I) the following variables:
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# . project_name="xxxx_project" / replace "xxxx" by your project name /
# . my_host="xx.xx.xx.xx" / replace "xx.xx.xx.xx" by a Public IPv4 or "localhost" /
# . / save/write and quit (ESC + :wq + Return) /
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# check out by printing the first lines of the script
head -n 20 install_and_apache_and_load_pkg.sh

# running the install script
source ./install_and_apache_and_load_pkg.sh
# ... ~ 8-10 minutes to install
# move to the parent directory
cd ..
# move the script to the appropriate folder (install/)
mv install_and_apache_and_load_pkg.sh /home/archesadmin/arches/arches/app/functions/install

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Use of environment variables
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# add 'permanent' environment variables                                         # PuTTY

# move to etc/ folder
cd /etc

# edit 'environment' file with vim (sudo mode)
sudo vim environment
# insert  (ESC + I) the following variables:
# your project name, replace 'xxxx' by your country name
export project_name="xxxx_project"
# your Arches user name (app admin)
export username="archesadmin"
# save/write and quit (ESC + :wq + Return)

# need to exit for Linux to update the new variables
exit
# need to exit for Linux to update the new variables
exit
# and re-log in with PuTTY                                                      # PuTTY

# create shortcut to activate the Python virtual environment (env)
cd /home/$user_name
# edit .bashrc
vim .bashrc
# insert  (ESC + I) the following alias at the end of the file:
alias venv='source ~/env/bin/activate'
# save/write and quit (ESC + :wq + Return)

# check out
# call the variables (echo)
echo $username
# .. gives: archesadmin
echo $project_name
# .. gives: the name of your project
cd /home/$username/$project_name/$project_name
# .. moves to your Arches project root folder
venv
# .. (env) 


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Authorise archesadmin user to connect via SSH (opt)
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# create directory, copy file, change permissions

# move to the .ssh/ folder                                                      # PuTTY
cd ~/.ssh
# see current permissions of SSH authorized keys
ls -l
# switch from ubuntu user to archesadmin user
su archesadmin
# ... you will have to insert your password
# create a new .ssh/ folder in archesadmin/
mkdir /home/$username/.ssh
# copy the authorized_keys file that contains your public key
sudo cp /home/ubuntu/.ssh/authorized_keys /home/$username/.ssh/authorized_keys
# change file ownership from ubuntu to archesadmin user
sudo chown -R $username:$username /home/$username/.ssh

# check out permissions
cd /home/$username/.ssh
ls -al
# ... total 12
# ... drwxrwxr-x 2 archesadmin archesadmin 4096 Feb 11 18:25 .
# ... drwxr-xr-x 6 archesadmin archesadmin 4096 Feb 11 18:25 ..
# ... -rw------- 1 archesadmin archesadmin  392 Feb 11 18:25 authorized_keys

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Add business data into the eamena-arches-package package
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# import the EAMENA package, add business data into the business_data/ folder

# switch to su                                                                  # PuTTY
sudo su
# activate Python virtual environment (env)
venv
# ...(env)
# move to the project/ folder
cd $project_name
# clone the 'eamena-arches-package' package
git clone https://github.com/eamena-oxford/eamena-arches-package.git
# change permission of 'eamena-arches-package' package to allow archesadmin
sudo chown -R $username:root ./eamena-arches-package
# mv to the business_data/ folder
cd eamena-arches-package/business_data
# in Filezilla                                                                  # FileZilla
# mv to /home/$username/$project_name/eamena-arches-package/business_data
# and upload from your local site to your server:
#   - Grid Square.jsonl
#   - Organization.jsonl
#   - Heritage Place.jsonl
# in PuTTY                                                                      # PuTTY
# move to the project/ folder
cd /home/$username/$project_name
# load package
python manage.py packages -o load_package -s eamena-arches-package/ -db
# ...
# collect static
# python manage.py collectstatic


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Convert business data from CSV to JSONL with 'ids_to_json.py'
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# import 'ids_to_json.py' to convert business data from CSV to JSONL
# /!\ to do in the 'main' database, e.g. EAMENA, not in the child one

# switch to su
sudo su
# move to the command/ folder
cd /opt/arches/eamena/eamena/management/commands
# move to GitHub, copy the URL of the raw version of the script (csv to jsonl), and download it
wget https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/training/ids_to_json.py
# move to arches/ folder
cd /opt/arches
# activate env
source ENV/bin/activate
# move to eamena/ folder
cd eamena
# check out if the dataset is here by listing
ls
# ... 'Heritage Place.csv' ...
# if not, add it here with FileZilla
# nb in this file 'resourceid' field should be renamed 'ResourceID'
# run the script
python manage.py ids_to_json -s /opt/arches/eamena/'Heritage Place.csv'
# ... has created a json_records.jsonl in the same directory
# rename this file
mv ./json_records.jsonl ./'Heritage Place.jsonl'

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Import business data, reindex
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Add business data into the package

# do as superuser                                                               # PuTTY
sudo su
# move to archesadmin user folder & activate Python virtual environment (env)
cd /home/$username/ && source env/bin/activate
# ...(env)
# move where is your JSONL file and manage.py
cd $project_name

# Arches Card Designer                                                          # Arches
# Authorise mutiple values to these field to fit the model with the data 
# by changing the cardinality of Cards, 'Allows Multiple Values' to these fields  
# RM > Person/organization > Card > 
#   > ACTOR ID
# RM > Grid Square
#   > Geometry Place Expression
# RM > HP > Card > 
#   > Bedrock Geology 
#   > Priority Assignment
#   > Detailed Condition Assessments

# - - - - - - - - - - -
# ERROR need value
# by adding a default vale
# RM > Person/organization > Card > 
#   > Actor/Investigator

# import business data                                                          # PuTTY
python manage.py packages -o import_business_data -s 'eamena-arches-package/business_data/Organization.jsonl' -ow 'overwrite'
# ...
python manage.py packages -o import_business_data -s 'eamena-arches-package/business_data/Grid Square.jsonl' -ow 'overwrite'
# ...
python manage.py packages -o import_business_data -s 'eamena-arches-package/business_data/Heritage Place.jsonl' -ow 'overwrite'
# ... ~ 1,500 HP = 15 min
# reindex data
python manage.py es index_database
# ... ~ 1,500 HP = 7 min
# restart server
service apache2 restart

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Update Cards/Reports
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 

# do as superuser
sudo su
# move to components/ folder
cd /home/$username/$project_name/$project_name/templates/views/components
# rename card_components/ folder as cards/
mv ./card_components ./cards

# import new cards
# HTM  file in cards/
cd /home/$username/$project_name/$project_name/templates/views/components/cards
curl -O https://raw.githubusercontent.com/eamena-oxford/eamena-arches-5-project/master/eamena/pkg/extensions/card_components/eamena-default-card/eamena-default-card.htm
# ... eamena-default-card.htm, and change ownership & permission
sudo chown -R $username:$username ./eamena-default-card.htm && chmod 644 ./eamena-default-card.htm
# JS related file in media/
cd /home/$username/$project_name/$project_name/media/js/views/components/card_components
curl -O https://raw.githubusercontent.com/eamena-oxford/eamena-arches-5-project/master/eamena/pkg/extensions/card_components/eamena-default-card/eamena-default-card.js
# ... eamena-default-card.js, and change ownership & permission
sudo chown -R $username:$username ./eamena-default-card.js && chmod 644 ./eamena-default-card.js
# JSON related file in $project_name/
cd /home/$username/$project_name/$project_name
curl -O https://raw.githubusercontent.com/eamena-oxford/eamena-arches-5-project/master/eamena/card_components
# ... eamena-default-card.json, and change ownership & permission
sudo chown -R $username:$username ./card_components && chmod 644 ./card_components

# move to card_components/
cd /home/$username/$project_name/$project_name/media/js/views/components/card_components
# copy card to static/ | useful ?
sudo yes | cp -r eamena-default-card.js /home/$username/$project_name/$project_name/static/js/views/components/cards
# move to cards/
cd /home/$username/$project_name/$project_name/static/js/views/components/cards
# change ownership & permissions
sudo chown -R $username:www-data ./eamena-default-card.js && chmod 775 ./eamena-default-card.js
# move to components/
cd /home/$username/$project_name/$project_name/static/js/views/components
# create symlink
ln -s cards card_components 
# change ownership
sudo chown -R $username:www-data ./card_components
# change user
su archesadmin
# activate Python virtual environment
cd /home/$username/ && source env/bin/activate
# ... (env)
# move to the project/ folder
cd /home/$username/$project_name
# collect static
python manage.py collectstatic

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Apache server, restart and check status
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# restart and check status of the Apache HTTP Server web server

# do as superuser
sudo su
# restart server
service apache2 restart
# check status (active/inactive)
service apache2 status

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## ElasticSearch, check status
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check status of the ElasticSearch

# move where is your JSONL file and manage.py
cd $project_name
# activate Python virtual environment (env)
venv
# ...(env)
# check status (active/inactive)
systemctl status elasticsearch
# re-index everything in database
python manage.py es index_database
# re-index by resource model
python manage.py es index_resources_by_type -rt [UUID for Resource Model]
# python manage.py es index_resources_by_type -rt '34cfe98e-c2c0-11ea-9026-02e7594ce0a0'
# python manage.py es index_resources_by_type -rt 34cfe98e-c2c0-11ea-9026-02e7594ce0a0

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Understanding permissions and ownerships
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# list permissions (user, group) for files and folder

# move to img/ folder
cd /home/$username/$project_name/$project_name/static/img
# list files' and folders' permissions and ownerships
ls -la
# ...
# drwxrwxr-x  4 archesadmin www-data  4096 Jan 17 11:59 landing
# ..
su $username


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Customize the homepage of the Arches/EAMENA
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# move files from remote site (download) and local site (upload)

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# move to the root of the project (= Python APP_ROOT variable)
cd /home/$username/$project_name/$project_name                                  # PuTTY
# In FileZilla, replace $username and $project_name by the variable values
/home/$username/$project_name/$project_name                                     # FileZilla

# move to the templates/ project folder
/home/$username/$project_name/$project_name/templates                           # FileZilla
# In FileZilla, replace $username and $project_name by the variable values
cd /home/$username/$project_name/$project_name/templates                        # PuTTY

# move to the landing/ project folder
/home/$username/$project_name/$project_name/static/img/landing                  # FileZilla
# In FileZilla, replace $username and $project_name by the variable values
cd /home/$username/$project_name/$project_name/static/img/landing               # PuTTY

# move to the sites-available/ folder
/etc/apache2/sites-available                                                    # FileZilla
cd /etc/apache2/sites-available                                                 # PuTTY


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Delete / Remove resources
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# delete resources with Python shell

# move to the project/ folder                                                   # PuTTY
cd /home/$username/$project_name
# activate Python virtual environment (env)
# ...(env)
venv
# run Python
python manage.py shell
# ... Python 3.8.10 (default, Nov 26 2021, 20:14:08)                            # PuTTY / Python
# ... [GCC 9.3.0] on linux
# ... Type "help", "copyright", "credits" or "license" for more information.
# ... >>>
from arches.app.models.resource import Resource                                 # Python
import pandas as pd
import os

# Delete one resource from its UUID (ie, 'resourceinstanceid')
Resource.objects.get(pk='228e6003-eba5-48ed-8d01-128d3b2c2c7c').delete()        

# Delete HP by batch
# 'Heritage_Place_ID.csv' is in the Python folder '/home/$username/$project_name'
# Resources UUID are listed as:
# 5c6144d3-a4a5-48f7-938c-ac38b043b46e, 520de939-79f7-44cc-b255-888a6214cd30, etc.
resource_data = pd.read_csv(os.path.join(os.getcwd(), 'Heritage_Place_ID.csv'))
# get the keys = UUIDs
resource_ids = list(resource_data.keys())

for _id in resource_ids:
    instance = Resource.objects.get(pk=_id)
    instance.delete()
# ...
# True

# reindex ElasticSearch
python manage.py es index_database

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Main configuration files
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# settings.py and settings_local.py
cd /home/$username/$project_name/$project_name                                  # PuTTY
/home/$username/$project_name/$project_name                                     # FileZilla

# 000-default.conf
cd /etc/apache2/sites-available                                                 # PuTTY
/etc/apache2/sites-available                                                    # FileZilla

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Issues: index issue
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# on RelatedObjectDoesNotExist error ?

# move to the project/ folder                                                   # PuTTY
cd /home/$username/$project_name
# activate Python virtual environment (env)
# ...(env)
venv
# delete index
python manage.py es delete_indexes
# re-setup index
python manage.py es setup_indexes
# re-index
python manage.py es index_database



## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Understanding Python
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# run Python                                                                    # PuTTY

# move to archesadmin user folder
cd /home/$username/
# activate Python virtual environment (env)
source env/bin/activate
# ...(env)
# move to the settings.py directory
cd $project_name/$project_name
# run Python
python
# ... Python 3.8.10 (default, Nov 26 2021, 20:14:08)                            # PuTTY / Python
# ... [GCC 9.3.0] on linux
# ... Type "help", "copyright", "credits" or "license" for more information.
# ... >>>

# import os library
import os
# current directory
os.getcwd()
# ... '/home/$username'

# exit Python
exit()
# ... back to shell                                                             # PuTTY



## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Understanding APP_ROOT
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# get the value of the APP_ROOT variable

# move to archesadmin user folder
cd /home/$username/
# activate Python virtual environment (env)
source env/bin/activate
# ...(env)
# move to the settings.py directory
cd $project_name/$project_name
# run Python
python
# ... Python 3.8.10 (default, Nov 26 2021, 20:14:08)                            # PuTTY / Python
# ... [GCC 9.3.0] on linux
# ... Type "help", "copyright", "credits" or "license" for more information.
# ... >>>

# import libraries
import os, inspect
# copied from the settings.py file, APP_ROOT initialisation
APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(APP_ROOT)
# ... print the path to the app root = /home/$username/$project_name/$project_name


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Export data from Arches v3 - http://levant.eamena.training/
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 34.254.48.177

# following https://arches.readthedocs.io/en/3.1.2/arches-data/ guidelines:
# mv to Projects-DEP/
cd /home/ubuntu/Projects-DEP/
# activate VE
source ENV/bin/activate
# mv to Projects-DEP/
cd /home/ubuntu/Projects-DEP/eamena
# run export
python manage.py packages -o export_resources -d EAMENA_data
# return an error:
# operation: export_resources
# package: eamena
# Traceback (most recent call last):
#   File "manage.py", line 28, in <module>
#     execute_from_command_line(sys.argv)
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/django/core/management/__init__.py", line 399, in execute_from_command_line    
#     utility.execute()
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/django/core/management/__init__.py", line 392, in execute
#     self.fetch_command(subcommand).run_from_argv(self.argv)
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/django/core/management/base.py", line 242, in run_from_argv
#     self.execute(*args, **options.__dict__)
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/django/core/management/base.py", line 285, in execute
#     output = self.handle(*args, **options)
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/arches/management/commands/packages.py", line 130, in handle
#     self.export_resources(package_name, options['dest_dir'])
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/arches/management/commands/packages.py", line 409, in export_resources
#     resource_exporter.export(search_results=False, dest_dir=data_dest)
#   File "/home/ubuntu/Projects-DEP/ENV/lib/python2.7/site-packages/arches/app/utils/data_management/resources/exporter.py", line 34, in export    
#     self.writer.write_resources(dest_dir)
# TypeError: write_resources() takes exactly 3 arguments (2 given)
