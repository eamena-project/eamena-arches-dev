# devtools::install_github("eamena-oxford/eamenaR")

library(eamenaR)
library(sf)
library(ggplot2)
library(ggrepel)

###################


symbology <- rio::import('https://github.com/eamena-oxford/eamenaR/blob/main/inst/extdata/symbology.xlsx?raw=true')

geojson_map(map.name = "caravanserail",
            field.names = c("Damage Extent Type"),
            fig.width = 11,
            export.plot = T)

geojson_map(map.name = "caravanserail",
            field.names = c("Disturbance Cause Type ", "Damage Extent Type"),
            fig.width = 11,
            export.plot = T)

d <- hash::hash()
my_con <- RPostgres::dbConnect(drv = RPostgres::Postgres(),
                               user = 'postgres',
                               password = 'postgis',
                               dbname = 'eamena',
                               host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                               port = 5432)
# Cultural periods
d <- list_concepts(db.con = my_con, d = d,
                   field = "Disturbance Extent Type",
                   uuid = '41488800-6c00-30f2-b93f-785e38ab6251')


geojson_map(map.name = "caravanserail",
            field.names = c("Damage Extent Type"),
            export.plot = F)

geojson_map(map.name = "caravanserail", export.plot = F)

geojson_stat(stat.name = "caravanserail", stat = "list_ids", export.stat = F, geojson.path = "C:/Rprojects/eamenaR/inst/extdata/caravanserail_2.geojson")

geojson_map(map.name = "caravanserail_2", export.plot = T, geojson.path = "C:/Rprojects/eamenaR/inst/extdata/caravanserail_2.geojson", fig.width = 14, fig.height = 11)

d_sql <- hash::hash() # hash instance to store the results
d_sql <- uuid_from_eamenaid("eamena", d_sql, "EAMENA-0207774")

