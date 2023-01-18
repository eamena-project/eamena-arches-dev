# EAMENA_2022-09-26_03-23-29.csv & resource_relationships.csv

These datasets are exported from the http://levant.eamena.training/ Arches v3 database with this search URL: 

http://levant.eamena.training/search?page=1&termFilter=%5B%5B%7B%22inverted%22%3Afalse%2C%22type%22%3A%22string%22%2C%22context%22%3A%22%22%2C%22context_label%22%3A%22%22%2C%22id%22%3A%22EAMENA-F%22%2C%22text%22%3A%22EAMENA-F%22%2C%22value%22%3A%22EAMENA-F%22%7D%5D%5D&temporalFilter=%5B%7B%22year_min_max%22%3A%5B%5D%2C%22filters%22%3A%5B%5D%2C%22inverted%22%3Afalse%7D%5D&spatialFilter=%7B%22geometry%22%3A%7B%22type%22%3A%22%22%2C%22coordinates%22%3A%5B%5D%7D%2C%22buffer%22%3A%7B%22width%22%3A%220%22%2C%22unit%22%3A%22m%22%7D%2C%22inverted%22%3Afalse%7D&mapExpanded=false&timeExpanded=false&booleanSearch=and&searchRelatedResources=false&termFilterAndOr=%5B%22and%22%5D&termFilterCombineWithPrev=%5B%5Bfalse%5D%5D&termFilterGroup=%5B%22No%20group%22%5D&advancedSearch=false&include_ids=true

These are HPs that must be imported into the EAMENA database. The result of this research is exported as a CSV.

The way to do this mapping, is to use the [eamenaR](https://github.com/eamena-project/eamenaR#bu-mapping) function `list_mapping_bu()` with the original exported CSV: `C:\Rprojects\eamena-arches-dev\data\bulk\bu\v3\EAMENA_2022-09-26_03-23-29.csv`