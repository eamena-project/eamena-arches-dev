library(openxlsx)
library(messydates)
library(lubridate)
library(tibble)
library(dplyr)
library(RPostgreSQL)
library(DBI)
library(DT)
library(plotly)
library(collapsibleTree)
library(htmlwidgets)


Dates <- F
EDTFs <- F
CulturalPeriods <- F
CulturalPer.HP <- F

if(CulturalPer.HP){
  # collect all Cultural periods for a given HP
  dir_funct <- paste0(getwd(), "/functions/R/")
  source(paste0(dir_funct, "_conn.R"))        # read the secret credential
  source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

  d_sql <- hash::hash() # hash instance to store the results
  d_sql <- uuid_from_eamenaid("eamena", "EAMENA-0187363", d_sql, "uuid")
  d_sql$uuid
  # - - - - - - - -
  # SQL: select * from values where value = 'Iron Age (Levant/Mesopotamia)'
  # return two values in conceptid:
  #     - b9f0270b-c04e-4c77-9a82-5062ecfa7ae1 : ???
  #     - ce7f6688-212a-47b1-8c2b-d95ce219c8e9 : c'est l'UUID de Concept/Thesauri
  # - - - - - - - -
}


if(Period.do){
  # convert Perio.do CSV into a data.table table
  url.perio.do <- "https://n2t.net/ark:/99152/p0dataset.csv"
  perio.do <- read.csv(url.perio.do, fileEncoding = "UTF-8")
  head(perio.do)
  perio.do.dt <- datatable(perio.do)
  saveWidget(perio.do.dt,
             paste0(getwd(),"/data/time/results/periodo_list.html"))
}

if(CulturalPeriods){
  # Plot Cultural Periods as a HTML tree
  dir_funct <- paste0(getwd(), "/functions/R/")
  source(paste0(dir_funct, "_conn.R"))        # read the secret credential
  source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

  d_sql <- hash::hash() # hash instance to store the results

  # list concepts below Cultural Period
  filed.out <- "CulturalPeriod_list"
  d_sql <- list_cpts("eamena", d_sql, field.out, '3b5c9ac7-5615-3de6-9e2d-4cd7ef7460e4')
  g <- d_sql$CulturalPeriod_list

  write.leaves <- F
  if(write.leaves){
    # The Cultural periods are the leaves of the Concept list
    leaves <- V(g)[degree(g, mode="out") == 0]
    leaves <- leaves$name
    df.equiv <- data.frame(eamena = leaves,
                           periodo = rep("", length(leaves)))
    write.table(df.equiv, paste0(getwd(),"/data/time/results/equivalences.tsv"), sep ="\t", row.names = F)
  }

  # format for collapsibleTree
  edges.cultural.period <- as_data_frame(g, what = "edges")
  edges.cultural.period$root <- "cultural.period"
  edges.cultural.period <- edges.cultural.period[edges.cultural.period$from != "cultural.period", ]
  tree.edges.cultural.period <- collapsibleTree(edges.cultural.period,
                                                hierarchy = c("root", "from", "to"),
                                                root = "Thesauri",
                                                c("from", "to"),
                                                collapsed = FALSE,
                                                width = 1200,
                                                height = 900)
  # tree.edges.cultural.period <- collapsibleTree(edges.cultural.period,
  #                                               c("from", "to"),
  #                                               collapsed = FALSE,
  #                                               width = 1200,
  #                                               height = 900)
  saveWidget(as_widget(tree.edges.cultural.period),
             paste0(getwd(),"/data/time/results/",
                    filed.out, ".html"))
}


