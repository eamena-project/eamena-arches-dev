# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure

library(hash)

d.sql <- hash() # hash instance

# count Heritage Places (HPs)
d.sql[["HPs_count"]] <- "select
count(tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%')
as HPs_count FROM tiles;"

## Not run
# d.sql
