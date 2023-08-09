
Arches 7.3 requires Python 3.8.10 or 3.10.12 (tested).


## Virtual environment

* install Python VE
	- `sudo apt-get install python3-virtualenv`
	- `sudo apt-get install virtualenv`
	- create `ENV/` under `opt/arches/ENV/`
	- as arches user, run: `virtualenv --python=/usr/bin/python3 ENV`
	- activate the VE `source ENV/bib/activate`