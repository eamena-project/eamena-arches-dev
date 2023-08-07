# Instalation of a training instance

## AWS EC2 instance

Ubuntu 22
r6g.large
IP: 54.247.46.210

Host EA-training-instance
  HostName 54.247.46.210
  IdentityFile "C:/Users/Thomas Huet/Desktop/EAMENA/IT/keys/EA_training.pem"
  User ubuntu

## Install Arches v7

* create 'arches' user in `opt/arches`

* sudo apt-get update

* install [Postgres](https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/install/prerequisites/PostgreSQL.md#download-postgresql)
