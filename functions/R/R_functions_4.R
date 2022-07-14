# miscellaneous of R functions

library(hash)
library(igraph)
library(stringr)
library(tidyr)
library(plotly)

raw.GH <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/"


#' Return the UUID of a HP from EAMENA id
#' @name uuid_from_eamenaid
#' @description Return the UUID of a HP from EAMENA id and store it into a hash() object
#' alongside the EAMENA id
#'
#' @param db the name of the database, by default 'eamena'
#' @param d a hash() object (a Python-like dictionary)
#' @param eamenaid a EAMENA ID (eg. "EAMENA-0187363")
#' @param field.uuid the name of the field that will be created in the a hash() object
#' for the UUID
#' @param field.eamenaid the name of the field that will be created in the a hash() object
#' for the EAMENA ID
#' @return a hash() object (a Python-like dictionary) with EAMENA ID and UUID
#'
#' @examples
#' d_sql <- hash::hash() # hash instance to store the results
#' d_sql <- uuid_from_eamenaid("eamena", d_sql, "EAMENA-0187363")
#'
#' @export
uuid_from_eamenaid <- function(db, d, eamenaid, field.uuid = "uuid", field.eamenaid = "eamenaid"){
  if(length(eamenaid) == 1){
    sqll <- str_interp("SELECT t.tileid, t.resourceinstanceid,
     t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text LIKE '%${eamenaid}%'")
  }
  if(length(eamenaid) > 1){
    eamenaids <- paste0(eamenaid, collapse = "|")
    sqll <- str_interp("SELECT t.tileid, t.resourceinstanceid,
     t.tiledata, n.nodeid
    FROM tiles t LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
    WHERE (t.tiledata::json -> n.nodeid::text)::text similar to '%(${eamenaids})%';")
    print(sqll)
  }
  con <- my_con(db) # load the Pg connection
  df <- dbGetQuery(con, sqll)
  d[[field.eamenaid]] <- eamenaid
  d[[field.uuid]] <- as.character(df$resourceinstanceid)
  dbDisconnect(con)
  return(d)
}

#' Basic statistic on EAMENA heritage places
#' @name count_hps
#' @description Count the number of HP, ...
#'
#' @param db the name of the database, by default 'eamena'
#' @param d a hash() object (a Python-like dictionary)
#' @param field the name of the field that will be created in the a hash() object
#' @return Basic statistics
#'
#' @examples
#' d_sql <- hash::hash()
#' d_sql <- count_hps(con, d_sql, "HPs_count")
#'
#' @export
count_hps <- function(db, d, field){
  # count Heritage Places (HPs)
  sqll <- "select count(
        tiledata->>'34cfe992-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
        ) as HPs_count FROM tiles;"
  con <- my_con(db) # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
}

#' The threats on HP
#' @name threats_hps
#' @description Read the DB and gather the different threats by HP. A join with the table 'values'
#' is needed since the 'tiles' table gathers principally UUID that must be translated
#' into human-readable values. Collect fields: EAMENA_ID, ThreatCat, AssessType,
#' AssessDate, resourceinstanceid
#'
#' @param db a Pg connection
#' @param d a hash() object (a Python-like dictionary)
#' @param field the name of the field that will be created in the a hash() object
#' @return A hash() with all threats, dates, etc. stored in the field name
#'
#' @examples
#'
#' @export
threats_hps <- function(db, d, field){
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
  con <- my_con(db) # load the Pg connection
  d[[field]] <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  return(d)
}


#' List the name of all the child-concepts below a certain Concept node
#' @name list_cpts
#' @description With a given concept UUID (v. Reference Data Manager), find all
#' the childs
#'
#' @param db the name of the database, by default 'eamena'
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
#' d_sql <- list_cpts("eamena", d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
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
  SELECT
  tiledata ->> '38cff73b-c77b-11ea-a292-02e7594ce0a0' AS periods,
  tiledata ->> '38cff738-c77b-11ea-a292-02e7594ce0a0' AS periods_certain,
  tiledata ->> '38cff73c-c77b-11ea-a292-02e7594ce0a0' AS subperiods,
  tiledata ->> '38cff73a-c77b-11ea-a292-02e7594ce0a0' AS subperiods_certain
  FROM tiles
  WHERE resourceinstanceid = '${uuid}'
                     ")
  con <- my_con(db) # load the Pg connection
  df <- dbGetQuery(con, sqll)
  dbDisconnect(con)
  periods <- df[!(is.na(df$periods) | df$periods == ""), ]
  df.periods <- data.frame(eamenaid = rep(d$eamenaid, nrow(periods)),
                           periods = periods$periods,
                           periods.certain = periods$periods_certain,
                           name.periods = rep(NA, nrow(periods)),
                           name.periods.certain = rep(NA, nrow(periods))
  )
  subperiods <- df[!(is.na(df$subperiods) | df$subperiods == ""), ]
  df.subperiods <- data.frame(eamenaid = rep(d$eamenaid, nrow(subperiods)),
                              subperiods = subperiods$subperiods,
                              subperiods.certain = subperiods$subperiods_certain,
                              name.subperiods = rep(NA, nrow(subperiods)),
                              name.subperiods.certain = rep(NA, nrow(subperiods))
  )
  # function CALL
  df.periods <- name_from_uuid(db = db, df = df.periods,
                               uuid.in = "periods", field.out = "name.periods")
  df.periods <- name_from_uuid(db = db, df = df.periods,
                               uuid.in = "periods.certain", field.out = "name.periods.certain")
  # --
  df.subperiods <- name_from_uuid(db = db, df = df.subperiods,
                                  uuid.in = "subperiods", field.out = "name.subperiods")
  df.subperiods <- name_from_uuid(db = db, df = df.subperiods,
                                  uuid.in = "subperiods.certain", field.out = "name.subperiods.certain")
  # --
  # store in tibble
  df.tibble <- tibble(
    uuid = uuid,
    period = df.periods,
    subperiods= df.subperiods
  )
  d[[field]] <- df.tibble
  # dbDisconnect(con)
  return(d)
}

