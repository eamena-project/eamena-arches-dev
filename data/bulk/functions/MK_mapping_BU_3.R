library(openxlsx)
library(xlsx)
library(googlesheets4)

##############################
# Fill an empty BU template with data from an unformated XLSX
# Fill by type of data:
#   - 'field': MK field one-to-one correspondences, will be copied as it;
#   - 'value': constant values (ie, always the same value);
#   - 'expression': logical functions, mainly if statements;
#   - 'escape': values depending from another column evaluated by 'expression'
#       not read
#
# mapping file: https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625
# export a TSV here: https://github.com/eamena-oxford/eamena-arches-dev/blob/main/data/bulk/examples/
#############################

# dir_funct <- paste0(getwd(), "/functions/R/")
# source(paste0(dir_funct, "R_functions_8.R"))  # read the functions file

# devtools::install_github("eamena-oxford/eamenaR")
library(eamenaR)
library(dplyr)

bu.path <- paste0(getwd(), "/data/bulk/")

# MK data
mk.data.path.folder <- paste0(bu.path, "bu/")
l.bus <- list.files(mk.data.path.folder)

# BU template
bu.template.path <- paste0(bu.path, "templates/BUS_TemplateUpdate20072021.xlsx")
bu <- openxlsx::read.xlsx(bu.template.path, startRow = 3)

# mapping file
mapping.file <- read_sheet('https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625')

# Grid Squares
# geojson.path <- "C:/Rprojects/eamena-arches-dev/data/bulk/functions/MK_grid_squares.geojson"
# grid.squares.sf <- st_read(geojson.path)

xcoord <- ycoord <- c()

for(bu.name in l.bus){
  # bu.name <- "AAA_f10_text.xlsx"
  print(paste0("*read: ", bu.name))
  mk.data.path <- paste0(bu.path, "bu/", bu.name)
  mk.data <- xlsx::read.xlsx(mk.data.path, sheetIndex = 1)
  print(paste0("     nb of rows: ", nrow(mk.data)))
#   xcoord <- c(xcoord, mk.data$xcoord)
#   ycoord <- c(ycoord, mk.data$ycoord)
# }
#
# max(xcoord, na.rm = T)
# max(ycoord, na.rm = T)
# min(xcoord, na.rm = T)
# min(ycoord, na.rm = T)
  # BU
  # bu.template.path <- paste0(bu.path, "templates/Heritage Place BUS Template.xlsx")
  # rm two first lines
  # structure only
  bu <- bu[0, ]
  for(i in seq(1, nrow(mk.data))){
    bu[nrow(bu) + 1, ] <- NA
  }

  # - - - - - - - - - - - - - -
  # loops

  # 'field'
  print(paste0("     works on 'field' field type"))
  mapping.file.fields <- mapping.file[mapping.file$type == "field", ]
  # mapping.file.fields[, "EAMENA"]
  for(i in seq(1, nrow(mapping.file.fields))){
    # i <- 1
    ea <- as.character(mapping.file.fields[i, "EAMENA"])
    x <- as.character(mapping.file.fields[i, "MKdone"])
    bu[ , ea] <- mk.data[ , x]
  }

  # 'value'
  print(paste0("     works on 'value' field type"))
  mapping.file.value <- mapping.file[mapping.file$type == "value", ]
  # mapping.file.value[, "EAMENA"]
  for(i in seq(1, nrow(mapping.file.value))){
    # i <- 1
    ea <- as.character(mapping.file.value[i, "EAMENA"])
    x <- as.character(mapping.file.value[i, "MKdone"])
    bu[ , ea] <- x
  }

  # 'expression'
  print(paste0("     works on 'expression' field type"))
  mapping.file.expres <- mapping.file[mapping.file$type == "expression", ]
  for(i in seq(1, nrow(mapping.file.expres))){
    # i <- 0 ; i <- i + 1
    ea <- as.character(mapping.file.expres[i, "EAMENA"])
    print(paste0("           ... and read '", ea,"'"))
    x.text <- as.character(mapping.file.expres[i, "MKdone"])
    x.text <- gsub("[\r\n]", "\n", x.text)
    # for(j in seq(1, nrow(mk.data))){
    #   j <- 1
    #   bu[j, "Geometric.Place.Expression"] <- mk.data[j, "Point"]
    #   bu[j, "Grid.ID"] <- geom_within_gs(mk.data[j, "Point"], grid.squares.sf)
    # }
    eval(parse(text = x.text)) # the XLSX cell text is executed
  }

  # 'Seen' column
  for(i in seq(1, nrow(mk.data))){
    # i <- 3
    seen <- mk.data[i, "Seen"]
    if (seen == "N"){
      bu[i, "Overall.Condition.State"] <- "Unknown"
      bu[i, "Damage.Extent.Type"] <- "Unknown"
      bu[i, "Disturbance.Cause.Category.Type"] <- "Unknown"
      bu[i, "Disturbance.Cause.Type"] <- "Unknown"
      bu[i, "Disturbance.Cause.Certainty"] <- "Not Applicable"
      bu[i, "Threat.Category"] <- "Unknown"
      bu[i, "Threat.Type"] <- "Unknown"
      bu[i, "Threat.Probability"] <- "Not Applicable"
    }
  }

  # the supplementary rows, a kind of 'pipe' work to add further data to a row
  bu.piped <- bu[0, ]
  for(i in seq(1, nrow(mk.data))){
    if (!is.na(mk.data[i, "Placename"])){
      # print(mk.data[i, "Placename"])
      new.row <- nrow(bu.piped) + 1
      bu.piped[new.row, ] <- NA
      bu.piped[new.row, "UNIQUEID"] <- mk.data[i, "Site_ID"]
      bu.piped[new.row, "Resource.Name"] <- mk.data[i, "Placename"]
      bu.piped[new.row, "Name.Type"] <- "Toponym"}
  }

  bu <- rbind(bu, bu.piped)

  # delete surnumerary rows
  bu <- bu[!is.na(bu$UNIQUEID), ]
  # sort on UNIQUEID
  bu <- bu[order(bu$UNIQUEID),]
  row.names(bu) <- seq(1, nrow(bu))
  # View(head(bu))

  # export
  out.bu <- paste0(bu.path, "out/", bu.name)
  # out.bu.tsv <- paste0(out.bu, ".tsv")
  # write.table(bu,
  #             out.bu.tsv,
  #             row.names = F,
  #             sep = "\t")
  out.bu.xlsx <- paste0(out.bu, "_out.xlsx")
  write.xlsx(bu, out.bu.xlsx, row.names = F, showNA = FALSE)
  print(paste0("      ", bu.name, " done: ", out.bu.xlsx, "\n"))
}








