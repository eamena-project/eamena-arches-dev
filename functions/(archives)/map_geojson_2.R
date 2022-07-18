library(leaflet)
library(dplyr)
library(htmlwidgets)

# TODO: documentation
# Create two maps to be imported into a reveal.js showcase:
#   1. a general map displaying all the HPs resulting from a EAMENA search ('geojson url' format)
#   2. a highlight map on one particular HP linked to a 3D model, photograph, etc.

# highlight some HP
highlight <- TRUE
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
# highlighted HP (1)
ea.highlights.row.point <- row.names(ea.search.point[ea.search.point@data$EAMENA.ID %in% ea.highlights.idf, ])
ea.highlights.row.line <- row.names(ea.search.line[ea.search.line@data$EAMENA.ID %in% ea.highlights.idf, ])
ea.highlights.row.polygon <- row.names(ea.search.polygon[ea.search.polygon@data$EAMENA.ID %in% ea.highlights.idf, ])


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
# add geometries POINT, LINES, POLYGON when exist
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
if(highlight){
  if(length(ea.highlights.row.point) > 0){
    hl.geom <- ea.search.point[rownames(ea.search.point@data) == ea.highlights.row.point, ]
    ea.map <- ea.map %>%
      addCircleMarkers(
        data = hl.geom,
        # lng = ea.search[ea.highlights.row, ]@coords[1],
        # lat = ea.search[ea.highlights.row, ]@coords[2],
        weight = 1,
        radius = 4,
        popup = ~lbl,
        label = ~EAMENA.ID,
        color = "red",
        fillOpacity = 1,
        opacity = 1)
  }
  if(length(ea.highlights.row.line) > 0){
    hl.geom <- ea.search.line[rownames(ea.search.line@data) == ea.highlights.row.line, ]
    ea.map <- ea.map %>%
      addPolylines(# lng = ~Longitude,
        # lng = ea.search.line@coords[,1],
        # lat = ea.search.line@coords[,2],
        data = hl.geom,
        weight = 2,
        color = "red",
        popup = ~lbl,
        label = ~EAMENA.ID,
        fillOpacity = .5,
        opacity = .8)
  }
  if(length(ea.highlights.row.polygon) > 0){
    hl.geom <- ea.search.polygon[rownames(ea.search.polygon@data) == ea.highlights.row.polygon, ]
    ea.map <- ea.map %>%
      addPolygons(# lng = ~Longitude,
        # lng = ea.search.line@coords[,1],
        # lat = ea.search.line@coords[,2],
        data = hl.geom,
        weight = 5,
        color = "red",
        popup = ~lbl,
        label = ~EAMENA.ID,
        fillOpacity = .5,
        opacity = .8)
  }
  ea.map.zoom <- ea.map %>%
    setView(lng = rgeos::gCentroid(hl.geom)$x,
            lat = rgeos::gCentroid(hl.geom)$y,
            zoom = 17)
  # ea.map.zoom
  map.name.out.zoom <- paste0(getwd(), "/data/geojson/maps/", map.name, "_zoom.html")
  saveWidget(ea.map.zoom, map.name.out.zoom)
}
# ea.map
saveWidget(ea.map, map.name.out)

