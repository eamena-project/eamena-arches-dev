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
# save/write and quit (ESC + :wq)

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
## Ubuntu: restart and check status of Apache web server
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#

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

# move to the landing/ project folder
/home/$username/$project_name/$project_name/static/img/landing                  # FileZilla
cd /home/$username/$project_name/$project_name/static/img/landing               # PuTTY
# move to the templates/ project folder
/home/$username/$project_name/$project_name/templates                           # FileZilla
cd /home/$username/$project_name/$project_name/templates                        # PuTTY

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
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os, inspect
# APP_ROOT (https://github.com/eamena-oxford/eamena-arches-dev/blob/f05af3a8d851bed41724e1717d1d986a93b72a65/training/JordanMasdar/files/settings.py#L16)
>>> APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
>>> print(APP_ROOT)
/home/$username/$project_name/$project_name
# the APP_ROOT is '/home/archesadmin/$project_name/$project_name'
# >>> MEDIA_URL = '/files/'
# >>> MEDIA_ROOT =  os.path.join(APP_ROOT)
# >>> print(MEDIA_ROOT)


