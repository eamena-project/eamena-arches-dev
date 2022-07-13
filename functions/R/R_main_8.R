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
source(paste0(dir_funct, "R_functions_3.R"))  # read the functions file

d_sql <- hash::hash() # hash instance to store the results
# con <- my_con("test")

# counts of HPs
d_sql <- count_hps("test", d_sql, "HPs_count")
d_sql$HPs_count

# UUID from EAMENA ID
d_sql <- uuid_from_eamenaid("eamena", "EAMENA-0187363", d_sql, "uuid")
d_sql$uuid

# subtree of Cultural Period (UUID: '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
d_sql <- list_cpts(con, d_sql, "CulturalPeriod_list", '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
plot(d_sql$CulturalPeriod_list)

#
d_sql <- uuid_from_eamenaid("eamena", "EAMENA-0187363", d_sql, "uuid")
d_sql <- list_culturalper("eamena", d_sql, "culturalper", d_sql$uuid)
