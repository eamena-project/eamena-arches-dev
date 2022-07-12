library(RPostgreSQL)
library(DBI)

dir_funct <- paste0(getwd(), "/functions/R/")

source(paste0(dir_funct, "_conn.R"))        # read the secret credential
source(paste0(dir_funct, "R_functions.R"))  # read the functions file

d_sql <- summary_eamena() # load a dict type

# counts of HPs
hps_count <- DBI::dbGetQuery(con.eamena, d_sql[["HPs_count"]])
hps_count

# threats and dates
hps_threats <- DBI::dbGetQuery(con.eamena, d_sql[["HPs_treats"]])
hps_threats

dbDisconnect(con.eamena)
