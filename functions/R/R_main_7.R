library(RPostgreSQL)
library(DBI)
library(dplyr)
library(plotly)
library(lubridate)

# SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
read_eamena_db <- F

if(read_eamena_db){
  # read the DB (could be very long)
  dir_funct <- paste0(getwd(), "/functions/R/")
  source(paste0(dir_funct, "_conn.R"))        # read the secret credential
  source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

  d_sql <- hash::hash() # hash instance to store the results

  # counts of HPs
  d_sql <- count_hps(con, d_sql, "HPs_count")
  d_sql$HPs_count

  # threats and dates
  d_sql <- threats_hps(con, d_sql, "HPs_treats")

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
  # clean the df
  out_df_clean <- out_df[out_df$threatcat != "Not Applicable", ]
  out_df_clean <- out_df_clean[!is.na(out_df_clean$assessdat), ]
  # save
  save(out_df_clean, file = "C:/Rprojects/eamena-arches-dev/functions/R/out_df_clean.RData")
} else {
  # print(getwd())
  # load 'out_df_clean'
  load("C:/Rprojects/eamena-arches-dev/functions/R/out_df_clean.RData")
}
# translate arabic
out_df_clean[grepl("بناء والتطوير", out_df_clean$threatcat), ] <- "Building and Development"
out_df_clean[grepl("لأنشطة المخالفة للقانون", out_df_clean$threatcat), ] <- "Looting/Illegal Activities"
out_df_clean[grepl("طبيعي", out_df_clean$threatcat), ] <- "Natural"
out_df_clean[grepl("مواصلات", out_df_clean$threatcat), ] <- "Infrastructure/Transport"
out_df_clean[grepl("رعوي", out_df_clean$threatcat), ] <- "Agricultural/Pastoral"
out_df_clean[grepl("نشاطات زيارة", out_df_clean$threatcat), ] <- "Tourism/Visitor Activities"
out_df_clean[grepl("استخدام اجتماعي", out_df_clean$threatcat), ] <- "Social/Cultural Uses of Heritage"
out_df_clean[grepl("تخريب", out_df_clean$threatcat), ] <- "Vandalism"
out_df_clean[grepl("استخدام مائي", out_df_clean$threatcat), ] <- "Hydrological"
out_df_clean[grepl("استخدام مؤسسي", out_df_clean$threatcat), ] <- "Public/Institutional Use"
out_df_clean[grepl("نزاع مسلح", out_df_clean$threatcat), ] <- "Military/Armed Conflict"
out_df_clean[grepl("إنتاجي", out_df_clean$threatcat), ] <- "Industrial/Productive"
out_df_clean[grepl("بناء والتطوير", out_df_clean$threatcat), ] <- "Building and Development"
out_df_clean[grepl("غير محدد", out_df_clean$threatcat), ] <- "Unknown"
out_df_clean[grepl("أثري", out_df_clean$threatcat), ] <- "Archaeological"



# library(stringr)
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "نشاطات زيارة", "Tourism/Visitor Activities")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "استخدام ثقافي للتراث أثري", "Social/Cultural Uses of Heritage")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "تخريب", "Vandalism ")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "استخدام مائي", "Hydrological")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "استخدام مؤسسي", "Public/Institutional Use")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "نزاع مسلح", "Military/Armed Conflict")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "إنتاجي", "Industrial/Productive ")
# out_df_clean$threatcat <- str_replace(out_df_clean$threatcat, "بناء والتطوير", "Building and Development")

# order on frequencies
n.threatcat <- table(out_df_clean$threatcat) %>%
  as.data.frame() %>%
  arrange(desc(Freq))
n.threatcat$perc <- round(n.threatcat$Freq/sum(n.threatcat$Freq)*100, 1)
threatcat.ord <- n.threatcat$Var1
# threatcat.ord

# grepl("بناء والتطوير", n.threatcat$Var1, "Building and Development")

# convert to Date
out_df_clean$assessdat <- as.Date(out_df_clean$assessdat)
# filter on dates
out_df_clean <- out_df_clean[out_df_clean$assessdat >= as.Date("2015-01-01"), ] # the earliest
out_df_clean <- out_df_clean[out_df_clean$assessdat <= as.Date(Sys.Date()), ] # the latest

