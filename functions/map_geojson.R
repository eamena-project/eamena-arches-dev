library(leaflet)
library(dplyr)
library(htmlwidgets)

# # gs4_deauth();gs4_auth()
# gg.url <- "https://docs.google.com/spreadsheets/d/1q6VdxS_1Pi0fVWfyQzW6VBhjuBY58hymtSLWg4JyLEA/edit?usp=sharing"
# db.atl <- read_sheet(gg.url)
#
# eamena.search <-
#
#   db.atl$lbl <- paste0("<b>", db.atl$SiteName," - ", db.atl$LabCode, "</b><br>",
#                        db.atl$C14BP, " +/- ", db.atl$C14SD, "<br>",
#                        db.atl$Period," - ",  db.atl$PhaseCode, "<br>",
#                        "<b>", db.atl$BD,"</b>")
# lf <- leaflet(data = db.atl) %>%
#   addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
#   addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
#   # addTiles(group = 'OSM') %>%
#   addCircleMarkers(layerId = ~LabCode,
#                    lng = ~Longitude,
#                    lat = ~Latitude,
#                    weight = 1,
#                    radius = 3,
#                    popup = ~lbl,
#                    label = ~SiteName,
#                    fillColor = ~color,
#                    fillOpacity = .2,
#                    color = ~color,
#                    opacity = .8) %>%
#   addLegend("bottomright",
#             colors = df.colors$color,
#             labels = df.colors$BD,
#             title = "BDs",
#             opacity = 1) %>%
#   addLayersControl(
#     baseGroups = c("Ortho", "OSM"),
#     position = "topleft"
#   )

map.name <- "caravanserail"
map.format <- '.geojson'
map.root <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/geojson/"
map.name.out <- paste0(getwd(), "/data/geojson/maps/", map.name, ".html")
map.url <- paste0(map.root, map.name, map.format)
ea.search <- rgdal::readOGR(map.url)
# colnames(ea.search@data)
ea.search$lbl <- paste0("<b>", ea.search$EAMENA.ID," - ", ea.search$Administrative.Division., ", ", ea.search$Country.Type, "</b><br>",
                        ea.search$Site.Feature.Interpretation.Type, " (", ea.search$Cultural.Period.Type, ")")
ea.map <- leaflet(data = ea.search) %>%
  addProviderTiles(providers$"Esri.WorldImagery", group = "Ortho") %>%
  addProviderTiles(providers$"OpenStreetMap", group = "OSM") %>%
  # addTiles(group = 'OSM') %>%
  addCircleMarkers(# lng = ~Longitude,
    # lat = ~Latitude,
    weight = 1,
    radius = 3,
    popup = ~lbl,
    label = ~EAMENA.ID,
    # fillColor = ~color,
    fillOpacity = .2,
    # color = ~color,
    opacity = .8) %>%
  # addLegend("bottomright",
  #           colors = df.colors$color,
  #           labels = df.colors$BD,
  #           title = "BDs",
  #           opacity = 1) %>%
  addLayersControl(
    baseGroups = c("Ortho", "OSM"),
    position = "topleft"
  )
saveWidget(ea.map, map.name.out)


#
#
# Administrative Division, Country Type
#
#
# leaflet(nycounties) %>%
#   addTiles() %>%
#   addCircleMarkers()

# --------------------------------------------------------------
# Works
# --------------------------------------------------------------

# mydata <- fromJSON(url)
# file_js = FROM_GeoJson(url_file_string = url)

# ---------------------------------------------------------------
# Trying to directly GET from the `geojson url` in EAMENA
# Gives errors
# --------------------------------------------------------------


# url <- 'https://database.eamena.org/en/api/search/export_results?paging-filter=1&tiles=true&format=geojson&precision=6&total=156&term-filter=%5B%7B%22context%22%3A%22%22%2C%22context_label%22%3A%22Heritage%20Place%20-%20Resource%20Name%22%2C%22id%22%3A1%2C%22text%22%3A%22CVNS-IR-KHORASAN%22%2C%22type%22%3A%22term%22%2C%22value%22%3A%22CVNS-IR-KHORASAN%22%2C%22inverted%22%3Afalse%7D%5D2'
# data <- read.csv2(url)
# library(jsonlite)
# mydata <- fromJSON(url)
# str(mydata)
#
# library(geojsonR)
# file_js = FROM_GeoJson(url_file_string = 'https://database.eamena.org/en/api/search/export_results?paging-filter=1&tiles=true&format=geojson&precision=6&total=156&term-filter=%5B%7B%22context%22%3A%22%22%2C%22context_label%22%3A%22Heritage%20Place%20-%20Resource%20Name%22%2C%22id%22%3A1%2C%22text%22%3A%22CVNS-IR-KHORASAN%22%2C%22type%22%3A%22term%22%2C%22value%22%3A%22CVNS-IR-KHORASAN%22%2C%22inverted%22%3Afalse%7D%5D')


# Error in open.connection(con, "rb") : HTTP error 500.


