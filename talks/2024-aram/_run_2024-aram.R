library(eamenaR)


rootDir <- "C:/Rprojects/eamena-arches-dev/talks/2024-aram/"
cvns.qnts.file <- "cvns-qnts.geojson"
CVNS <- paste0(rootDir, "cvns_1.geojson")

cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))

# filter, only CVNS
cvns.geojson <- cvns.qnts.geojson[cvns.qnts.geojson[["Site Feature Interpretation Type"]] == "Caravanserai/Khan", ]
# rm POLYGON, .. to have points only
cvns.geojson <- cvns.geojson[!sf::st_geometry_type(cvns.geojson) %in% c("POLYGON", "MULTIPOLYGON"), ]
# rm fields
cvns.geojson <- cvns.geojson[, c("EAMENA ID", "Site Feature Interpretation Type")]


# write (nb: this as to be changed in the cascade of functions `geojson_map_path`, `geojson_formath_path` and `geojson_stat`)
sf::st_write(cvns.geojson,
             CVNS,
             driver = "GeoJSON")

# x,y map
source("R/geojson_map_path_1.R")
source("R/geojson_format_path.R")
source("R/geojson_stat.R")
CVNS.path <- paste0(rootDir, "caravanserail_paths_1.csv")
d <- hash::hash()
d <- geojson_map_path(d = d,
                      geojson.path = CVNS,
                      csv.path = CVNS.path,
                      map.name = "caravanserail_paths")
d$caravanserail_paths_map

# profiles/section
source("R/geojson_addZ.R")
# e <- hash::hash()
d <- geojson_addZ(d = NA,
                  geojson.path = CVNS)

source("R/geojson_map_path_1.R")
source("R/geojson_stat.R")
d <- geojson_map_path(d = d,
                      geojson.path = d$withZ,
                      csv.path = CVNS.path,
                      map.name = "caravanserail_paths",
                      stats = "profile")

