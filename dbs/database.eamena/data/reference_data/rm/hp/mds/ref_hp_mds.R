## Generates a DT table of field names and field description from 'mds-template.xlsx'

#' Create boxplot or various boxplots of path lengths between different heritage places
#'
#' @name geojson_boxplot Create boxplot or various boxplots of path lengths between different heritage places
#'
#' @description
#'
#' @param mds.template The XLSX file listing the HP fields, field descriptions, fields UUID in the DB, if these fields are part of the Minimum Data Standards (MDS), etc..
#' @param create.datatable If TRUE (default), will export an HTML datatable
#' @param mds.datatable.name The name of the HTML datatable
#' @param verbose if TRUE (Default), print messages.
#'
#' @return An HTML datatable (sortable, searchable, etc.)
#'
#' @examples
#'
#'
#' @export
ref_hp_mds <- function(mds.template = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/rm/hp/mds/mds-template.xlsx",
                       create.datatable = TRUE,
                       mds.path = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/",
                       mds.datatable.name = "fields-description.html",
                       verbose = TRUE){

  # library(readxl)
  library(DT)
  # library(htmlwidgets)

  # Download the file temporarily
  temp_file <- tempfile(fileext = ".xlsx")
  download.file(mds.template, destfile = temp_file, mode = "wb")
  df <- readxl::read_excel(temp_file, sheet = 1)
  df[["is MDS"]] <- NA
  df[grep("Yes", df[["Minimum Data Standard"]]), "is MDS"] <- "Yes"

  # paths
  #
  # mds.path <- paste0(root.path, "")
  # #
  # mds.template <- paste0(mds.path, "mds-template.xlsx")
  # df <- read_excel(mds.template, sheet = 1)


  df$level1.url <- stringr::str_to_title(gsub(" ", "_", df$level1))
  df$level3.url <- stringr::str_to_title(gsub("//", "_", gsub(" ", "_", df$level3)))
  sort(df$level3.url)

  description.field <- "description"
  df_filtered <- df[, c("num", "level1", "level2", "level3", "is MDS", description.field, "color")]
  colnames(df_filtered)[colnames(df_filtered) == 'level3'] <- 'Heritage Place field'
  # rm the transparency from colors (ie, mds)
  df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
  # df_filtered$color <- as.factor(df_filtered$color)
  if(verbose){
    print(paste0("Creates the datatable"))
  }
  dt_widget <- datatable(df_filtered[ , c("num", "Heritage Place field", "is MDS", description.field), drop=FALSE],
                         escape = FALSE,
                         rownames = FALSE,
                         options = list(pageLength = 25,
                                        autoWidth = TRUE,
                                        initComplete = JS(
                                          "function(settings, json) {",
                                          "$(this.api().table().body()).css({'font-family': 'Arial'});",
                                          "}"
                                        ))) %>%
    formatStyle(
      columns = c("Heritage Place field"),
      backgroundColor = styleEqual(df_filtered[["Heritage Place field"]], df_filtered$color)
    )
  if(create.datatable){
    outFile <- paste0(mds.path, '/', mds.datatable.name)
    htmlwidgets::saveWidget(dt_widget, outFile, selfcontained = TRUE)
    if(verbose){
      print(paste0("The HTML datatable '", mds.datatable.name,"' has been exported into '", mds.path,"'"))
    }
  } else {
    return(dt_widget)
  }
}

ref_hp_mds(mds.datatable.name = "fields-description-test.html")
