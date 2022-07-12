library(RPostgreSQL)
library(DBI)
library(dplyr)
library(plotly)
library(lubridate)
library(shiny)

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
  load("C:/Rprojects/eamena-arches-dev/functions/R/out_df_clean.RData")
}
# convert to Date
out_df_clean$assessdat <- as.Date(out_df_clean$assessdat)
# group and count
out_df_clean <- out_df_clean %>%
  group_by(assessdat, threatcat) %>%
  summarise(n = n())
# filter on dates
out_df_clean <- out_df_clean[out_df_clean$assessdat >= as.Date("2015-01-01"), ] # the earliest
out_df_clean <- out_df_clean[out_df_clean$assessdat <= as.Date(Sys.Date()), ] # the earliest
# aggregate on months
out_df_clean$assessdat.m <- format(as.Date(out_df_clean$assessdat), "%Y-%m")
out_df_clean$assessdat.y <- format(as.Date(out_df_clean$assessdat), "%Y")
time.interv <- c("day", "month", "year")

#
# plot_ly(
#   data = out_df_clean,
#   x = ~assessdat.m,
#   y = ~n,
#   color = ~threatcat,
#   type = "bar") %>%
#   layout(barmode = "stack")

# shiny app
ui <- fluidPage(
  headerPanel('EAMENA Threat Category through time'),
  sidebarPanel(
    selectInput('timeint','time interval', time.interv, "day")),
    # selectInput('xcol','X Variable', names(mtcars)),
    # selectInput('ycol','Y Variable', names(mtcars)),
    # selected = names(mtcars)[[2]]),
  mainPanel(
    plotlyOutput('plot')
  )
)

server <- function(input, output) {

  t <- reactive({input$timeint})

  x <- reactive({
    mtcars[,input$xcol]
  })

  y <- reactive({
    mtcars[,input$ycol]
  })

  output$plot <- renderPlotly(
    if(t() == "day"){
      plot1 <- plot_ly(
        data = out_df_clean,
        x = ~assessdat,
        y = ~n,
        color = ~threatcat,
        type = "bar") %>%
        layout(barmode = "stack")
    }
    else if (t() == "month"){
      plot1 <- plot_ly(
        data = out_df_clean,
        x = ~assessdat.m,
        y = ~n,
        color = ~threatcat,
        type = "bar") %>%
        layout(barmode = "stack")
    }
    else if (t() == "year"){
      plot1 <- plot_ly(
        data = out_df_clean,
        x = ~assessdat.y,
        y = ~n,
        color = ~threatcat,
        type = "bar") %>%
        layout(barmode = "stack")
    }
  )
}

shinyApp(ui,server)

