| Task | 3->5 | 5->7 |
|------|-------|-------|
| Export data structures from old database  | Up | Up |
| Install new version of Arches on a test box  | Up | Up |
| Develop/convert data structures in new database  | Up | Up |
| Develop/convert EAMENA customisations  | Up | Up |
| Export a subset of data from old database  | Down | Up |
| Determine changes to be made to data  | Down | Up |
| Write automated scripts to convert data  | Down | Up |
| Convert a subset of data using test script  | Down | Up |
| Install correct version of Python, Django, PostgreSQL, etc | Down | Up |
| Install new database on AWS   | Down | Up |
| Install new data structures into new database  | Down | Up |
| Apply EAMENA customisations to the database  | Down | Up |
| Export complete data from old database (test run) | Down | Up |
| Import complete data into new database (test run) | Down | Up |
| Export complete data from old database   | Down | Down |
| Import complete data into new database   | Down | Down |
| Perform the 'switch' (eg server certificates, domain name, etc)   | Down | Down |


## Still to do (2023-03-22)

### If time is tight
* A complete test export/import of the data.
	* This will not require the existing DB to be shut off
	* This will take a few days
	* Assuming success, the length of time this process takes will be the same as the time the database server needs to be turned off
	* AWS test server will need to be up for the duration
* The actual import/export of the data
	* I anticipate this will take a few days, but if I've done my job right it'll be automatic and can therefore be set going last thing on a Friday and run over the weekend.
	* We will give a week's notice before this is to happen, so people can reach a suitable break in their work involving the database.

### If time isn't tight
* All of the above
* Upgrade to 7.4 (currently 7.3)
* A few more partial export/imports using the AWS server.
* Some heavy stress testing
* Proper bulk uploader UI implementation, as the ETL manager doesn't appear to work.
* Experiment with the EAMENA card - this was developed for 5.2/3 and never worked with 7. However a card with very similar (but not identical) functionality was created as part of core Arches. It has since come to my attention that Mike Fisher at MAPSS has paid Farallon to convert my old code to work with 7, and has been good enough to open source the result, so we can keep the identical functionality.
* 
