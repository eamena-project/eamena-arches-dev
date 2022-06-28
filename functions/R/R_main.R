library(RPostgreSQL)
library(DBI)

dir_funct <- paste0(getwd(), "/functions/R/")

source(paste0(dir_funct, "_conn.R")) # read the functions file
source(paste0(dir_funct, "R_functions.R")) # read the functions file

d_sql <- summary_eamena() # load a dict type
hps_count <- dbGetQuery(con.eamena, d_sql[["HPs_count"]])
hps_count # count of HPs

dbDisconnect(con.eamena)
