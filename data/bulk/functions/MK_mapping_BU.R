library(openxlsx)
library(xlsx)
library(googlesheets4)

##############################
# Fill an empty BU template with data from an unformatted XLSX
# Fill by type of data:
#   - MK field one-to-one correspondences ('field');
#   - constant values ('value');
#   - logical functions ('expression');
#
# mapping file: https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625
# export a TSV here: https://github.com/eamena-oxford/eamena-arches-dev/blob/main/data/bulk/examples/
#############################

bu.path <- paste0(getwd(), "/data/bulk/")

# MK data
mk.data.path <- paste0(bu.path, "functions/AAA_f22_text only.xlsx")
mk.data <- xlsx::read.xlsx(mk.data.path, sheetIndex = 1)

# BU
# bu.template.path <- paste0(bu.path, "templates/Heritage Place BUS Template.xlsx")
bu.template.path <- paste0(bu.path, "templates/BUS_TemplateUpdate20072021.xlsx")
# rm two first lines
bu <- openxlsx::read.xlsx(bu.template.path, startRow = 3)
# structure only
bu <- bu[0, ]
for(i in seq(1, nrow(mk.data))){
  bu[nrow(bu)+1, ] <- NA
}

# mapping file
mapping.file <- read_sheet('https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625')

# 'field'
mapping.file.fields <- mapping.file[mapping.file$type == "field", ]
# mapping.file.fields[, "EAMENA"]
for(i in seq(1, nrow(mapping.file.fields))){
  # i <- 1
  ea <- as.character(mapping.file.fields[i, "EAMENA"])
  x <- as.character(mapping.file.fields[i, "MKdone"])
  bu[ , ea] <- mk.data[ , x]
}

# 'value'
mapping.file.value <- mapping.file[mapping.file$type == "value", ]
# mapping.file.value[, "EAMENA"]
for(i in seq(1, nrow(mapping.file.value))){
  # i <- 1
  ea <- as.character(mapping.file.value[i, "EAMENA"])
  x <- as.character(mapping.file.value[i, "MKdone"])
  bu[ , ea] <- x
}

# 'expression'
# TODO

# export
write.table(bu, paste0(bu.path, "examples/", Sys.Date(), "-Mohamed.tsv"),
            row.names = F,
            sep = "\t")