if(Dates){
  # run analyse on the EAMENA database

  # SQL queries on EAMENA DB for R, stored in a Python-dictionary-like structure
  read_eamena_db <- F

  if(read_eamena_db){
    # read the DB (could be very long)
    dir_funct <- paste0(getwd(), "/functions/R/")
    source(paste0(dir_funct, "_conn.R"))        # read the secret credential
    source(paste0(dir_funct, "R_functions_2.R"))  # read the functions file

    d_sql <- hash::hash() # hash instance to store the results

    # threats and dates
    d_sql <- threats_hps(con, d_sql, "HPs_treats")

    df_threats_hps <- d_sql$HPs_treats

    out_df <- df_threats_hps[0, ] # copy structure
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
  # translate from arabic to english
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

}


if(EDTFs){
  # run analyse on the 19 syrian database (XLSX)
  plot_ly <- T
  by.cat <- T
  export.to.tsv <- F
  show.to.html <- F
  filter.on.id <- T
  id.filter <- c("AM009") # select these/this IDs

  path_time <- paste0(getwd(), "/functions/time/")

  # df <- read.xlsx(paste0(path_time, "data.xlsx"))
  data_file <- "Disturbances_EDTF.xlsx"
  date_field <- "EDTF"
  site_field <- "S_ID"
  cause_field <- "Disturbance.Cause" # R doesn't accept spaces in headers
  type_field <- "Disturbance.Type"
  # data_file <- "data.xlsx"
  # date_field <- "date"
  # site_field <- "site"
  # cause_field <- "cause"
  # type_field <- "type"

  file_out <- "df_syria_out"

  df_syria <- read.xlsx(paste0(path_time, data_file),
                        sheet = "Sheet1")
  # export XLSX to TSV
  if(export.to.tsv){
    write.table(df_syria,  paste0(path_time, file_out, ".tsv"),
                quote = FALSE, sep = "\t", col.names = TRUE)
  }

  if(filter.on.id){
    df_syria <- df_syria[df_syria$S_ID %in% id.filter, ]
    file_out <- paste0(file_out, "_", paste0(as.character(id.filter), collapse = "_"))
  }


  # reformat dataframe and dates
  df_syria.out <- data.frame(#region = character(),
    site = character(),
    date = character(),
    cause = character(),
    type = character(),
    density = integer())
  for(i in seq_len(nrow(df_syria))){
    # intersect with the limits of the study: "2004-01-01..2019-12-31"
    # loop to read the date field
    if (i %% 50 == 0){print(paste0("   - ", i, "/", nrow(df_syria)))}
    var.date <- md_intersect(as_messydate("2004-01-01..2019-12-31"),
                             as_messydate(df_syria[i, date_field]))
    n.dates <- length(var.date)
    # var.region <- rep(df_syria[i, "region"], n.dates)
    var.site <- rep(df_syria[i, site_field], n.dates)
    var.cause <- rep(df_syria[i, cause_field], n.dates)
    var.type <- rep(df_syria[i, type_field], n.dates)
    df.damage <- data.frame(#region = var.region,
      site = var.site,
      date = var.date,
      cause = var.cause,
      type = var.type,
      density = 1/n.dates)
    df_syria.out <- rbind(df_syria.out, df.damage)
  }
  # # export XLSX to TSV
  # write.table(df_syria.out,  paste0(path_time, file_out, "_ext.tsv"),
  #             quote = FALSE, sep='\t', col.names = TRUE)
  # plot
  df_syria.out$date <- as.Date(df_syria.out$date)

  df_syria.out.general <- df_syria.out %>%
    group_by(date) %>%
    summarise(density = sum(density))

  df_syria.out.cat <- df_syria.out %>%
    group_by(date, type) %>%
    summarise(density = sum(density))

  if(plot_ly){
    # general
    p <- plot_ly(df_syria.out.general,
                 type = 'scatter',
                 x = ~date,
                 y = ~round(density, 4),
                 mode = 'line') %>%
      layout(title = "Threats")
    saveWidget(as_widget(p), paste0(getwd(),"/functions/time/results/", file_out, "_threats.html"))
    if(by.cat){
      # type
      p <- plot_ly(df_syria.out.cat,
                   type = 'scatter',
                   x = ~date,
                   # y = ~density,
                   y = ~round(density, 4),
                   color=~type,
                   mode = 'line') %>%
        layout(title = "Threats types")
      if(filter.on.id){
        saveWidget(as_widget(p), paste0(getwd(),"/functions/time/results/", file_out, "_threats_types", paste0(as.character(id.filter), collapse = "_"), ".html"))
      }
      saveWidget(as_widget(p), paste0(getwd(),"/functions/time/results/", file_out, "_threats_types.html"))
    }
    # saveWidget(as_widget(p), paste0(getwd(),"/results/threats.html"))
  }

  if(png.out){
    png(paste0(path_time, file_out, ".png"), width = 18, height = 12, res = 300, units = "cm")
    plot(density ~ date, df_syria.out, xaxt = "n", type = "l")
    axis(1, df_syria.out$date, format(df_syria.out$date, "%b %y"), cex.axis = .7)
    dev.off()
  }

  # show XLSX to HTML (for reveal.js)
  if(show.to.html){
    library(xtable)
    df_syria_select <- df_syria[, c("S_ID", "Disturbance.Type", "Disturbance.Cause", "EDTF")]
    print(xtable(df_syria_select),
          type="html",
          # file="example.html",
          align="llll",include.rownames = F,
          html.table.attributes="")

  }

  #
  # if(plot_ly){
  #   # if TRUE, export as plot_ly widget
  #   p <- plot_ly(df, type = 'scatter', x = ~date, y = ~hp, color = ~threat,
  #                mode = 'line', stackgroup='one')
  #   p
  #   saveWidget(as_widget(p), paste0(getwd(),"/results/threats_stacked.html"))
  #   #
  # }

}
