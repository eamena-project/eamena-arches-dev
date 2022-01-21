


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## main Linux commands
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
cd      # change directory
ls      # list folder and files
pwd     # current directory


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## use environmental variable to navigate into the folders
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# add the project name in a 'permanent' environmental variable
cd /etc
sudo vim environment
# replace 'xxx' by the country name &
# add line: project_name="xxxx_project"

# use $project_name to cd to the root of the project (APP_ROOT)
/home/archesadmin/$project_name/$project_name/