geojson_map_path(map.name = "map_paths_5",
                 geojson.path = "C:/Rprojects/eamenaR/inst/extdata/caravanserail_2.geojson",
                 csv.path = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/caravanserail_paths_3.csv",
                 export.plot = T,
                 fig.width = 14,
                 fig.height = 11,
                 dirOut = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/")

geojson_boxplot_path(plot.name = "box_paths_4",
                     geojson.path = "C:/Rprojects/eamenaR/inst/extdata/caravanserail_2.geojson",
                     csv.path = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/caravanserail_paths_3.csv",
                     export.plot = F,
                     fig.width = 14,
                     fig.height = 11,
                     dirOut = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/")



###############################

# geojson_map(map.name = "caravanserail")
df <- geojson_stat(stat = c("list_ids"), geojson.path = "C:/Rprojects/eamenaR/inst/extdata/caravanserail_2.geojson", export.stat = T)
df$id <- rownames(df)
# sequence list of caravanserail ..;20;33;82;46;39;...
paths <- read.table("C:/Rprojects/eamena-arches-dev/projects/caravanserail/caravanserail_paths_3.csv", sep = ",", header = T)
paths

geojson.path <- 'C:/Users/Thomas Huet/Documents/R/win-library/4.1/eamenaR/extdata/caravanserail_2.geojson'
caravan.geom.sf <- geojsonsf::geojson_sf(geojson.path)

paths$path.wkt <- paths$dist.m <- paths$from.id <- paths$to.id <- paths$from.geom <- paths$to.geom <- NA
for(i in seq(1, nrow(paths))){
  # i <- 1
  from <- caravan.geom.sf[caravan.geom.sf$`EAMENA ID` == paths[i, "from"], ]
  to <- caravan.geom.sf[caravan.geom.sf$`EAMENA ID` == paths[i, "to"], ]
  paths[i, "from.id"] <- df[df$ea.ids == from$`EAMENA ID`, "id"]
  paths[i, "to.id"] <- df[df$ea.ids == to$`EAMENA ID`, "id"]
  paths[i, "from.geom"] <- st_as_text(from$geometry)
  paths[i, "to.geom"] <- st_as_text(to$geometry)
  paths[i, "dist.m"] <- as.numeric(sf::st_distance(from, to))
  paths[i, "path.wkt"] <- st_as_text(st_cast(st_union(from$geometry, to$geometry), "LINESTRING"))
}
# reorder columns
paths <- paths[ , c("from.id", "from", "to.id", "to", "from.geom", "to.geom", "path.wkt", "dist.m", "route")]



# stat distances
gout <- ggplot(paths, aes(x = 0, y = dist.m)) +
  ggplot2::geom_boxplot(data = paths,
                        ggplot2::aes(x = 0, y = dist.m),
                        alpha = 0,
                        fatten = 1.5, width = 0.5, lwd = 0.3,
                        inherit.aes = FALSE) +
  ggplot2::geom_jitter(ggplot2::aes(color = "red"),
                       position = position_jitter(seed = 1),
                       size = 3, stroke = 0, alpha = 0.7) +
  ggplot2::geom_text_repel(data = paths,
                           position = position_jitter(seed = 1),
                           ggplot2::aes(x = 0, y = dist.m,
                                        label = paste0(from.id," <-> ", to.id))) +
  # geom_point(data = paths, aes(x = 0, y = dist.m),
  #            shape = 3,
  #            color = 'red') +
  ggplot2::theme_bw() +
  ggplot2::theme(legend.position = "none",
                 plot.title = element_text(size = 10)) +
  ggplot2::theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank()) +
  theme(axis.text.y = element_text(size = 8, angle = 90, vjust = 0, hjust=0.5)) +
  ylab("distance (m)") +
  # theme(axis.title.y = element_text("distance (m)")) +
  theme(axis.ticks.length = unit(2, "pt")) +
  theme(axis.ticks = element_line(colour = "black", size = 0.2)) +
  theme(panel.border = element_rect(colour= "black", size = 0.2)) +
  theme(panel.grid.major.x = element_blank()) +
  theme(panel.grid.minor.x =  element_blank()) +
  theme(panel.grid.major.y = element_line(colour = "lightgrey", size = 0.1)) +
  theme(panel.spacing = unit(2, "mm")) +
  theme(strip.text = element_text(size = 8),
        strip.background = element_rect(colour="black", size = 0.2)) +
  # scale_color_identity() +
  ggtitle("Distribution of distances between two caravan")

gout

ggplot2::ggsave(filename = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/stat_paths.png",
                plot = gout,
                height = 8,
                width = 5)

# caravan.geom <- unique(c(paths$from.geom, paths$to.geom))
# paths.caravans.geom <- paths$path.wkt
#
# ## map
# paths.caravans.geom.sf <- st_as_sf(paths, wkt = "path.wkt")
# st_crs(paths.caravans.geom.sf) <- 4326
# left <- as.numeric(sf::st_bbox(caravan.geom.sf)$xmin)
# bottom <- as.numeric(sf::st_bbox(caravan.geom.sf)$ymin)
# right <- as.numeric(sf::st_bbox(caravan.geom.sf)$xmax)
# top <- as.numeric(sf::st_bbox(caravan.geom.sf)$ymax)
# buffer <- mean(c(abs(left - right), abs(top - bottom)))/10
# bbox <- c(left = left - buffer,
#           bottom = bottom - buffer,
#           right = right + buffer,
#           top = top + buffer
# )
# stamenbck <- ggmap::get_stamenmap(bbox,
#                                   zoom = 8,
#                                   maptype = "terrain-background")
#
# caravan.geojson.point <- caravan.geom.sf[sf::st_geometry_type(caravan.geom.sf$geometry) == "POINT", ]
# caravan.geojson.line <- caravan.geom.sf[sf::st_geometry_type(caravan.geom.sf$geometry) == "LINESTRING", ]
# caravan.geojson.polygon <- caravan.geom.sf[sf::st_geometry_type(caravan.geom.sf$geometry) == "POLYGON", ]
#
# mout <- ggmap::ggmap(stamenbck) +
#   ggplot2::geom_sf(data = paths.caravans.geom.sf,
#                    aes(colour = route),
#                    # colour = "black",
#                    inherit.aes = FALSE) +
#   ggplot2::geom_sf(data = caravan.geojson.point,
#                    colour = "black",
#                    inherit.aes = FALSE) +
#   ggplot2::geom_sf(data = caravan.geojson.line,
#                    colour = "black",
#                    inherit.aes = FALSE) +
#   ggplot2::geom_sf(data = caravan.geojson.polygon,
#                    colour = "black",
#                    inherit.aes = FALSE) +
#   ggrepel::geom_text_repel(data = caravan.geojson.point,
#                            ggplot2::aes(x = sf::st_coordinates(caravan.geojson.point)[, "X"],
#                                         y = sf::st_coordinates(caravan.geojson.point)[, "Y"],
#                                         label = rownames(caravan.geojson.point)),
#                            size = 2,
#                            segment.color = "red",
#                            segment.size = .1,
#                            segment.alpha = .5,
#                            min.segment.length = .3,
#                            force = .5,
#                            max.time = 1.5,
#                            max.overlaps = Inf,
#                            inherit.aes = FALSE) +
#   ggrepel::geom_text_repel(data = caravan.geojson.polygon,
#                            ggplot2::aes(x = sf::st_coordinates(sf::st_centroid(caravan.geojson.polygon))[, "X"],
#                                         y = sf::st_coordinates(sf::st_centroid(caravan.geojson.polygon))[, "Y"],
#                                         label = rownames(caravan.geojson.polygon)),
#                            size = 2,
#                            segment.color = "red",
#                            segment.size = .1,
#                            segment.alpha = .5,
#                            min.segment.length = .3,
#                            force = .5,
#                            max.time = 1.5,
#                            max.overlaps = Inf,
#                            inherit.aes = FALSE) +
#   # ggplot2::labs(title = "caravan",
#   #               subtitle = paste0(field.name, " = ", field.value)) +
#   ggplot2::theme(plot.title = ggplot2::element_text(size = 15,
#                                                     hjust = 0.5),
#                  plot.subtitle = ggplot2::element_text(size = 12,
#                                                        hjust = 0.5))
# mout
#
# # mout <- ggmap::ggmap(stamenbck) +
# #   ggplot2::geom_sf(data = paths.caravans.geom.sf,
# #                    aes(colour = route),
# #                    # colour = "black",
# #                    inherit.aes = FALSE) +
# #   ggplot2::geom_sf(data = caravan.geom.sf,
# #                    colour = "black",
# #                    inherit.aes = FALSE) +
# #   ggrepel::geom_text_repel(data = caravan.geom.sf,
# #                            ggplot2::aes(x = sf::st_coordinates(caravan.geom.sf)[, "X"],
# #                                         y = sf::st_coordinates(caravan.geom.sf)[, "Y"],
# #                                         label = rownames(caravan.geom.sf)),
# #                            size = 2,
# #                            max.overlaps = Inf,
# #                            inherit.aes = FALSE) +
# #   # ggplot2::labs(title = "caravan",
# #   #               subtitle = paste0(field.name, " = ", field.value)) +
# #   ggplot2::theme(plot.title = ggplot2::element_text(size = 15,
# #                                                     hjust = 0.5),
# #                  plot.subtitle = ggplot2::element_text(size = 12,
# #                                                        hjust = 0.5))
# # mout
# ggplot2::ggsave(filename = "C:/Rprojects/eamena-arches-dev/projects/caravanserail/map_paths_3.png",
#                 plot = mout,
#                 height = 11,
#                 width = 14)


