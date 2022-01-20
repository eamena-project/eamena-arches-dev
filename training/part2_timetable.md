# Jordan training 2/2

This is the second part of Database Management training for Arches-powered platform, EAMENA compliant, for cultural heritage management. The previous part (part 1) took place in person, in Amman, Jordan (5/11/21 - 9/11/21). This part 2  consists of 3 different slots of 3-hours each:
1. Slot 1: Documentation and installation
2. Slot 2: Navigate through administration tools
3. Slot 3: Edit as a Database Manager

This online training will take place online (app to be defined)

* Requirements before the start of this the training:
  - one person for each country (Jordan, Lebanon, Palestine) with:
    + its computer IP (for AWS firewall)
    + PuTTY installed
    + Filezilla installed

---

## Slot 1 (3-hours)

Use available documentation. Install AWS server, Arches core, HTTP Apache, and project

### Documentation

* Part 1 slides:
  - day 1: https://docs.google.com/presentation/d/1k9JMuj5oSZXHO3Z9RSVMogn4CUSJ1EK8Plus8sK7xDo/edit#slide=id.g103cf15c0a6_0_296
  - day 2: https://docs.google.com/presentation/d/1zsqCzLDIotaShU9OUXg4tMWfaTrMF5fF5bZoLuhavKs/edit#slide=id.p
  - day 3: https://docs.google.com/presentation/d/16wjDpFGCn20tQcDdjrchhp9ZJiJvJsL6dKlF_rH-QjI/edit#slide=id.p
  - day 4: https://docs.google.com/presentation/d/1ki9Uefiop3SG3qOrLHUYrjzTekoaLXK5Iy2bMiFR0kM/edit#slide=id.p
  - day 5: https://docs.google.com/presentation/d/1G_2cqayQZDrL68W9Fcs1UIKRaSBW1k8YhnkKAysJ-zM/edit#slide=id.p
  
* University of Oxford
  - dropbox: https://www.dropbox.com/home/EAMENA/Trainings/2112CPFJordan
  - GitHub: https://github.com/eamena-oxford

#### Arches

* project: https://www.archesproject.org/
* documentation: https://arches.readthedocs.io/en/stable/
* forum: https://community.archesproject.org/
* GitHub: https://github.com/archesproject/arches
* development: https://www.archesproject.org/development/

#### EAMENA

* *to be completed*

### Installations

#### AWS server

* install a new AWS machine (AMI)
  - create Security Group (sg-)
    + firewall (inbounds and outbounds rules)
  - backups
  
#### Arches and Apache

* install Arches 
  - Postgres
  - Celery
  - couchDB
  - yarn
  - Elasticsearch
  - ...

* install Apache

#### EAMENA model

* install EAMENA package

---

## Slot 2 (3-hours)

Understand the administration of an Arches-powered database management platform.  

### Read Arches/EAMENA

#### EAMENA model

* Manage System Settings
  - System settings
  - System Settings Graph (Graph Designer)

* Add New Resource
  - Built Component
  - Detailed Condition Assesment
  - ...
  - Heritage Place
  - ...
  
* Arches designer
  - Resource Models
  - Branches
  
* Map Layer Manager
  - Heritage Place
  
* Profile Manager

### Django Admin

* *to be completed*

---

## Slot 3 (3-hours)

### Write and Run Arches/EAMENA

* load packages
  - import_business_data
  
* create packages
  - create_mapping_file
  - export business data
  
* edit Cards

* moving Arches/project 
  - between to different AWS accounts
  - between AWS and local server



* *to be completed*
  

