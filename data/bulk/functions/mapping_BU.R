# devtools::install_github("eamena-oxford/eamenaR")
library(eamenaR)
library(dplyr)
library(openxlsx)
library(xlsx)
library(googlesheets4)

##############################
# Fill an empty BU template with data from an unformated XLSX
# Fill by type of data:
#   - 'field': job field one-to-one correspondences, will be copied as it;
#   - 'value': constant values (ie, always the same value);
#   - 'expression': logical functions, mainly if statements;
#   - 'escape': values depending from another column evaluated by 'expression'. This field is
#       not read
#
# mapping file: https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625
# export a TSV here: https://github.com/eamena-oxford/eamena-arches-dev/blob/main/data/bulk/examples/
#############################

# dir_funct <- paste0(getwd(), "/functions/R/")
# source(paste0(dir_funct, "R_functions_8.R"))  # read the functions file

verb <- T

bu.path <- paste0(getwd(), "/data/bulk/")

job <- "mk" # Mohamed Kenawi
job.type <- paste0(job, "_type")

# MK data
data.path.folder <- paste0(bu.path, "bu/", job, "/")
l.bus <- list.files(data.path.folder)

# BU template
bu.template.path <- paste0(bu.path, "templates/BUS_TemplateUpdate20072021.xlsx")
bu <- openxlsx::read.xlsx(bu.template.path, startRow = 3)

# mapping file
mapping.file <- read_sheet('https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625')

# Grid Squares
# geojson.path <- "C:/Rprojects/eamena-arches-dev/data/bulk/functions/MK_grid_squares.geojson"
# grid.squares.sf <- st_read(geojson.path)

# l.bus <- l.bus[c(1)] # already done

# l.bus <- c("AAA_f18_text.xlsx")# test

cpt <- 0
for(bu.name in l.bus){
  # bu.name <- "AAA_f10_text.xlsx"
  # bu.name <- "AAA_f18_text.xlsx"
  cpt <- cpt + 1
  print(paste0(cpt, "- read: ", bu.name))
  data.path <- paste0(bu.path, "bu/", job, "/", bu.name)
  data <- xlsx::read.xlsx(data.path,
                          sheetIndex = 1)
  data <- data[rowSums(is.na(data)) != ncol(data),]
  print(paste0(" - nb of rows: ", nrow(data)))
  data[is.na(data)] <- "" # rm NA value for logical tests
  # BU
  # bu.template.path <- paste0(bu.path, "templates/Heritage Place BUS Template.xlsx")
  # rm two first lines
  # structure only
  bu <- bu[0, ]
  for(i in seq(1, nrow(data))){
    bu[nrow(bu) + 1, ] <- NA
  }

  # - - - - - - - - - - - - - -
  # loops

  # 'field'
  print(paste0("     works on 'field' field type"))
  mapping.file.fields <- mapping.file[mapping.file[ , job.type] == "field", ]
  # mapping.file.fields[, "EAMENA"]
  for(i in seq(1, nrow(mapping.file.fields))){
    # i <- 1
    ea <- as.character(mapping.file.fields[i, "EAMENA"])
    if(verb){print(paste0("           ... and read '", ea,"'"))}
    x <- as.character(mapping.file.fields[i, job])
    bu[ , ea] <- data[ , x]
  }

  # 'value'
  print(paste0("     works on 'value' field type"))
  mapping.file.value <- mapping.file[mapping.file[ , job.type] == "value", ]
  # mapping.file.value[, "EAMENA"]
  for(i in seq(1, nrow(mapping.file.value))){
    # i <- 1
    ea <- as.character(mapping.file.value[i, "EAMENA"])
    if(verb){print(paste0("           ... and read '", ea,"'"))}
    x <- as.character(mapping.file.value[i, job])
    bu[ , ea] <- x
  }

  # 'expression'
  print(paste0("     works on 'expression' field type"))
  mapping.file.expres <- mapping.file[mapping.file[ , job.type] == "expression", ]
  for(i in seq(1, nrow(mapping.file.expres))){
    # i <- 0 ; i <- i + 1
    ea <- as.character(mapping.file.expres[i, "EAMENA"])
    if(verb){print(paste0("           ... and read '", ea,"'"))}
    x.text <- as.character(mapping.file.expres[i, job])
    x.text <- gsub("[\r\n]", "\n", x.text)
    # ## TEST BLOCK
    # if(ea == 'Geometric.Place.Expression'){
    #   for(j in seq(1, nrow(data))){
    #     bu[j, "Geometric.Place.Expression"] <- data[j, "Point"]
    #     bu[j, "Grid.ID"] <- geom_within_gs(data[j, "Point"], "C:/Rprojects/eamena-arches-dev/data/bulk/functions/MK_grid_squares_2.geojson")
    #   }
    # } else {
    #   eval(parse(text = x.text)) # the XLSX cell text is executed
    # }
    # ## END OF THE TEST BLOCK
    eval(parse(text = x.text)) # the XLSX cell text is executed
  }

  # 'value'
  print(paste0("     works on 'value' field type"))
  mapping.file.value <- mapping.file[mapping.file[ , job.type] == "value", ]
  # mapping.file.value[, "EAMENA"]
  for(i in seq(1, nrow(mapping.file.value))){
    # i <- 1
    ea <- as.character(mapping.file.value[i, "EAMENA"])
    if(verb){print(paste0("           ... and read '", ea,"'"))}
    x <- as.character(mapping.file.value[i, job])
    bu[ , ea] <- x
  }

  # 'other' column
  print(paste0("     works on 'other' field values"))
  mapping.file.other <- mapping.file[mapping.file[ , job.type] == "other", ]
  for(i in seq(1, nrow(mapping.file.other))){
    x.text <- as.character(mapping.file.other[i, job])
    x.text <- gsub("[\r\n]", "\n", x.text)
    eval(parse(text = x.text)) # the XLSX cell text is executed
  }

  # delete surnumerary rows
  bu <- bu[!is.na(bu$UNIQUEID), ]
  # sort on UNIQUEID
  # bu$UNIQUEID <- as.numeric(bu$UNIQUEID)
  bu <- bu[order(bu$UNIQUEID),]
  row.names(bu) <- seq(1, nrow(bu))

  # export
  out.bu <- paste0(bu.path, "out/", bu.name)
  out.bu.xlsx <- paste0(out.bu, "_out.xlsx")
  write.xlsx(bu, out.bu.xlsx, row.names = F, showNA = FALSE)
  print(paste0(" - '", bu.name, "' done: ", out.bu.xlsx))
  print("")
}
