library(RPostgreSQL)
library(DBI)
library(dplyr)
library(plotly)


# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure

dir_funct <- paste0(getwd(), "/functions/R/")
source(paste0(dir_funct, "_conn.R"))        # read the secret credential
source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

# con <- my_con() # load the Pg connection

d_sql <- hash::hash() # hash instance to store the results


# d_sql <- summary_eamena() # load a dict type

# counts of HPs
d_sql <- count_hps(con, d_sql, "HPs_count")
d_sql$HPs_count

# threats and dates
d_sql <- threats_hps(con, d_sql, "HPs_treats")
#  View(d_sql$HPs_treats)

df_threats_hps <- d_sql$HPs_treats

out_df <- df_threats_hps[0,]
out_df$activtyp <- out_df$resourceid <- NULL
nb_tot <- length(unique(df_threats_hps$resourceid))
print(paste("run on", nb_tot, "different HP"))
ct <- 0
for (i in unique(df_threats_hps$resourceid)){
  # TODO: the removal of Field-based is partly arbitrary
  # the problem is to relate a threatcat with a date
  # i <- "000c8925-af3b-4dc4-8047-e48725648d7c"
  ct <- ct + 1
  if (ct %% 1000 == 0){print(paste0("   - ", ct, "/", nb_tot))}
  df <- df_threats_hps[df_threats_hps$resourceid == i, ]
  df <- df[df$activtyp != "Field-based" | is.na(df$activtyp), ]
  eamenaid <- max(as.character(na.omit(df$eamenaid))) # 1 max, to improve
  assessdat <- max(df$assessdat, na.rm = T) # 1 max, to improve
  threatcat <- as.character(na.omit(df$threatcat)) # > 1 max
  # fill the out_df
  for (j in threatcat){
    out_df[nrow(out_df)+1, "eamenaid"] <- eamenaid
    out_df[nrow(out_df), "threatcat"] <- j
    out_df[nrow(out_df), "assessdat"] <- assessdat
  }
}

save(out_df, file = "out_df.RData")

# clean the df
out_df_clean <- out_df[out_df$threatcat != "Not Applicable", ]
out_df_clean <- out_df_clean[!is.na(out_df_clean$assessdat), ]

save(out_df_clean, file = "out_df_clean.RData")
out_df_clean1 <- out_df_clean

out_df_clean1$assessdat <- as.Date(out_df_clean1$assessdat)

out_df_clean2 <- out_df_clean1
# out_df_clean2 <- head(out_df_clean1, 20)
out_df_clean2 <- out_df_clean2 %>%
  group_by(assessdat, threatcat) %>%
  summarise(n = n())

out_df_clean3 <- out_df_clean2[out_df_clean2$assessdat > as.POSIXct("1800-01-01"), ]

# fig <- plot_ly(alpha = 0.6)
# for(threat in unique(out_df_clean2$threatcat)){
#   out_df_clean3 <- out_df_clean2[out_df_clean2$threatcat == threat, ]
#   fig <- fig %>% add_histogram(out_df_clean3, x = ~assessdat, y = ~n, color = ~threatcat)
# }
# fig <- fig %>% layout(barmode = "stack")
# fig
#
# plot_ly(out_df_clean2, type = 'bar', x = ~assessdat, y = ~n, color = ~threatcat,
#         mode = 'line', stackgroup='one')

plot_ly(
  data = out_df_clean3,
  x = ~assessdat,
  y = ~n,
  color = ~threatcat,
  type = "bar") %>%
  layout(barmode = "stack")

a <- as.POSIXct("0208-03-15")
b <- as.POSIXct("1800-01-10")
c <- as.POSIXct("1800-10-01")
b > a
c > b
c > a

#

#
# # Use dplyr to group the data and keep the non-NA value from the other columns.
# df_threats_hps <- d_sql$HPs_treats %>% group_by(resourceid) %>%
#   summarise(eamenaid = max(eamenaid, na.rm = T),
#             threatcat = max(threatcat, na.rm = T),
#             activtyp = max(activtyp, na.rm = T),
#             assessdat = max(assessdat, na.rm = T))

