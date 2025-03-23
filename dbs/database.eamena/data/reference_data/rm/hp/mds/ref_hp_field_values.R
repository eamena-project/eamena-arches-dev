#' @name ref_hp_field_values
#'
#' @description Read the root directory of all exported TSV of the possible values for each field: https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp/values. Enter the subfolders and convert TSV to HTML for interactivity purpose
#'
#' @param mds.template The XLSX file listing the HP fields, field descriptions, fields UUID in the DB, if these fields are part of the Minimum Data Standards (MDS), etc.
#' @param create.datatable If TRUE (default), will export an HTML datatable
#' @param mds.datatable.name The name of the HTML datatable
#' @param verbose if TRUE (Default), print messages.
#'
#' @return Creates HTML datatables (sortable, searchable, etc.) and return the GitHub Hyperlinks to be inserted into 'mds.xlsx'
#'
#' @examples
#'
#'
#' @export
ref_hp_field_values <- function(dir.values = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/values/",
                                dir.values.gh = "https://eamena-project.github.io/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/values/",
                                font.size = "15pt",
                                avoid = c("(archives)"),
                                verbose = TRUE){
  # TODO: list on GH directly, not locally (https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/refs/heads/main/dbs/database.eamena/data/reference_data/rm/hp/values/)
  
  list.files(dir.values)
  # only TSV files
  all.files <- list.files(path = dir.values, pattern = "\\.tsv$", full.names = TRUE, recursive = TRUE)
  notavoided.files <- all.files[!grepl("(archives)", all.files)]
  # notavoided.files <- notavoided.files[!grepl("README.md", notavoided.files)]
  ll <- list()
  # for(i in seq(1, 5)){
  for(i in seq(1, length(notavoided.files))){
    file.path <- notavoided.files[i]
    if(verbose){
      print(paste0("Read: ", file.path))
    }
    field <- read.csv2(file.path, sep = "\t")
    field <- field[,colSums(is.na(field)) < nrow(field)]
    path <- DescTools::SplitPath(file.path)$dirname
    fullfilename <- DescTools::SplitPath(file.path)$fullfilename 
    filename <- DescTools::SplitPath(file.path)$filename 
    filename.html <- paste0(filename, ".html")
    parent.directory <- basename(dirname(file.path))
    dt_widget <- DT::datatable(field,
                               escape = FALSE,
                               rownames = FALSE,
                               options = list(pageLength = 25,
                                              autoWidth = TRUE,
                                              initComplete = htmlwidgets::JS(
                                                "function(settings, json) {",
                                                paste0("$(this.api().table().container()).css({'font-size': '", font.size, "'});"),
                                                "}"
                                              # initComplete = DT::JS(
                                              #   "function(settings, json) {",
                                              #   "$(this.api().table().body()).css({'font-family': 'Arial'});",
                                              #   "}"
                                              )))
    # filename.html.path.gh <- paste0(dir.values.gh, parent.directory, '/', filename.html)
    
    filename.html.path.gh <-  paste0("<small><b><a href= '", 
                                     paste0(dir.values.gh, parent.directory, '/', filename.html),
                                     "' target='_blank'>values</a></b></small> ")
    
    ll[[length(ll) + 1]] <- filename.html.path.gh
    outFile <- paste0(path, '/', filename.html)
    htmlwidgets::saveWidget(dt_widget, outFile, selfcontained = TRUE)
    if(verbose){
      print(paste0(i, ") The HTML datatable '", filename.html,"' has been exported into '", path,"'"))
    }
  }
  return(ll)
}
  
ll <- ref_hp_field_values()
