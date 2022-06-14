library(leaflet)
library(dplyr)
library(htmlwidgets)

map.name <- "caravanserail"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
ea.search <- rgdal::readOGR(map.url)
# highlight some HP
highlight <- TRUE
ea.highlights.idf <- c('EAMENA-0192700')
ea.highlights.row <- as.integer(row.names(ea.search[ea.search@data$EAMENA.ID %in% ea.highlights.idf, ]))
# write.table(colnames(ea.search@data),
#            sep = "\t",
#            file = paste0(getwd(),"/functions/list_HP_fields_for_R.tsv"),
#            row.names = F)
ea.search$lbl <- paste0("<b>", ea.search$EAMENA.ID,"</b><br>",
                        ea.search$Site.Feature.Interpretation.Type, " (", ea.search$Cultural.Period.Type, ")",
                        ea.search$Administrative.Division., ", ", ea.search$Country.Type, "<br>")
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
    position = "topright") %>%
  addScaleBar(position = "bottomright")


if(highlight){
  map.name.out.zoom <- paste0(getwd(), "/data/geojson/maps/", map.name, "_zoom.html")
  ea.map <- ea.map %>%
    addCircleMarkers(
      lng = ea.search[ea.highlights.row, ]@coords[1],
      lat = ea.search[ea.highlights.row, ]@coords[2],
      weight = 1,
      radius = 4,
      label = ea.search@data[ea.highlights.row, "EAMENA.ID"],
      color = "red",
      fillOpacity = 1,
      opacity = 1)
  ea.map.zoom <- ea.map %>%
    setView(lng = ea.search[ea.highlights.row, ]@coords[1],
            lat = ea.search[ea.highlights.row, ]@coords[2],
            zoom = 17)
}
# ea.map
saveWidget(ea.map, map.name.out)
# ea.map.zoom
saveWidget(ea.map.zoom, map.name.out.zoom)

leaflet() %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  setView(lng = -1.254156387634452,
          lat = 51.758082040247636,
          zoom = 16) %>%
  addCircleMarkers(
    lng = -1.254156387634452,
    lat = 51.758082040247636,
    weight = 1,
    radius = 3,
    popup = "my popup",
    label = "my label",
    fillOpacity = .5,
    opacity = .8) %>%
  addLayersControl(
    baseGroups = c("OSM", "Ortho"),
    position = "topright") %>%
  addScaleBar(position = "bottomright")
