library(RPostgreSQL)
library(DBI)

source(paste0(getwd(), "/select/select.R")) # read the SQL queries

drv <- dbDriver("PostgreSQL")

con <- dbConnect(drv,
                 user = 'xxx',
                 password = 'xxx',
                 dbname = 'eamena',
                 host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                 port = 5432)
# dbListTables(con)
HPs_count <- dbGetQuery(con, d.sql[["HPs_count"]])

HPs_count # count of HPs

dbDisconnect(con)