#' Plot the duration of EAMENA HP in a plotly chart
#' @name plot_cultural_periods
#' @description
#'
#' @param d a hash() object (a Python-like dictionary)
#' @param field the field name where the periods, subperiods, etc. will be read in the a hash() object
#' @param export.plot if True, export as HTML widget
#'
#' @return A plotly chart to display or save
#'
#' @examples
#'
#' d_sql <- hash::hash() # hash instance to store the results
#' d_sql <- uuid_from_eamenaid("eamena", "EAMENA-0187363", d_sql, "uuid")
#' d_sql <- list_culturalper(db = "eamena", d = d_sql, field = "culturalper", uuid = d_sql[["uuid"]])
#' plot_cultural_periods(d = d_sql, field = "culturalper", export.plot = TRUE)
#'
#' @export
plot_cultural_periods <- function(d, field, export.plot = F){
  # field = "culturalper" ; d <- d_sql ;
  df.all <- d[[field]]
  # nb of HP
  hps <- unique(d[[field]]$period$eamenaid)
  nb.hps <- length(hps)
  cultural_periods <- read.table(paste0(raw.GH, "data/time/results/cultural_periods.tsv"),
                                 sep = "\t", header = T)
  for(hp in seq(1, nb.hps)){
    # hp <- 1
    a.hp <- hps[hp] # get a EAMENA id
    df <- df.all$period[df.all$period$eamenaid == a.hp, ]
    # df.periods <- df$period
    # only useful columns
    df.periods <- df[, c("name.periods", "name.periods.certain")]
    time.table <- merge(df.periods, cultural_periods, by.x = "name.periods", by.y = "ea.name", all.x = TRUE)
    # get unique cultural periods
    time.table <- time.table[!duplicated(time.table), ]
    time.table$ea.duration.taq <- as.numeric(as.character(time.table$ea.duration.taq))
    time.table$ea.duration.tpq <- as.numeric(as.character(time.table$ea.duration.tpq))
    # time.table <- sapply(time.table[, c("ea.duration.taq", "ea.duration.tpq")], as.numeric)
    # plot
    gplotly <- plot_ly()
    for(i in seq(1, nrow(time.table))){
      # thedifferent boxes
      # i <- 1
      # 4 points to create a rectangle
      per <- c(rep(time.table[i, "ea.duration.taq"], 2),
               rep(time.table[i, "ea.duration.tpq"], 2))
      per <- as.numeric(per)
      lbl <- paste0("<b>", time.table[i, "name.periods"], "</b><br>",
                    time.table[i, "ea.duration.taq"], " to ", time.table[i, "ea.duration.tpq"], " ANE")
      gplotly <- gplotly %>%
        add_polygons(x = per,
                     # x=c(per1,per2,per3,per4),
                     # x=c(periodes.df$tpq, periodes.df$tpq, periodes.df$taq, periodes.df$taq),
                     y = c(hp-1, hp, hp, hp-1),
                     line = list(width=1)
        ) %>%
        # the name in the rectangle centre
        add_annotations(x = mean(per),
                        y = hp/2.5,
                        text = lbl,
                        font = list(size=12),
                        showarrow = FALSE,
                        inherit = T)
    }
    # the name of the EAMENA HP
    centre.eamena.id <- mean(c(time.table$ea.duration.taq, time.table$ea.duration.tpq))
    gplotly <- gplotly %>%
      add_annotations(x = centre.eamena.id,
                      y = hp/1.5,
                      text = a.hp,
                      font = list(size=16),
                      showarrow = FALSE,
                      inherit = T)
  }
  gplotly <- gplotly %>%
    layout(yaxis = list(title = "Cultural periods",
                        showgrid = FALSE,
                        showticklabels = FALSE,
                        zeroline = FALSE))
  if(export.plot){
    htmlwidgets::saveWidget(as_widget(gplotly), paste0(getwd(), "/data/time/results/cultural_period.html"))
  } else {
    gplotly
  }
}











