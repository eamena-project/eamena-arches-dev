library(RPostgreSQL)
library(DBI)
library(dplyr)

# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure

dir_funct <- paste0(getwd(), "/functions/R/")
source(paste0(dir_funct, "_conn.R"))        # read the secret credential
source(paste0(dir_funct, "R_functions_1.R"))  # read the functions file

# con <- my_con() # load the Pg connection

d_sql <- hash::hash() # hash instance to store the results


# d_sql <- summary_eamena() # load a dict type

# counts of HPs
d_sql <- count_hps(con, d_sql, "HPs_count")
d_sql$HPs_count

# threats and dates
d_sql <- threats_hps(con, d_sql, "HPs_treats")
d_sql$HPs_treats

# Use dplyr to group the data and keep the non-NA value from the other columns.
df_threats_hps <- d_sql$HPs_treats %>% group_by(resourceid) %>%
  summarise(eamenaid = max(eamenaid, na.rm = T),
            threatcat = max(threatcat, na.rm = T),
            assessdat = max(assessdat, na.rm = T))

# sum(duplicated(df_threats_hps$))

#
# # dbDisconnect(con.eamena)
#
# # Create sample data frame.
# id <- c(rep('Participant 1', 2), rep('Participant 2', 2))
# value1 <- rep('A', 4)
# value2 <- rep('B', 4)
# value3 <- rep('C', 4)
# value4 <- c('x', NA, NA, 'x')
# value5 <- c('x', NA, 'x', NA)
# value6 <- c(NA, 'x', NA, 'x')
#
# df <- data.frame(id, value1, value2, value3, value4, value5, value6, stringsAsFactors = F)
#
# # Use dplyr to group the data and keep the non-NA value from the other columns.
# df %>% group_by(id, value1, value2, value3) %>%
#   summarise(value4 = max(value4, na.rm = T),
#             value5 = max(value5, na.rm = T),
#             value6 = max(value6, na.rm = T))
