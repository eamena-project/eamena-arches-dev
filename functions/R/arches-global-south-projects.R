library(leaflet)
library(leaflet.extras)

gs <- geojsonsf::geojson_sf("C:/Rprojects/eamena-arches-dev/data/geojson/globalsouth.geojson")
gs.globalsouth <- gs[!is.na(gs$globalsout),]
arches.projects <- readLines("C:/Rprojects/eamena-arches-dev/data/geojson/arches-projects.geojson") %>%
  paste(collapse = "\n") %>%
  fromJSON(simplifyVector = FALSE)
ggs <- leaflet(gs.globalsouth,
               width = "100%",
               height = "100vh") %>%
  addProviderTiles(providers$Stamen.Toner,
                   options = providerTileOptions(noWrap = TRUE)
  ) %>%
  setView(lng = 53,
          lat = 25,
          zoom = 3) %>%
  addPolygons(color = "red",
              weight = 0,
              opacity = .5,
              fillOpacity = .5) %>%
  addGeoJSONv2(geojson = arches.projects,
               labelProperty = "project",
               popupProperty = "description",
               weight = 1,
               color = "blue",
               opacity = 1,
               fillOpacity = 0) %>%
  addControl("<a href='https://www.archesproject.org/'>Arches</a> projects in the Global South", position = "topright")
fileOut <- paste0(getwd(),"/data/geojson/maps/arches-global-south.html")
htmlwidgets::saveWidget(ggs, fileOut)
print(paste0(fileOut, " has been saved"))