#' Get the name (eg, of Cultural Periods) from their UUID
#' @name name_from_uuid
#' @description This function is run by list_culturalper()
#'
#' @param db the name of the database, by default 'eamena'
#' @param df a dataframe with at least a colum 'uuid'
#' @param uuid.in the UUID column to read, by default 'uuid'
#' @param field the name of the dataframe field that will be filled with names
#'
#' @return a dataframe with the UUID and the name (eg, of Cultural Periods)
#'
#' @examples
#'
#' @export
name_from_uuid <- function(db = "eamena", df, uuid.in = "uuid", field.out = "name"){
  # uuid = "periods" ; df = df.periods ; field = "name.periods"
  con <- my_con(db) # load the Pg connection
  for(i in seq(1, nrow(df))){
    # i <- 1
    uuid_ <- df[i, uuid.in]
    sqll <- str_interp("
    SELECT value FROM values WHERE valueid = '${uuid_}'
                     ")
    name <- dbGetQuery(con, sqll)
    name <- as.character(name)
    df[i, field.out] <- name
  }
  dbDisconnect(con)
  return(df)
}

#' Create a list of child-concepts below Cultural Period of all periods with their durations
#' @name ref_culturalper
#' @description create a list concepts below Cultural Period of all periods
#' with their durations. If 'overwrite' then write a CSV file
#'
#' @param overwrite overwrite the reference table
#'
#' @return NA
#'
#' @examples
#'
#' @export
ref_culturalper <- function(overwrite = F){
  # create a list concepts below Cultural Period of all periods with their durations
  # write a CSV file
  # a periodo colum is added
  field <- "CulturalPeriod_list"
  d_sql <- list_cpts("eamena", d_sql, field, '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  g <- d_sql$CulturalPeriod_list
  leaves <- V(g)[degree(g, mode="out") == 0]
  leaves <- leaves$name # all the periods (and superiods?)
  if(overwrite){
    df.culturalper <- data.frame(ea.name = leaves,
                                 ea.duration.taq = rep("", length(leaves)),
                                 ea.duration.tpq = rep("", length(leaves)),
                                 periodo = rep("", length(leaves)))
    for(i in seq(1, length(leaves))){
      # i <- 2
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
        df.culturalper[i, ] <- c(name, taq, tpq, "")
      } else {
        print(paste(" - The period", name, "has no scopeNote (ie, no duration)"))
      }
      write.table(df.culturalper, paste0(getwd(),"/data/time/results/cultural_periods.tsv"), sep ="\t", row.names = F)
      # df.name <- df.name.duration[df.name.duration$valuetype == 'scopeNote', "value"]
    }
  }
  return(leaves)
}

#' Create an interactive tree for a given Concept and its concepts-child
#' (eg: 'Cultural Period')
#' @name tree_concepts
#' @description Read the arborescence of concept below of a given concept,
#' creates a collapsibleTree. Plot it by defaut, but if 'export.tree' will
#' export it
#'
#' @param db the name of the database, by default 'eamena'
#' @param d a hash() object (a Python-like dictionary)
#' @param field the field name that will be created in the a hash() object and
#' the name of the collapsibleTree if exported
#' @param export.tree if True, export the tree as a HTML widget

#' @return a plot or a HTML widget of the tree
#'
#' @examples
#'
#' @export
tree_concepts <- function(db = "eamena", d, field, export.tree = F){
  # TODO: put UUID in the function options
  d <- list_cpts(db, d, field, '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  g <- d[[field]]
  leaves <- V(g)[degree(g, mode="out") == 0]
  leaves <- leaves$name # all the periods (and superiods?)
  # format for collapsibleTree
  edges.cultural.period <- as_data_frame(g, what = "edges")
  edges.cultural.period$root <- "cultural.period"
  edges.cultural.period <- edges.cultural.period[edges.cultural.period$from != "Cultural Period", ]
  tree.edges.cultural.period <- collapsibleTree(edges.cultural.period,
                                                hierarchy = c("root", "from", "to"),
                                                root = "Thesauri",
                                                c("from", "to"),
                                                collapsed = FALSE,
                                                width = 1200,
                                                height = 900)
  if(export.tree){
    saveWidget(as_widget(tree.edges.cultural.period),
               paste0(getwd(),"/data/time/results/",
                      filed.out, ".html"))
  } else {
    # plot
    tree.edges.cultural.period
  }
}







