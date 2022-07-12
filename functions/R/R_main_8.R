# Main function to deal with the EAMENA DB
# this file has to remain a minimal example of what do the functions
# for further analysis, create a separated document

library(RPostgreSQL)
library(DBI)
library(dplyr)
library(plotly)
library(lubridate)
library(htmlwidgets)

dir_funct <- paste0(getwd(), "/functions/R/")
source(paste0(dir_funct, "_conn.R"))        # read the secret credential
source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

d_sql <- hash::hash() # hash instance to store the results

# counts of HPs
d_sql <- count_hps(con, d_sql, "HPs_count")
d_sql$HPs_count

# subtree of Cultural Period (UUID: '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
d_sql <- list_cpts(con, d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
plot(d_sql$CulturalPeriod_list)
#
# E(d_sql$CulturalPeriod_list)
#
# edges.cultural.period <- as_data_frame(d_sql$CulturalPeriod_list, what="edges")
#
# library(collapsibleTree)
# tree.edges.cultural.period <- collapsibleTree(edges.cultural.period, c("from", "to"), collapsed = FALSE)
# getwd()
