# library(openxlsx)
library(xlsx)
library(googlesheets4)

# Will fill the BU by type of data: MK field one-to-one correspondences ('field'),
# constant values ('value'), logical functions ('expression')
# the mapping file is here: https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625
# export a TSV here: https://github.com/eamena-oxford/eamena-arches-dev/blob/main/data/bulk/examples/

bu.path <- paste0(getwd(), "/data/bulk/")

# MK data
mk.data.path <- paste0(bu.path, "functions/AAA_f22_text only.xlsx")
mk.data <- xlsx::read.xlsx(mk.data.path, sheetIndex = 1)

# BU
# bu.template.path <- paste0(bu.path, "templates/Heritage Place BUS Template.xlsx")
bu.template.path <- paste0(bu.path, "templates/BUS_TemplateUpdate20072021.xlsx")

# rm two first lines
bu <- openxlsx::read.xlsx(bu.template.path, startRow = 3)
# colnames(bu)
# structure only
bu <- bu[0, ]
for(i in seq(1, nrow(mk.data))){
  bu[nrow(bu)+1, ] <- NA
}

# mapping file
mapping.file <- read_sheet('https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625')

# View(head(mk.data))



# fields
mapping.file.fields <- mapping.file[mapping.file$type == "field", ]
# mapping.file.fields[, "EAMENA"]
for(i in seq(1, nrow(mapping.file.fields))){
  # i <- 1
  ea <- as.character(mapping.file.fields[i, "EAMENA"])
  x <- as.character(mapping.file.fields[i, "MKdone"])
  bu[ , ea] <- mk.data[ , x]
}

# values
mapping.file.value <- mapping.file[mapping.file$type == "value", ]
# mapping.file.value[, "EAMENA"]
for(i in seq(1, nrow(mapping.file.value))){
  # i <- 1
  ea <- as.character(mapping.file.value[i, "EAMENA"])
  x <- as.character(mapping.file.value[i, "MKdone"])
  bu[ , ea] <- x
}

# expression
# TODO

# export
write.table(bu, paste0(bu.path, "examples/", Sys.Date(), "-Mohamed.tsv"),
            row.names = F,
            sep = "\t")
