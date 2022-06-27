library(RPostgreSQL)
library(DBI)

source(paste0(getwd(), "/functions/R_functions.R")) # read the functions file
source(paste0(getwd(), "/functions/_conn")) # read the functions file

hps_count <- dbGetQuery(con.masdar, d_sql[["HPs_count"]])

hps_count # count of HPs

dbDisconnect(con.eamena)
