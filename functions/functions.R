# miscellaneous of R functions

library(hash)

uuid.from.eamenaid <- function(eamenaid.pattern){
    # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
    d.sql <- hash() # hash instance
    d.sql[["HPs_count"]] <- paste0("SELECT t.tileid, t.resourceinstanceid, t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text like '%", eamenaid.pattern,"%'")
    return(d.sql)
}

summary.eamena <- function(){
    # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
    d.sql <- hash() # hash instance
    # count Heritage Places (HPs)
    d.sql[["HPs_count"]] <- "select count(tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%') as HPs_count FROM tiles;"
    return(d.sql)
}


