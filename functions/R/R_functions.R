# miscellaneous of R functions

library(hash)

uuid_from_eamenaid <- function(eamenaid_pattern){
# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
    d_sql <- hash::hash() # hash instance
    d_sql[["HPs_count"]] <- paste0("SELECT t.tileid, t.resourceinstanceid,
     t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text like '%",
     eamenaid.pattern, "%'")
    return(d_sql)
}

summary_eamena <- function(){
# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
    d_sql <- hash::hash() # hash instance
    # count Heritage Places (HPs)
    d_sql[["HPs_count"]] <- "select count(
        tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
        ) as HPs_count FROM tiles;"
    return(d_sql)
}

threats_eamena <- function(){
  # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
  d_sql <- hash::hash() # hash instance
  # count Heritage Places (HPs)
  d_sql[["HPs_threats"]] <- "
  SELECT
  tiles.tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
  values.value as ThreatCat,
  tiles.tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssessDat,
  resourceinstanceid as ResourceID
  FROM tiles LEFT JOIN values ON
  values.valueid::text = tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0'
  WHERE ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0')
  OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0')
  OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
  ) --AND tiles IS NOT NULL
  LIMIT 100;"
  return(d_sql)
}

# summary_eamena <- function(){
#   # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
#   d_sql <- hash::hash() # hash instance
#   # count Heritage Places (HPs)
#   d_sql[["HPs_count"]] <- "select count(
#         tiledata->>'34cfea81-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
#         ) as HPs_count FROM tiles;"
#   return(d_sql)
# }




