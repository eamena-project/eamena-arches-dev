library(eamenaR)


rootDir <- "C:/Rprojects/eamena-arches-dev/talks/2024-aram/"
cvns.qnts.file <- "cvns-qnts.geojson"
# CVNS <- paste0(rootDir, "cvns_1.geojson")
cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))
# selected fields
cvns.qnts.geojson <- cvns.qnts.geojson[, c("EAMENA ID", "Site Feature Interpretation Type")]
# CVNS & QNTS
site.feat.interp <- cvns.qnts.geojson[["Site Feature Interpretation Type"]]
cvns.geojson <- cvns.qnts.geojson[grep("Caravanserai/Khan", site.feat.interp), ]
# Points
cvns.geojson <- cvns.geojson[!sf::st_geometry_type(cvns.geojson) %in% c("POLYGON", "MULTIPOLYGON", "LINESTRING"), ]
qnts.geojson <- cvns.qnts.geojson[grep("Qanat/Foggara", site.feat.interp), ]
# Lines
qnts.geojson <- qnts.geojson[!sf::st_geometry_type(qnts.geojson) %in% c("POLYGON", "MULTIPOLYGON", "POINT"), ]

# checks geometry types
unique(st_geometry_type(qnts.geojson)) # LINESTRING only
unique(st_geometry_type(cvns.geojson)) # POINT only
# convert CRS to WGS 84 / UTM zone 40N
cvns_utm <- st_transform(cvns.geojson, crs = 32640)
qnts_utm <- st_transform(qnts.geojson, crs = 32640)
# Calculating the nearest features and the distances in meters
qnts_utm$nearest_index <- st_nearest_feature(qnts_utm, cvns_utm)
qnts_utm$distance_m <- st_distance(qnts_utm, cvns_utm[qnts_utm$nearest_index, ], by_element = TRUE) %>%
  set_units("m")


###################
library(sf)
library(dplyr)
library(units)

# First, ensure both datasets are properly transformed to the same CRS, if not already
cvns_utm <- st_transform(cvns.geojson, crs = 32640)
qnts_utm <- st_transform(qnts.geojson, crs = 32640)

# Initialize an empty sf dataframe for storing results
df.closest <- st_sf(
  cvn = character(),
  qnt = character(),
  dist = numeric(),
  geometry = st_sfc(crs = 32640),  # Specify CRS appropriately
  sf_column_name = "geometry"
)

# Calculate the nearest qnts for each cvns
cvns_utm$nearest_index <- st_nearest_feature(cvns_utm, qnts_utm)
cvns_utm$distance_m <- st_distance(cvns_utm, qnts_utm[cvns_utm$nearest_index, ], by_element = TRUE) %>%
  set_units("m")

# Loop over cvns to find and connect to the nearest qnts
# for (i in seq_len(nrow(cvns_utm))) {
library(sf)
library(dplyr)
library(units)

# First, ensure both datasets are properly transformed to the same CRS, if not already
cvns_utm <- st_transform(cvns.geojson, crs = 32640)
qnts_utm <- st_transform(qnts.geojson, crs = 32640)

# Initialize an empty sf dataframe for storing results
df.closest <- st_sf(
  cvn = character(),
  qnt = character(),
  dist = numeric(),
  geometry = st_sfc(crs = 32640),  # Specify CRS appropriately
  sf_column_name = "geometry"
)

# Calculate the nearest qnts for each cvns
cvns_utm$nearest_index <- st_nearest_feature(cvns_utm, qnts_utm)
cvns_utm$distance_m <- st_distance(cvns_utm, qnts_utm[cvns_utm$nearest_index, ], by_element = TRUE) %>%
  set_units("m")

# Loop over cvns to find and connect to the nearest qnts
# for (i in seq_len(nrow(cvns_utm))) {
for (i in seq_len(8)) {
  cvn.closest <- as.character(sf::st_drop_geometry(cvns_utm[i, "EAMENA ID"]))
  dist.closest <- as.numeric(sf::st_drop_geometry(cvns_utm[i, "distance_m"]))  # Ensure conversion to numeric
  qnt.closest.idx <- as.integer(sf::st_drop_geometry(cvns_utm[i, "nearest_index"]))
  qnt.closest <- as.character(sf::st_drop_geometry(qnts_utm[qnt.closest.idx, "EAMENA ID"]))

  nearest_points <- sf::st_nearest_points(cvns_utm[i, ], qnts_utm[qnt.closest.idx, ])
  line_coords <- sf::st_coordinates(nearest_points)  # Extracts a matrix of coordinates from MULTIPOINT
  shortest_linestring <- sf::st_sfc(sf::st_linestring(line_coords), crs = 32640)

  new_row <- st_sf(
    cvn = cvn.closest,
    qnt = qnt.closest,
    dist = dist.closest,
    geometry = shortest_linestring
  )
  df.closest <- rbind(df.closest, new_row)
}

