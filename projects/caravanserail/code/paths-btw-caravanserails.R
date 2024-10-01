library(eamenaR)
library(sf)


geojson_map(map.name = "caravanserail")
df <- geojson_stat(stat = c("list_ids"), export.stat = T)

# sequence list of caravanserail ..;20;33;82;46;39;...

paths <- read.table("C:/Rprojects/eamenaR/inst/extdata/caravanserail_ord.csv", sep = ";", header = T)
paths

geojson.path <- 'C:/Users/Thomas Huet/Documents/R/win-library/4.1/eamenaR/extdata/caravanserail.geojson'
ea.geojson <- geojsonsf::geojson_sf(geojson.path)

paths$path.wkt <- paths$dist <- NA
for(i in seq(1, nrow(paths))){
  # i <- 1
  a <- ea.geojson[ea.geojson$`EAMENA ID` == paths[i, "from"], ]
  b <- ea.geojson[ea.geojson$`EAMENA ID` == paths[i, "to"], ]
  paths[i, "dist"] <- as.numeric(sf::st_distance(a, b))
  # path.geom <- st_as_sf(st_cast(st_union(a$geometry, b$geometry),"LINESTRING"))
  paths[i, "path.wkt"] <- st_as_text(st_cast(st_union(a$geometry, b$geometry),"LINESTRING"))
  # path.geom <- as.character(path.geom[[1,"x"]])
  # paths[i, "path"] <- st_as_text($geometry)
}

a <- ea.geojson[ea.geojson$`EAMENA ID` == "EAMENA-0192617", ]
b <- ea.geojson[ea.geojson$`EAMENA ID` == "EAMENA-0192630", ]

cbind()


st_sfc(mapply(function(a, b){st_cast(st_union(a, b),"LINESTRING")},
              df$geometry, df$geometry.1, SIMPLIFY=FALSE))

plot(sf::st_linestring(sf::st_coordinates(a), sf::st_coordinates(b)))

