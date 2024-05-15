# devtools::install_github("eamena-project/eamenaR")
library(eamenaR)


geojson.path = "C:/Rprojects/eamena-arches-dev/projects/kites/data/kites_ea_ant_match.geojson"
`%>%` <- dplyr::`%>%` # used to not load dplyr
ea.geojson <- sf::read_sf(geojson.path)
sort(na.omit(unique(ea.geojson$Type)))
