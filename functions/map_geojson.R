library(leaflet)
library(dplyr)
library(htmlwidgets)

# TODO: documentation

map.name <- "NWSyria_sites"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
ea.search <- rgdal::readOGR(map.url)
# highlight some HP
highlight <- TRUE
ea.search$lbl <- paste0("<b>", ea.search$S_ID,"</b><br>",
                        ea.search$Name)
# ea.search$lbl <- paste0("<b>", ea.search$EAMENA.ID,"</b><br>",
#                         ea.search$Site.Feature.Interpretation.Type, " (", ea.search$Cultural.Period.Type, ")",
#                         ea.search$Administrative.Division., ", ", ea.search$Country.Type, "<br>")
ea.map <- leaflet(data = ea.search) %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  addCircleMarkers(# lng = ~Longitude,
    weight = 1,
    radius = 3,
    popup = ~lbl,
    # label = ~EAMENA.ID,
    label = ~S_ID,
    fillOpacity = .5,
    opacity = .8) %>%
  #setView(zoom = 15) %>%
  addLayersControl(
    baseGroups = c("OSM", "Ortho"),
    position = "topright") %>%
  addScaleBar(position = "bottomright")


if(highlight){
  ea.highlights.idf <- c('AM009')
  # ea.highlights.idf <- c('EAMENA-0205783')
  ea.highlights.row <- as.integer(row.names(ea.search[ea.search@data$S_ID %in% ea.highlights.idf, ]))
  # ea.highlights.row <- as.integer(row.names(ea.search[ea.search@data$EAMENA.ID %in% ea.highlights.idf, ]))
  map.name.out.zoom <- paste0(getwd(), "/data/geojson/maps/", map.name, "_zoom.html")
  ea.map <- ea.map %>%
    addCircleMarkers(
      lng = ea.search[ea.highlights.row, ]@coords[1],
      lat = ea.search[ea.highlights.row, ]@coords[2],
      weight = 1,
      radius = 4,
      label = ea.search@data[ea.highlights.row, "S_ID"],
      popup = ea.search@data[ea.highlights.row, "lbl"],
      # label = ea.search@data[ea.highlights.row, "EAMENA.ID"],
      color = "red",
      fillOpacity = 1,
      opacity = 1,
      labelOptions = labelOptions(noHide = T, textsize = "15px")
    )
  ea.map.zoom <- ea.map %>%
    # addMarkers(
    #   lng = ea.search[ea.highlights.row, ]@coords[1],
    #   lat = ea.search[ea.highlights.row, ]@coords[2],
    #   label= ea.search@data[ea.highlights.row, "S_ID"]) %>%
    setView(lng = ea.search[ea.highlights.row, ]@coords[1],
            lat = ea.search[ea.highlights.row, ]@coords[2],
            zoom = 17)
  # ea.map.zoom
  saveWidget(ea.map.zoom, map.name.out.zoom)
}
# ea.map
saveWidget(ea.map, map.name.out)

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


