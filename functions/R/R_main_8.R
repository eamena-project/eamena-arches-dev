# Main function to deal with the EAMENA DB
# this file has to remain a minimal example of what do the functions
# these are example
# for further analysis, create a separated document

library(RPostgreSQL)
library(DBI)
library(dplyr)
library(plotly)
library(lubridate)
library(htmlwidgets)

dir_funct <- paste0(getwd(), "/functions/R/")
source(paste0(dir_funct, "_conn.R"))        # read the secret credential
source(paste0(dir_funct, "R_functions_6.R"))  # read the functions file

d_sql <- hash::hash() # hash instance to store the results

cultural.periods <- T
if(cultural.periods){
  # UUID of a HP from its EAMENA ID..
  # d_sql <- uuid_from_eamenaid(db = "eamena", d_sql, "EAMENA-0187363", "uuid")
  # TODO: trong long, v. Arches Forum
  ea.ids <- geojson_get_field("https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/caravanserail.geojson",
                    "EAMENA.ID")
  d_sql <- uuid_from_eamenaid(db = "eamena", d_sql, ea.ids, "uuid")
  # d_sql <- uuid_from_eamenaid(db = "eamena", d_sql, c("EAMENA-0187363", "EAMENA-0184752", "EAMENA-0076769"), "uuid")
  d_sql[["uuid"]] # "12053a2b-9127-47a4-990f-7f5279cd89da"

  # get its periods and subperiods UUIDs
  d_sql <- list_culturalper(db = "eamena", d = d_sql, field = "culturalper", uuid = d_sql[["uuid"]])
  d_sql$culturalper
  # plot the cultural period time span
  plot_cultural_periods(d = d_sql, field = "culturalper", export.plot = T)
}

display.refdata <- F
if(display.refdata){
  # subtree of Cultural Period (UUID: '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  d_sql <- list_cpts(db == "eamena", d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  plot(d_sql$CulturalPeriod_list)

  # plot the tree of the cultural periods
  tree_concepts(d = d_sql, field = "CulturalPeriod_list")
}

basic.statistics <- F
if(basic.statistics){
  # counts of HPs
  d_sql <- count_hps("eamena", d_sql, "HPs_count")
  d_sql$HPs_count
}


#

