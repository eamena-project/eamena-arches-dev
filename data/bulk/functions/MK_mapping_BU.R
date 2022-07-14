library(openxlsx)
library(googlesheets4)
# library(httr)

# BU
bu.template.path <- paste0(getwd(), "/data/bulk/templates/Heritage Place BUS Template.xlsx")
# rm two first lines
bu <- read.xlsx(bu.template.path, startRow = 3)
# colnames(bu)
# structure
bu <- bu[0, ]

# MK data
mk.data.path <- paste0(getwd(), "/data/bulk/functions/AAA_f22_text only.xlsx")
mk.data <- read.xlsx(mk.data.path)

# mapping file
mapping.file <- read_sheet('https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625')

View(head(mk.data)


# temp <- tempfile()
# url.bu <- "https://database.eamena.org/en/bulk-upload/templates/34cfe98e-c2c0-11ea-9026-02e7594ce0a0.xlsx"
# download.file(url.bu, temp)
# bu <- read.xlsx(a)
#
# a <- GET(url.bu)
#
