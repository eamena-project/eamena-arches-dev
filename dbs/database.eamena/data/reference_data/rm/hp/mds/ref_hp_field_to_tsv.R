#' @name ref_hp_fields_to_tsv 
#'
#' @description Creates an HTML widget (datatable) from an XLSX listing the groups of fields (i.e. `level1` groups: Assessment Summary, Resource Summary, etc.) and export an HTML table with hyperlinks to the different subfolders. The latter will host TSV files. 
#'
#' @param mds.template The XLSX file listing the HP fields, field descriptions, fields UUID in the DB, if these fields are part of the Minimum Data Standards (MDS), etc.
#' @param base_url The root path of the hyperlinks
#' @param mds.path The root directory of the MDS template
#' @param create.datatable If TRUE (default), will export an HTML datatable
#' @param mds.datatable.name The name of the HTML datatable
#' @param verbose if TRUE (Default), print messages.
#'
#' @return An HTML datatable (sortable, searchable, etc.)
#'
#' @examples
#' 
#' @export
ref_hp_fields_to_tsv <- function(mds.template = "mds-template.xlsx",
                                 base_url = "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/values/",
                                 mds.path = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/",
                                 create.datatable = TRUE,
                                 mds.datatable.name = "field-to-tsv.html",
                                 verbose = TRUE){
  

  mds.template.df <- paste0(mds.path, mds.template)
  df <- openxlsx::read.xlsx(mds.template.df, sheet = 1)
  df_filtered <- df[, c("level1", "color")]
  df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
  df_filtered <- df_filtered[!duplicated(df_filtered), ]
  colnames(df_filtered)[colnames(df_filtered) == 'level1'] <- 'Groups'
  df_filtered$Groups <- stringr::str_to_title(df_filtered$Groups)
  # Apply the color and hyperlink together
  df_filtered$Groups <- mapply(function(group, color) {
    sprintf("<a href='%s%s' target='_blank' style='font-size: 16px; font-family:arial; color:%s'>%s</a>", 
            base_url, gsub(" ", "_", group), color, stringr::str_to_upper(group))
  }, df_filtered$Groups, df_filtered$color)
  dt_widget <- DT::datatable(df_filtered[ , c("Groups"), drop=FALSE], 
                             escape = FALSE,
                             rownames = FALSE,
                             options = list(paging = FALSE, 
                                            searching = FALSE, 
                                            info = FALSE, 
                                            autoWidth = TRUE)) 
  if(!create.datatable){
    dt_widget #plot
  } else {
    htmlwidgets::saveWidget(dt_widget, paste0(mds.path, '/', fileOut), selfcontained = TRUE)
  }
}

