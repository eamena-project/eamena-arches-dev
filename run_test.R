library(eamenaR)

path <- "C:/Users/Thomas Huet/Desktop/CityOfTheDead/"
list_mapping_bu(
  bu.path = path,
  bu.template.path = "C:/Users/Thomas Huet/Desktop/CityOfTheDead/",
  mapping.file = "https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625",
  mapping.file.ggsheet = TRUE,
  job = "cairo",
  job.type = "cairo_type",
  eamena.field = "target",
  eamena.id = "UNIQUEID",
  verbose = TRUE
)

CoordinE <- 31.273372
CoordinN <- 30.045597

for(j in seq(1, nrow(data))){
  geom <- paste0("POINT(",
                 data[j, "CoordinE"], " ", data[j, "CoordinN"],
                 ")")
}



##########################################################################

# devtools::install_github("eamena-oxford/eamenaR")
library(eamenaR)
library(dplyr)

geojson_map(map.name = "geoarch",
            ids = "GEOARCH.ID",
            geojson.path = "C:/Rprojects/eamena-arches-dev/data/geojson/geoarchaeo.geojson",
            export.plot = F)

geojson_stat(stat.name = "caravanserail", stat = "list_ids", export.stat = F)

library(dplyr)

list_mapping_bu(bu.path = "C:/Rprojects/eamena-arches-dev/data/bulk/bu/",
                mapping.file = 'https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625',
                mapping.file.ggsheet = T,
                job = "mk2",
                job.type = "mk2_type")


geojson_measurements(stat.name = "areas", plot.stat = T)


geom_within_gs(resource.wkt = "POINT(2.95179492341257 36.0477563810438)")
2.95179492341257 36.0477563810438
