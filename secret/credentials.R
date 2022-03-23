library(RPostgreSQL)
library(DBI)

drv <- dbDriver("PostgreSQL")

# DOES NOT WORK!
# test masdar, aka 23test
con.masdar <- dbConnect(drv,
                        user = 'postgres',
                        password = 'postgis',
                        dbname = 'masdar-test',
                        host = 'ec2-54-74-247-130.eu-west-1.compute.amazonaws.com',
                        port = 5432)


# EAMENA prod
con.eamena <- dbConnect(drv,
                        user = 'postgres',
                        password = 'postgis',
                        dbname = 'eamena',
                        host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                        port = 5432)


