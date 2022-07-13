# miscellaneous of R functions

library(hash)
library(igraph)
library(stringr)
library(tidyr)

uuid_from_eamenaid <- function(db, eamenaid, d, field){
  # return the UUUID from EAMENA id
  sqll <- str_interp("SELECT t.tileid, t.resourceinstanceid,
     t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text like '%${eamenaid}%'")
  con <- my_con(db) # load the Pg connection
  df <- dbGetQuery(con, sqll)
  d[[field]] <- as.character(df$resourceinstanceid)
  dbDisconnect(con)
  return(d)
}

# count_hps(con.eamena, d_sql, "HPs_count")

count_hps <- function(db, d, field){
  # count Heritage Places (HPs)
  # Is 'con' useful?
  sqll <- "select count(
        tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
        ) as HPs_count FROM tiles;"
  print(sqll)
  con <- my_con(db) # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
}

#' collect fields: EAMENA_ID, ThreatCat, AssessType, AssessDate, resourceinstanceid
#' @name threats_hps
#' @description Read the DB and gather the different threats by HP. A join with the table 'values'
#' is needed since the 'tiles' table gathers principally UUID that must be translated
#' into human-readable values
#'
#' @param con a Pg connection
#' @param d a hash() object (a Python-like dictionary)
#' @param field the name of the field that will be created in the a hash() object
#' @return A hash() with all threats, dates, etc. stored in the field name
#'
#' @examples
#' d_sql <- hash::hash()
#' d_sql <- count_hps(con, d_sql, "HPs_count")
#'
#' @export
threats_hps <- function(con, d, field){
  sqll <- "
  SELECT
  tiles.tiledata ->> '34cfe992-c2c0-11ea-9026-02e7594ce0a0' as EamenaID,
  values1.value as ThreatCat,
  values2.value as ActivTyp,
  tiles.tiledata ->> '34cfea81-c2c0-11ea-9026-02e7594ce0a0' as AssessDat,
  resourceinstanceid as ResourceID
  FROM tiles
  LEFT JOIN values as values1 ON
  values1.valueid::text = tiledata ->> '34cfea76-c2c0-11ea-9026-02e7594ce0a0'
  LEFT JOIN values as values2 ON
  values2.valueid::text = tiledata ->> '34cfea4d-c2c0-11ea-9026-02e7594ce0a0'
  WHERE ((nodegroupid::text = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0')
		 OR (nodegroupid::text = '34cfe9fb-c2c0-11ea-9026-02e7594ce0a0')
		 OR (nodegroupid::text = '34cfe992-c2c0-11ea-9026-02e7594ce0a0')
		 OR (nodegroupid::text = '34cfea4d-c2c0-11ea-9026-02e7594ce0a0')
		)
  ORDER BY resourceid
  -- LIMIT 5000
  "
  con <- my_con() # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
}


#' List the name of all the child-concepts below a certain Concept node
#' @name list_cpts
#' @description With a given concept UUID (v. Reference Data Manager), find all
#' the childs
#'
#' @param con a Pg connection
#' @param d a hash() object (a Python-like dictionary)
#' @param field the field name that will be created in the a hash() object
#' @param uuid the UUID of the Concept parent
#'
#' @return A hash() with listed child-concepts in the provided field name
#'
#' @examples
#' '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4' is the UUID of ...
#'
#' d_sql <- hash::hash()
#' d_sql <- list_cpts(con, d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
#'
#' @export
list_cpts <- function(db, d, field, uuid){
  # field <- "CulturalPeriod_list"
  # uuid <- '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4'
  # db <- "eamena"
  sqll <- "
  SELECT conceptidfrom as from, conceptidto as to FROM relations
  "
  con <- my_con(db) # load the Pg connection
  relations <- dbGetQuery(con, sqll)
  # subset the Concepts graph on the selected UUID
  g <- graph_from_data_frame(relations, directed = TRUE)
  nodes.subgraph <- subcomponent(g, uuid, mode = "out")
  subgraph <- subgraph(g, nodes.subgraph)
  # get the name of the nodes from their UUID
  l.uuids <- as_ids(V(subgraph))
  for(uuid_ in l.uuids){
    # uuid_ <- "ea784c69-d61d-4bfc-9aa9-b3fb0bfa1b42"
    sqll <- str_interp("
    SELECT value FROM values
    WHERE conceptid = '${uuid_}'
    AND languageid = 'en-US'
    AND valuetype = 'prefLabel'
                       ")
    uuid_name <- dbGetQuery(con, sqll)
    uuid_name <- as.character(uuid_name)
    V(subgraph)$name[V(subgraph)$name == uuid_] <- uuid_name
  }
  d[[field]] <- subgraph
  dbDisconnect(con)
  return(d)
}


#' List the name of all the cultural period of a given HP
#' @name list_culturalper
#' @description With a given concept UUID (v. Reference Data Manager), find all
#' the cultural periods, subperiods, etc., of a given HP
#'
#' @param db the name of the database, by default 'eamena'
#' @param d a hash() object (a Python-like dictionary)
#' @param field the field name that will be created in the a hash() object
#' @param uuid the UUID of the HP
#'
#' @return A hash() with listed cultural periods names
#'
#' @examples
#'
#' d_sql <- hash::hash()
#' d_sql <- uuid_from_eamenaid("eamena", "EAMENA-0187363", d_sql, "uuid")
#' d_sql <- list_culturalper("eamena", d_sql, "culturalper", d_sql$uuid)
#'
#' @export
list_culturalper <- function(db = 'eamena', d, field, uuid){
  # d <- d_sql ; uuid <- '12053a2b-9127-47a4-990f-7f5279cd89da'; field <- "culturalper"
  sqll <- str_interp("
  SELECT tiledata ->> '38cff73b-c77b-11ea-a292-02e7594ce0a0' AS period,
  tiledata ->> '38cff73c-c77b-11ea-a292-02e7594ce0a0' AS subperiod
  FROM tiles
  WHERE resourceinstanceid = '${uuid}'
                     ")
  con <- my_con(db) # load the Pg connection
  df <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  periods <- as.character(na.omit(df$period))
  df.periods <- data.frame(uuid = periods,
                           name = rep(NA, length(periods)))
  subperiods <- as.character(na.omit(df$subperiod))
  df.subperiods <- data.frame(uuid = subperiods,
                              name = rep(NA, length(subperiods)))
  # call function
  df.periods <- name_from_uuid(db, df.periods)
  df.subperiods <- name_from_uuid(db, df.subperiods)
  # store in tibble
  df1 <- tibble(
    uuid = uuid,
    period = df.periods,
    subperiods= df.subperiods
    # cult_per = list(
    #   period = df.periods,
    #   df.subperiods= df.subperiods
    # )
  )
  d[[field]] <- df
  # dbDisconnect(con)
  return(d)
}

name_from_uuid <- function(db, df){
  con <- my_con(db) # load the Pg connection
  for(i in seq(1, nrow(df))){
    # i <- 1
    uuid_ <- df[i, "uuid"]
    sqll <- str_interp("
    SELECT value FROM values WHERE valueid = '${uuid_}'
                     ")
    name <- dbGetQuery(con, sqll)
    name <- as.character(name)
    df[i, "name"] <- name
  }
  dbDisconnect(con)
  return(df)
}


ref_culturalper <- function(){
  # create a list concepts below Cultural Period of all periods with their durations
  # write a CSV file
  # a periodo colum is added
  field.out <- "CulturalPeriod_list"
  d_sql <- list_cpts("eamena", d_sql, field.out, '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  g <- d_sql$CulturalPeriod_list
  leaves <- V(g)[degree(g, mode="out") == 0]
  leaves <- leaves$name # all the periods (and superiods?)

  # The Cultural periods are the leaves of the Concept list
  # df.equiv <- data.frame(eamena = leaves,
  #                        periodo = rep("", length(leaves)))
  write.table(df.equiv, paste0(getwd(),"/data/time/results/equivalences.tsv"), sep ="\t", row.names = F)

}



df.culturalper <- data.frame(ea.name = leaves,
                             ea.duration.taq = rep("", length(leaves)),
                             ea.duration.tpq = rep("", length(leaves)),
                             periodo = rep("", length(leaves)))
for(i in seq(1, length(leaves))){
  # i <- 1
  name <- leaves[i]
  print(paste(i, name))
  sqll <- str_interp("
    SELECT conceptid::text FROM values WHERE value = '${name}'
                     ")
  per.conceptid <- dbGetQuery(con, sqll)
  per.conceptid <- per.conceptid$conceptid
  df.name.duration <- data.frame(value = character(),
                                 # languageid = character(),
                                 valuetype = character())
  # there are two concepts for the same value, so it is needed to loop..
  for(conceptid in per.conceptid){
    sqll <- str_interp("
    SELECT value, valuetype FROM values WHERE conceptid = '${conceptid}'
                     ")
    res <- dbGetQuery(con, sqll)
    df.name.duration <- rbind(df.name.duration, res)
  }
  # The cultural period duration is recorded as "600 1200" in a scopeNote
  culturalper.duration <- df.name.duration[df.name.duration$valuetype == 'scopeNote', "value"]
  if(length(culturalper.duration) > 0){
    # some Cultural Periods haven't any scopeNote
    taq <- str_split(culturalper.duration, pattern = "\t")[[1]][1]
    tpq <- str_split(culturalper.duration, pattern = "\t")[[1]][2]
    df.culturalper <- rbind(df.culturalper, c(name, taq, tpq, ""))
  } else {
    print(paste(" - The period", name, "has no scopeNote (ie, no duration)"))
  }
  # df.name <- df.name.duration[df.name.duration$valuetype == 'scopeNote', "value"]
}