# Write the result to a GeoJSON file
st_write(df.closest, paste0(rootDir, "closest_lines_cvns_to_qnts.geojson"), append=FALSE)



######################
# works but need to iterate over cvns
library(sf)
library(dplyr)
library(units)

# Initialize an empty sf dataframe for storing results
df.closest <- st_sf(
  cnv = character(),
  qnt = character(),
  dist = numeric(),
  geometry = st_sfc(crs = 32640),  # Specify CRS appropriately
  sf_column_name = "geometry"
)

# Loop through each qnts and find the closest cvns
for (i in seq_len(4)) {
  qnt.closest <- as.character(sf::st_drop_geometry(qnts_utm[i, "EAMENA ID"]))
  dist.closest <- as.numeric(sf::st_drop_geometry(qnts_utm[i, "distance_m"]))  # Ensure conversion to numeric
  cvn.closest.idx <- as.integer(sf::st_drop_geometry(qnts_utm[i, "nearest_index"]))
  cvn.closest <- as.character(sf::st_drop_geometry(cvns_utm[cvn.closest.idx, "EAMENA ID"]))

  nearest_points <- sf::st_nearest_points(qnts_utm[i, ], cvns_utm[cvn.closest.idx, ])
  print(sf::st_geometry_type(nearest_points))
  line_coords <- sf::st_coordinates(nearest_points)  # This extracts a matrix of coordinates from MULTIPOINT
  shortest_linestring <- sf::st_sfc(sf::st_linestring(line_coords), crs = 32640)

  new_row <- st_sf(
    cnv = cvn.closest,
    qnt = qnt.closest,
    dist = dist.closest,
    geometry = shortest_linestring
  )
  df.closest <- rbind(df.closest, new_row)
}

st_write(df.closest, paste0(rootDir, "closest_lines_2.geojson"), append=FALSE)


########################
# Not working as expected

library(sf)
library(dplyr)
library(units)

###########
df.closest <- st_sf(
  cnv = character(),
  qnt = character(),
  dist = numeric(),
  geometry = st_sfc(crs = 32640),  # Specify CRS appropriately
  sf_column_name = "geometry"
)
# TODO: loop
# nrow(qnts_utm)
for (i in 1:2){
  # i <- 1
  qnt.closest <- as.character(sf::st_drop_geometry(qnts_utm[i, "EAMENA ID"]))
  dist.closest <- as.integer(sf::st_drop_geometry(qnts_utm[i, "distance_m"]))
  cvn.closest.idx <- as.integer(sf::st_drop_geometry(qnts_utm[i, "nearest_index"]))
  cvn.closest <- as.character(sf::st_drop_geometry(cvns_utm[cvn.closest.idx, "EAMENA ID"]))
  # df.closest[nrow(df.closest) + 1, ] = c(cvn.closest, qnt.closest, dist.closest)
  # df.closest
  nearest_points <- st_nearest_points(qnts_utm[i,], cvns_utm[i,])
  closest_point_on_line <- nearest_points[2]
  shortest_linestring <- st_sfc(st_linestring(rbind(st_coordinates(qnts_utm[i,]), st_coordinates(nearest_points))), crs = 32640)
  new_row <- st_sf(
    cnv = cvn.closest,
    qnt = qnt.closest,
    dist = dist.closest,
    geometry = shortest_linestring
  )
  # empty_sf <- st_transform(empty_sf, crs = 4326)
  # new_row <- st_transform(new_row, crs = 4326)
  df.closest <- rbind(df.closest, new_row)
}
st_write(df.closest, paste0(rootDir, "closest_lines.geojson"), append=FALSE)


library(ggplot2)
ggplot() +
  geom_sf(data = updated_sf, color = "blue", size = 1.2) +  # Plot the LINESTRING
  geom_sf(data = qnts_utm[i, ], color = "red", size = 1.2) +   # Plot the POINT
  geom_sf(data = cvns_utm[i, ], color = "black", size = 3) +   # Plot the POINT
  theme_minimal() +  # Optional: Use a minimal theme
  labs(title = "Plot of a LINESTRING and a POINT")  # Add a title

# write (nb: this as to be changed in the cascade of functions `geojson_map_path`, `geojson_formath_path` and `geojson_stat`)
# sf::st_write(cvns.geojson,
#              CVNS,
#              driver = "GeoJSON")

# x,y map
source("R/geojson_map_path_1.R")
source("R/geojson_format_path.R")
source("R/geojson_stat.R")
CVNS.path <- paste0(rootDir, "caravanserail_paths_1.csv")
d <- hash::hash()
d[['cvns']] <- cvns.geojson
d <- geojson_map_path(d = d,
                      # geojson.path = CVNS,
                      geojson.path = d[['cvns']],
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

