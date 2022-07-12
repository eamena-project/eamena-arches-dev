# miscellaneous of R functions

library(hash)
library(igraph)
library(stringr)

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


#' List the name of all the child-concepts below a certain node
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
#' d_sql <- hash::hash()
#' d_sql <- list_cpts(con, d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
#'
#' @export
list_cpts <- function(con, d, field, uuid){
  # uuid <- '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4'
  sqll <- "
  SELECT conceptidfrom as from, conceptidto as to FROM relations
  "
  # sqll <- "
  # SELECT conceptidto as childs FROM relations
  # WHERE conceptidfrom = '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4'
  # "
  con <- my_con() # load the Pg connection
  relations <- dbGetQuery(con, sqll)



  # library(castor)
  # library(alakazam)
  # library(ape)

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

  #
  #
  # library(stringr)
  #
  # V(subgraph)$name[V(subgraph)$name == 'ea784c69-d61d-4bfc-9aa9-b3fb0bfa1b42'] <- 'Chalcolithic'
  #
  # get.vertex.attribute(subgraph, "name", index=V(subgraph))
  #
  # subgraph<-minimum.spanning.tree(subgraph)
  #
  #
  # grps <- split(dfTest, ~ cumsum(!isLeaf))
  #
  # edges <- do.call(
  #   rbind,
  #   lapply(
  #     grps,
  #     function(x) {
  #       with(x, expand.grid(from = node[!isLeaf],
  #                           to = node[isLeaf]))
  #     }
  #   )
  # )
  #
  # for (k in seq_along(grps)) {
  #   if (nrow(grps[[k]]) == 1) {
  #     lleaf <- with(grps[[k + 1]], node[!isLeaf])
  #     rleaf <- with(grps[[k + 2]], node[!isLeaf])
  #     edges <- rbind(edges, data.frame(from = grps[[k]]$node, to = c(lleaf, rleaf)))
  #   }
  # }
  #
  # edges <- `row.names<-`(edges[with(edges, order(from, to)), ], NULL)
  #
  #
  #
  #
  #
  #
  #
  #
  # induced_subgraph(g, c(uuid, neighbors(g,1)))
  #
  # tree <- unfold_tree(g, roots=uuid)
  # g.tree <- ape::as.phylo(g)
  #
  # g.sub <- subcomponent(g, uuid, mode = "out")
  # g.childs <- bfs(g, uuid,
  #                 mode="out",
  #                 unreachable=FALSE)
  # subtree <- get_subtree_at_node(g, uuid)$subtree
  #
  #
  # for(i in df$childs)
  #   d[[field]] <- dbGetQuery(con, sqll)
  # dbDisconnect(con)
  # return(d)
}

# g <- make_tree(10) %du% make_tree(10)
# V(g)$id <- seq_len(vcount(g))-1
# roots <- sapply(decompose(g), function(x) {
#   V(x)$id[ topo_sort(x)[1]+1 ] })
# tree <- unfold_tree(g, roots=roots)
# lay <- layout_as_tree(g)
# plot(as.undirected(tree), layout = lay %*% diag(c(1, -1)))


# summary_eamena <- function(){
#   # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
#   d_sql <- hash::hash() # hash instance
#   # count Heritage Places (HPs)
#   d_sql[["HPs_count"]] <- "select count(
#         tiledata->>'34cfea81-c2c0-11ea-9026-02e7594ce0a0' like '%EAMENA%'
#         ) as HPs_count FROM tiles;"
#   return(d_sql)
# }




