library(openxlsx)
library(xlsx)
library(googlesheets4)

##############################
# Fill an empty BU template with data from an unformatted XLSX
# Fill by type of data:
#   - MK field one-to-one correspondences ('field');
#   - constant values ('value');
#   - logical functions ('expression');
#   - depending values ('escape') not read, dependent from another column evaluated by 'expression'
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
mapping.file.expres <- mapping.file[mapping.file$type == "expression", ]
# mapping.file.expres[, "EAMENA"]
# for(i in seq(1, nrow(mapping.file.expres))){
#   # i <- 1
#   ea <- as.character(mapping.file.expres[i, "EAMENA"])
#   x.text <- as.character(mapping.file.expres[i, "MKdone"])
#   x <- eval(parse(text = x.text)) # the text is executed as a function
#   # x <- as.character(mapping.file.expres[i, "MKdone"])
#   bu[ , ea] <- x
# }
for(i in seq(1, nrow(mapping.file.expres))){
  # i <- 3
  ea <- as.character(mapping.file.expres[i, "EAMENA"])
  x.text <- as.character(mapping.file.expres[i, "MKdone"])
  x.text <- gsub("[\r\n]", "\n", x.text)
  eval(parse(text = x.text)) # the XLSX cell text is executed
}

# delete surnumerary rows
bu <- bu[!is.na(bu$UNIQUEID), ]
# export
write.table(bu, paste0(bu.path, "examples/", Sys.Date(), "-Mohamed.tsv"),
            row.names = F,
            sep = "\t")

# - - - - - - - - -


# # Cultural.Period.Type
# for(j in seq(1, nrow(mk.data))){
#   Classical <- mk.data[j, "Roman"] == "Y" | mk.data[j, "Byzantine"] == "Y"
#   if(!is.na(Classical)){
#     bu[j, ea] <- "Classical/Protohistoric/Pre-Islamic (North Africa)"
#     bu[j, "Cultural.Period.Certainty"] <- "Possible"
#   }
#   Berber <- mk.data[j, "Breber"] == "Y" | mk.data[j, "Berber for"] == "Y"
#   if(!is.na(Classical)){
#     bu[j, ea] <- "Unknown"
#     bu[j, "Cultural.Period.Certainty"] <- "Not Applicable"
#   }
# }



# Heritage.Place.Function
# for(j in seq(1, nrow(mk.data))){
#   Funerary <- mk.data[j, "Tomb"] == "Y" | mk.data[j, "Mausoleum"] == "Y" | mk.data[j, "Bazina"] == "Y"
#   if(!is.na(Funerary)){
#     bu[j, ea] <- "Funerary/Memorial"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Domestic <- mk.data[j, "Town"] == "Y" | mk.data[j, "Village"] == "Y"
#   if(!is.na(Domestic)){
#     bu[j, ea] <- "Domestic"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Agricultural <- mk.data[j, "Farm.Site"] == "Y"
#   if(!is.na(Agricultural)){
#     bu[j, ea] <- "Agricultural/Pastoral"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Industrial <- mk.data[j, "Press"] == "Y"
#   if(!is.na(Industrial)){
#     bu[j, ea] <- "Industrial/Productive"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Hydrological <- mk.data[j, "Aqueduct"] == "Y"
#   if(!is.na(Hydrological)){
#     bu[j, ea] <- "Hydrological"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Religious <- mk.data[j, "Church"] == "Y"
#   if(!is.na(Religious)){
#     bu[j, ea] <- "Religious"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   Defensive <- mk.data[j, "Roman.Fort"] == "Y" | mk.data[j, "Fort.gasr"] == "Y"
#   if(!is.na(Defensive)){
#     bu[j, ea] <- "Defensive/Fortification"
#     bu[j, "Heritage.Place.Function.Certainty"] <- "Medium"
#   }
#   # - - - - - - - - - - - - - - - - -
#   Structure <- Funerary | Domestic | Agricultural | Industrial | Hydrological | Religious | Defensive
#   if(!is.na(Structure)){
#     bu[j, "Site.Feature.Form.Type"] <- "Structure"
#     bu[j, "Site.Feature.Form.Type.Certainty"] <- "Medium"
#   }
# }










