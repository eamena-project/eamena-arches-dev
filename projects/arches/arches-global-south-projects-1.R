###########################
# Show the extension of the different Global South projects based in Arches in an interactive leaflet map.
###########################

root.project <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/projects/arches/"
l.projects <- read.csv(paste0(root.project, "list-projects.txt"), header = F)
l.projects <- l.projects[ , 1]
projects.colors <- RColorBrewer::brewer.pal(length(l.projects), "Set1")
# background
gs <- geojsonsf::geojson_sf("C:/Rprojects/eamena-arches-dev/data/geojson/globalsouth.geojson")
gs.globalsouth <- gs[!is.na(gs$globalsout),]
# leaflet map
ggs <- leaflet::leaflet(gs.globalsouth,
                        width = "100%",
                        height = "100vh") %>%
  leaflet::addProviderTiles(providers$Stamen.Toner,
                            options = providerTileOptions(noWrap = TRUE)
  ) %>%
  leaflet::setView(lng = 53,
                   lat = 25,
                   zoom = 3) %>%
  leaflet::addPolygons(color = "red",
                       weight = 0,
                       opacity = .5,
                       fillOpacity = .5)
# loop to add the layers
for(i in seq(1, length(l.projects))){
  arches.projects <- readLines(paste0(root.project, "geojson/", l.projects[i], ".geojson")) %>%
    paste(collapse = "\n") %>%
    jsonlite::fromJSON(simplifyVector = FALSE)
  ggs <- ggs %>%
    leaflet.extras::addGeoJSONv2(geojson = arches.projects,
                                 labelProperty = "project",
                                 popupProperty = "description",
                                 weight = 1,
                                 color = projects.colors[i],
                                 opacity = 1,
                                 fillOpacity = 0)
}
ggs <- ggs %>%
  leaflet::addControl("<a href='https://www.archesproject.org/'>Arches</a> projects in the Global South", position = "topright")

export <- F
if(export){
  fileOut <- paste0(getwd(),"/projects/arches/arches-global-south.html")
  htmlwidgets::saveWidget(ggs, fileOut)
  print(paste0(fileOut, " has been saved"))
} else {
  print(ggs)
}

