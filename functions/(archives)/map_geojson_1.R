library(leaflet)
library(dplyr)
library(htmlwidgets)

# TODO: documentation

# highlight some HP
highlight <- FALSE
ea.highlights.idf <- c('EAMENA-0205783')
# project
map.name <- "kiln"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
# different geometries
ea.search.point <- rgdal::readOGR(map.url, require_geomType = "wkbPoint")
ea.search.line <- rgdal::readOGR(map.url, require_geomType = "wkbLineString")
ea.search.polygon <- rgdal::readOGR(map.url, require_geomType = "wkbPolygon")
# ea.highlights.row <- as.integer(row.names(ea.search[ea.search@data$EAMENA.ID %in% ea.highlights.idf, ]))
# highlighted HP
ea.highlights.row.point <- as.integer(row.names(ea.search.point[ea.search.point@data$EAMENA.ID %in% ea.highlights.idf, ]))
ea.highlights.row.line <- as.integer(row.names(ea.search.line[ea.search.line@data$EAMENA.ID %in% ea.highlights.idf, ]))
ea.highlights.row.polygon <- as.integer(row.names(ea.search.polygon[ea.search.polygon@data$EAMENA.ID %in% ea.highlights.idf, ]))

# write.table(colnames(ea.search@data),
#            sep = "\t",
#            file = paste0(getwd(),"/functions/list_HP_fields_for_R.tsv"),
#            row.names = F)
ea.search.point$lbl <- paste0("<b>", ea.search.point$EAMENA.ID,"</b><br>",
                              ea.search.point$Site.Feature.Interpretation.Type, " (", ea.search.point$Cultural.Period.Type, ")",
                              ea.search.point$Administrative.Division., ", ", ea.search.point$Country.Type, "<br>")
ea.search.line$lbl <- paste0("<b>", ea.search.line$EAMENA.ID,"</b><br>",
                             ea.search.line$Site.Feature.Interpretation.Type, " (", ea.search.line$Cultural.Period.Type, ")",
                             ea.search.line$Administrative.Division., ", ", ea.search.line$Country.Type, "<br>")
ea.search.polygon$lbl <- paste0("<b>", ea.search.polygon$EAMENA.ID,"</b><br>",
                                ea.search.polygon$Site.Feature.Interpretation.Type, " (", ea.search.polygon$Cultural.Period.Type, ")",
                                ea.search.polygon$Administrative.Division., ", ", ea.search.polygon$Country.Type, "<br>")
# ea.search$lbl <- paste0("<b>", ea.search$EAMENA.ID,"</b><br>",
#                         ea.search$Site.Feature.Interpretation.Type, " (", ea.search$Cultural.Period.Type, ")",
#                         ea.search$Administrative.Division., ", ", ea.search$Country.Type, "<br>")
ea.map <- leaflet() %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM")
if(nrow(ea.search.point) > 0){
  ea.map <- ea.map %>%
    addCircleMarkers(
      data = ea.search.point,
      # lng = ea.search.point@coords[,1],
      # lat = ea.search.point@coords[,2],
      weight = 1,
      radius = 3,
      popup = ~lbl,
      label = ~EAMENA.ID,
      fillOpacity = .5,
      opacity = .8)
}
if(nrow(ea.search.line) > 0){
  ea.map <- ea.map %>%
    addPolylines(# lng = ~Longitude,
      # lng = ea.search.line@coords[,1],
      # lat = ea.search.line@coords[,2],
      data = ea.search.line,
      weight = 1,
      popup = ~lbl,
      label = ~EAMENA.ID,
      fillOpacity = .5,
      opacity = .8)
}
if(nrow(ea.search.polygon) > 0){
  ea.map <- ea.map %>%
    addPolygons(# lng = ~Longitude,
      # lng = ea.search.line@coords[,1],
      # lat = ea.search.line@coords[,2],
      data = ea.search.polygon,
      weight = 1,
      popup = ~lbl,
      label = ~EAMENA.ID,
      fillOpacity = .5,
      opacity = .8)
}
ea.map <- ea.map %>%
  addLayersControl(
    baseGroups = c("Ortho", "OSM"),
    position = "topright") %>%
  addScaleBar(position = "bottomright")


# ea.highlights.row.polygon[ea.highlights.row.polygon, ]@coords[1]
# TODO:
if(highlight){
  map.name.out.zoom <- paste0(getwd(), "/data/geojson/maps/", map.name, "_zoom.html")
  if(!is.null(nrow(ea.highlights.row.point))){
    ea.map <- ea.map %>%
      addCircleMarkers(
        # data = ea.search.point,
        lng = ea.search[ea.highlights.row, ]@coords[1],
        lat = ea.search[ea.highlights.row, ]@coords[2],
        weight = 1,
        radius = 4,
        label = ea.search@data[ea.highlights.row, "EAMENA.ID"],
        color = "red",
        fillOpacity = 1,
        opacity = 1)
  }
  if(!is.null(nrow(ea.highlights.row.line))){
    ea.map <- ea.map %>%
      addPolylines(# lng = ~Longitude,
        # lng = ea.search.line@coords[,1],
        # lat = ea.search.line@coords[,2],
        data = ea.search.line,
        weight = 2,
        color = "red",
        popup = ~lbl,
        label = ~EAMENA.ID,
        fillOpacity = .5,
        opacity = .8)
  }

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
  # ea.map.zoom
  saveWidget(ea.map.zoom, map.name.out.zoom)
}
# ea.map
saveWidget(ea.map, map.name.out)

