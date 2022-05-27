library(leaflet)
library(rgdal)
library(htmlwidgets)

## create leaflet map with a QDGC grid for a particular country
# see:

grids.path <- paste0(getwd(),"/data/grids")
grid.afghanistan <- readOGR(grids.path, layer = "afghanistan", verbose = FALSE)

map.afghanistan <- leaflet() %>%
  addTiles() %>%
  addPolygons(data = grid.afghanistan,
              weight = 2,
              fillOpacity = 0,
              col = 'red')
saveWidget(map.afghanistan, file=paste0(grids.path, "/grid_afghanistan.html"))

