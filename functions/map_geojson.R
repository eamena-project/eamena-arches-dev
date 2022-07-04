library(leaflet)
library(dplyr)
library(htmlwidgets)

# TODO: documentation

map.name <- "kiln"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
ea.search <- rgdal::readOGR(map.url)
# highlight some HP
highlight <- TRUE
ea.highlights.idf <- c('EAMENA-0205783')
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

# Any other maps
library(leaflet)
library(dplyr)
library(htmlwidgets)
lbl <- '<a href = "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/EAMENA-0164997.geojson">EAMENA-0164997.geojson</a>'
# 1 point map
map.name <- "bam"
ea.map <- leaflet() %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
  addCircleMarkers(
    lng = 58.36796164354272,
    lat = 29.115391062920825,
    weight = 1,
    radius = 5,
    popup = lbl,
    color = "red",
    fillOpacity = 1,
    opacity = 1) %>%
  setView(lng = 58.36796164354272,
          lat = 29.11539106292082,
          zoom = 15) %>%
  addLayersControl(
    baseGroups = c("Ortho", "OSM"),
    position = "topright") %>%
  addScaleBar(position = "bottomright")
ea.map
saveWidget(ea.map, paste0(getwd(), "/data/geojson/maps/", map.name, ".html"))


