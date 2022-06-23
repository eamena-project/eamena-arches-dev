# Training of a backend IT profile to assist a database manager on Arches v7

## Background and motivations

Our Jordanian colleagues have an Arches v5.2 instance based on EAMENA hosting their national data. This database is named 'Jordan Masdar'. This database will be updated to Arches v7. In parallel to this upgrade, another database named 'Mega-Jordan' will be converted to Arches v7. The two databases 'Jordan Masdar' and 'Mega-J' will then be merged into a single instance of the Arches v7 database. All these processes will be supported by Farallon and the EAMENA team (Oxford University). 
Farallon is expected to release Arches version 7 (Arches v7) in August 2022. Migrations from 'Jordan Masdar' and 'Mega-Jordan' to Arches v7 will take place after that date, most likely in late 2022. 

## Database manager role

Our Jordanian colleagues have already identified a point person for managing their Arches database. This database manager (DBM) has been trained by the EAMENA team. This DBM is primarily an archaeologist responsible for the content of the database. To assist this DBM, we are looking for an IT profile able to manage the back-end of an Arches v7 instance.

## New role: backend profile

We expect our Jordanian colleagues to hire a new person who will be trained in Arches v7 to maintain the server and who will be able to troubleshoot back-end issues (e.g., server, Elasticsearch) for the Arches database, supporting the DBM. This person will primarily interact with the Arches v7 database on the back-end, primarily with Linux and Python commands. This person will need to know how to use Linux CLI, query a Postgresql database, understand Django frameworks (Administration, Migrations, etc.), track errors on log files, etc. This person will need to be able to communicate and teach the DBM the causes of troubleshooting, how to identify them by interpreting error messages, create and share documentation on these error sources and fixes. This new profile will be expected to share their knowledge by documenting his/her work using structured files and computer scripts such as bash scripts. This new profile will be expected to value GitHub as a computing platform to share all software developments that can be opened to the public in the spirit of open science, and participate in the Arches user community.

The new backend specialist profile will be hired by our Jordanian colleagues based on these skills :

Professional background:

- Professional experience in IT
- Degree in computer science, preferably with a focus on systems administration, database administration, or database management.
- Be integrated in a Jordanian IT company (better a big than a small one)
- Proficiency in Arabic and English languages
- Communication/teaching skills

Computer skills:

- OS: Linux
- Servers : Ubuntu, Apache
- Programming languages: bash, Python
- Web application framework/model-view-controller: Django
- RDBMS: Postgresql/Postgis
- Standard file formats: JSON, GeoJSON, XML, HTML
- Version control system: Git, GitHub
- IDE : Visual Studio Code, or others

Nice-to-haves

- Key concepts: cloud computing, geo-web and GIS, semantic web, FAIR data.
- Programming language: JavaScript, CSS
- Databases: Arches, NoSQL or graph database
- Other software, frameworks or protocols: ElasticSearch, IIIF, Knockout.js, RESTful API, cURL, SSH/SSL

## Training proposal for the backend profile

The backend profile must be trained on:

- understanding the purpose, architecture and software stack of Arches.  
- [install Arches](https://arches.readthedocs.io/en/stable/requirements-and-dependencies/) on a Linux operating system  
- understand [project](https://arches.readthedocs.io/en/stable/projects-and-packages/#) and [packages](https://arches.readthedocs.io/en/stable/projects-and-packages/#understanding-packages)
    - understand the `settings.py` file.
    - understand resource models, ontologies, concepts and collections
- understand the [CLI reference](https://arches.readthedocs.io/en/stable/command-line-reference/#command-line-reference)
    - understand the main commands of the `manage.py` command: `bu`, `collectstatic`, `index_database`, `packages`, etc.
- backups
    - plan a backup under Linux
    - `dump` of Postgresql for raw data
    - exporting Arches packages to GitHub repositories
- usage of online and collaborative resources:
    - [Arches project](https://www.archesproject.org/)
    - [Arches software documentation](https://arches.readthedocs.io/en/stable/)
    - [Arches Project Community Forum](https://community.archesproject.org/)
    - [Arches GitHub](https://github.com/archesproject/arches)