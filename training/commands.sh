## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##
#                                                                                 #
# Welcome to the Aches/EAMENA Database Manager training !                         #
# This document resume some Linux and Python commands for the install of an       #
# Arches database management platform with a EAMENA-like project                  #
#                                                                                 #
#                                                  credit: University of Oxford   #
#                                                  year  :                 2022   #
#                                                                                 #
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## main Linux commands
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
cat                           # print the content of a file
cd                            # change directory
chgrp                         # change files/folder group
chmod                         # change files/folders access permission
chown                         # change files/folder owner
ls                            # list folder and files
ls -a                         # list hidden and visible folders and files
ls -l                         # list folders and files + permissions + owners (visible)
ls -la                        # list folders and files + permissions + owners (hidden and visible)
man command_name              # command documentation
pwd                           # current directory
source                        # read and execute the content of a file
sudo                          # do as superuser
su user_name                  # change user
# for Apache server - - - - - - - - - - - - - - - - - - - - - -
service apache2 restart       # restart server
service apache2 status        # check status (active/inactive)

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Prerequisites and Arches/EAMENA install
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Project specifications, Arches dabatabase and EAMENA package install          # PuTTY

# switch to su
sudo su
# create a sudo user to install arches under e.g 'archesadmin'
adduser archesadmin
# .. choose a password
# append a new group to arches admin
usermod -aG sudo archesadmin                                                    # useful?
# move to archesadmin account
cd /home/archesadmin/
# move to GitHub, copy the URL of the raw version of the install script, and download it
wget https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/training/install_and_apache_and_load_pkg.sh

# edit 'install_and_apache_and_load_pkg.sh' file with vim (sudo mode)
vim install_and_apache_and_load_pkg.sh
# insert  (ESC + I) the following variables:
# your project name, replace 'xxxx' by your country name
project_name="xxxx_project"
# your host, replace 'xx.xx.xx.xx' by the IPv4 Public address of your host
my_host="xx.xx.xx.xx"
# save/write and quit (ESC + :wq + Return)

# check out by printing the first lines of the script
head -n 20 install_and_apache_and_load_pkg.sh

# running the install script
source ./install_and_apache_and_load_pkg.sh
# ... ~ 8-10 minutes to install


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

# make environment variables visibles (excecutable) by anyone
sudo chmod 745 environment      # useful ?

# to see the new variables, need to logout
exit
# and re-log in with PuTTY                                                      # PuTTY

# check out
# call the variables (echo)
echo $username
# .. gives: archesadmin
echo $project_name
# .. gives: the name of your project
cd /home/$username/$project_name/$project_name
# .. moves to your Arches project root folder

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Authorised the archesadmin user to connect via SSH
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


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Clone eamena-arches-package.git from GitHub
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# import the EAMENA package

# switch to su
sudo su
# move to the project/ folder
cd /home/$username/$project_name
# clone
git clone https://github.com/eamena-oxford/eamena-arches-package.git


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Convert business data from CSV to JSONL with 'ids_to_json.py'
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# import 'ids_to_json.py' to convert business data from CSV to JSONL
# to do in the 'main' database, e.g. EAMENA, not in the child one

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
# run the script
python manage.py ids_to_json -s /opt/arches/eamena/'Heritage Place.csv'
# ... has created a json_records.jsonl in the same directory
# rename this file
mv ./json_records.jsonl ./'Heritage Place.jsonl'

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Import business data, update Cards/Reports, reindex
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# after importing the CSV into the business_data/ folder

# import business data
python manage.py packages -o import_business_data -s 'Heritage Place.jsonl' -ow 'overwrite'
# ... ~ 1,500 HP = 15 min
# move to components/ folder
cd /home/$username/$project_name/$project_name/templates/views/components
# rename card_components/ folder as cards/
mv ./card_components ./cards
# reindex data
python manage.py es reindex_database
# ... Status: Passed, Resource Type: Heritage Place, In Database: 1592, Indexed: 1592, Took: 183 seconds


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Ubuntu: restart and check status of Apache server
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# restart and check status of the Apache HTTP Server web server

# do as superuser
sudo su
# restart server
service apache2 restart
# check status (active/inactive)
service apache2 status


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Understanding permissions and ownerships
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#

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
## main configuration files
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# settings.py and settings_local.py
cd /home/$username/$project_name/$project_name                                  # PuTTY
/home/$username/$project_name/$project_name                                     # FileZilla

# 000-default.conf
cd /etc/apache2/sites-available                                                 # PuTTY
/etc/apache2/sites-available                                                    # FileZilla

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
# ... Python 3.8.10 (default, Nov 26 2021, 20:14:08)
# ... [GCC 9.3.0] on linux
# ... Type "help", "copyright", "credits" or "license" for more information.
# ... >>>

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
# ... Python 3.8.10 (default, Nov 26 2021, 20:14:08)                            # Python
# ... [GCC 9.3.0] on linux
# ... Type "help", "copyright", "credits" or "license" for more information.
# ... >>>

# import libraries                                                              # Python
>>> import os, inspect
# copied from the settings.py file, APP_ROOT initialisation
>>> APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
>>> print(APP_ROOT)
# ... print the path to the app root like /home/$username/$project_name/$project_name


