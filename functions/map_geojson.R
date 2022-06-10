library(leaflet)
library(dplyr)
library(htmlwidgets)

map.name <- "caravanserail"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
ea.search <- rgdal::readOGR(map.url)
# write.table(colnames(ea.search@data),
#            sep = "\t",
#            file = paste0(getwd(),"/functions/list_HP_fields_for_R.tsv"),
#            row.names = F)
ea.search$lbl <- paste0("<b>", ea.search$EAMENA.ID," - ", ea.search$Administrative.Division., ", ", ea.search$Country.Type, "</b><br>",
                        ea.search$Site.Feature.Interpretation.Type, " (", ea.search$Cultural.Period.Type, ")")
ea.map <- leaflet(data = ea.search) %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
  addCircleMarkers(# lng = ~Longitude,
    weight = 1,
    radius = 3,
    popup = ~lbl,
    label = ~EAMENA.ID,
    fillOpacity = .5,
    opacity = .8) %>%
  addLayersControl(
    baseGroups = c("Ortho", "OSM"),
    position = "topleft"
  ) %>%
  addCircleMarkers(
    lng = ea.search[1, ]@coords[1],
    lat = ea.search[1, ]@coords[2],
    weight = 1,
    radius = 4,
    popup = ~lbl,
    label = ~EAMENA.ID,
    color = "red",
    fillOpacity = 1,
    opacity = 1)

saveWidget(ea.map, map.name.out)


