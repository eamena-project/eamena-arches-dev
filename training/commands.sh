## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##
# Welcome to the Aches/EAMENA Database Manager training !                         #
# This document resume some IT commands following the install of Arches:          #
#  https://github.com/zoometh/arches-scripts/blob/master/install_and_apache.sh    #
#                                                  credit: University of Oxford   #
#                                                  year  :                 2022   #
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
## Ubuntu: installation prerequisites
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# before running the install script                                             # PuTTY

# switch to su
sudo su
# create a sudo user to install arches under e.g 'archesadmin'
adduser archesadmin
# .. choose a password
# append a new group to arches admin
usermod -aG sudo archesadmin                                                    # useful?
# move to archesadmin account
cd /home/archesadmin/
# go to GitHub, copy the URL of the raw version of the install script, and download it
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


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Ubuntu: running the install script
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# after Ubuntu: prerequisites                                                   # PuTTY

source ./install_and_apache_and_load_pkg.sh
# ~ 10 minutes to install


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Ubuntu: use of environmental variables
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# add 'permanent' environmental variables                                       # PuTTY

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

# check out
# call the variables (echo)
echo $username
# .. gives: archesadmin
echo $project_name
# .. gives: the name of your project
cd /home/$username/$project_name/$project_name
# .. moves to your Arches project root folder


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Ubuntu: authorised the Arches admin user to connect via SSH
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# create directory, copy file, change permissions

# see current permissions of SSH authorized keys                                # PuTTY
cd ~/.ssh
ls -l
# switch user from ubuntu to archesadmin
su archesadmin
# you will have to insert your password
# create a new .ssh/ folder in archesadmin/
mkdir /home/$username/.ssh
# copy the authorized_keys file that contains your public key
sudo cp /home/ubuntu/.ssh/authorized_keys /home/$username/.ssh/authorized_keys
# change file ownership from ubuntu to Arches user
sudo chown -R $username:$username /home/$username/.ssh

# check out permissions
cd /home/$username/.ssh
ls -al


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
## Ubuntu: understanding permissions and ownerships
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
## understanding Python
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ubuntu@ip-172-31-46-153:~$ cd /home/$username/
# activate Python virtual environment
ubuntu@ip-172-31-46-153:/home/archesadmin$ source env/bin/activate
# got to settings.py directory
(env) ubuntu@ip-172-31-46-153:/home/archesadmin$ cd $project_name/$project_name
# run Python
(env) ubuntu@ip-172-31-46-153:/home/archesadmin/$project_name/$project_name$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## understanding APP_ROOT
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ubuntu@ip-172-31-46-153:~$ cd /home/$username
# activate Python virtual environment
ubuntu@ip-172-31-46-153:/home/archesadmin$ source env/bin/activate
# got to settings.py directory
(env) ubuntu@ip-172-31-46-153:/home/archesadmin$ cd $project_name/$project_name
# run Python
(env) ubuntu@ip-172-31-46-153:/home/archesadmin/$project_name/$project_name$ python
## Python 3.8.10 (default, Nov 26 2021, 20:14:08)
## [GCC 9.3.0] on linux
## Type "help", "copyright", "credits" or "license" for more information.
# import libraries
>>> import os, inspect
# copied from the settings.py file, APP_ROOT initialisation
>>> APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
>>> print(APP_ROOT)
/home/$username/$project_name/$project_name
# the APP_ROOT is '/home/archesadmin/$project_name/$project_name'
# >>> MEDIA_URL = '/files/'
# >>> MEDIA_ROOT =  os.path.join(APP_ROOT)
# >>> print(MEDIA_ROOT)