# # aggregate on days
# out_df_clean <- out_df_clean %>%
#   group_by(assessdat, threatcat) %>%
#   summarise(n = n())
# # aggregate on months
# out_df_clean$assessdat.m <- format(as.Date(out_df_clean$assessdat), "%Y-%m")
# out_df_clean <- out_df_clean %>%
#   group_by(assessdat.m, threatcat) %>%
#   summarise(n.m = n())
# # aggregate on years
# out_df_clean$assessdat.y <- format(as.Date(out_df_clean$assessdat), "%Y")
# out_df_clean <- out_df_clean %>%
#   group_by(assessdat.y, threatcat) %>%
#   summarise(n.y = n())

# time.interv <- c("day", "month", "year")

# by day
# aggregate on days
out_df_clean_d <- out_df_clean %>%
  group_by(assessdat, threatcat) %>%
  summarise(n = n())
plot1 <- plot_ly(
  data = out_df_clean_d,
  x = ~assessdat,
  y = ~n,
  color = ~factor(threatcat, levels = rev(threatcat.ord)),
  # color = ~threatcat,
  text = ~paste0(threatcat, " - ", as.character(n)),
  hoverinfo = 'text',
  type = "bar") %>%
  layout(title = 'Categories of threats registered in EAMENA - by day',
         barmode = "stack")
plot1
htmlwidgets::saveWidget(as_widget(plot1), "C:/Rprojects/eamena-arches-dev/data/time/threats_day.html")

# by month
out_df_clean$assessdat.m <- format(as.Date(out_df_clean$assessdat), "%Y-%m")
# aggregate on months
out_df_clean_m <- out_df_clean %>%
  group_by(assessdat.m, threatcat) %>%
  summarise(n.m = n())
plot1 <- plot_ly(
  data = out_df_clean_m,
  x = ~assessdat.m,
  y = ~n.m,
  color = ~factor(threatcat, levels = rev(threatcat.ord)),
  # color = ~threatcat,
  text = ~paste0(threatcat, " - ", as.character(n.m)),
  hoverinfo = 'text',
  type = "bar") %>%
  layout(title = 'Categories of threats registered in EAMENA - by month',
         barmode = "stack")
plot1
htmlwidgets::saveWidget(as_widget(plot1), "C:/Rprojects/eamena-arches-dev/data/time/threats_month.html")

# by year
out_df_clean$assessdat.y <- format(as.Date(out_df_clean$assessdat), "%Y")
# aggregate on years
out_df_clean_y <- out_df_clean %>%
  group_by(assessdat.y, threatcat) %>%
  summarise(n.y = n())
plot1 <- plot_ly(
  data = out_df_clean_y,
  x = ~assessdat.y,
  y = ~n.y,
  color = ~factor(threatcat, levels = rev(threatcat.ord)),
  # color = ~threatcat,
  text = ~paste0(threatcat, " - ", as.character(n.y)),
  hoverinfo = 'text',
  # colors = colorRampPalette(c("#0000FF", "#00FF00", '#FF0000'))(nrow(n.threatcat)),
  type = "bar") %>%
  layout(title = 'Categories of threats registered in EAMENA - by year',
         barmode = "stack")
plot1
htmlwidgets::saveWidget(as_widget(plot1), "C:/Rprojects/eamena-arches-dev/data/time/threats_year.html")
#
# plot_ly(
#   data = out_df_clean,
#   x = ~assessdat.y,
#   y = ~n,
#   color = ~factor(threatcat, levels = rev(threatcat.ord)),
#   # color = ~threatcat,
#   type = "bar",
#   text = ~paste0(threatcat, as.character(sum(n))),
#   hoverinfo = 'text') %>%
#   layout(title = 'Categories of threats registered in EAMENA - by year',
#          barmode = "stack")
#
# fig <- plot_ly(type = 'bar')
# fig <- fig %>%
#   add_trace(data =out_df_clean,
#     x = ~assessdat.y,
#     y = ~n,
#     color = ~factor(threatcat, levels = rev(threatcat.ord)),
#     text = ~threatcat,
#     hoverinfo = 'text'
#     # marker = list(color='green'),
#     # showlegend = F
#   )
#
# fig
