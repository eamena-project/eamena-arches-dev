# miscellaneous of R functions

library(hash)

uuid_from_eamenaid <- function(eamenaid_pattern){
  d_sql[["HPs_count"]] <- paste0("SELECT t.tileid, t.resourceinstanceid,
     t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text like '%",
                                 eamenaid.pattern, "%'")
  return(d_sql)
}

# count_hps(con.eamena, d_sql, "HPs_count")

count_hps <- function(con, d, field){
  # count Heritage Places (HPs)
  sqll <- "select count(
        tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
        ) as HPs_count FROM tiles;"
  con <- my_con() # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
}

threats_hps <- function(con, d, field){
  sqll <- "
  SELECT
  tiles.tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
  tiles.tiledata ->> 'ab02796c-c5da-4f36-af69-ed1f7fdc903e' as ActivTyp,
  values.value as ThreatCat,
  tiles.tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssesDat,
  resourceinstanceid as ResourceID
  FROM tiles LEFT JOIN values ON
  values.valueid::text = tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0'
  WHERE ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0') OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
  )
  ORDER BY resourceid
  LIMIT 60;"
  con <- my_con() # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
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




