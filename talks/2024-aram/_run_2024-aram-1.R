library(eamenaR)
library(sf)
library(dplyr)
library(units)


rootDir <- "C:/Rprojects/eamena-arches-dev/talks/2024-aram/"
rootDirOut <- "C:/Rprojects/eamena-arches-dev/talks/2024-aram/out/"
cvns.qnts.file <- "cvns-qnts.geojson"
# CVNS <- paste0(rootDir, "cvns_1.geojson")

#######################################
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
# closest CVNS to QNTS, create a line from a CVNS (POINT) to QNTS (LINE)
# convert CRS to WGS 84 / UTM zone 40N
cvns_utm <- st_transform(cvns.geojson, crs = 32640)
qnts_utm <- st_transform(qnts.geojson, crs = 32640)
# Calculating the nearest features and the distances in meters
cvns_utm$nearest_index <- st_nearest_feature(cvns_utm, qnts_utm)
cvns_utm$distance_m <- st_distance(cvns_utm, qnts_utm[cvns_utm$nearest_index, ], by_element = TRUE) %>%
  set_units("m")
# empty sf dataframe to store
df.closest <- st_sf(
  cvn = character(),
  qnt = character(),
  dist = numeric(),
  geometry = st_sfc(crs = 32640),  # Specify CRS appropriately
  sf_column_name = "geometry"
)
# Loop over cvns to find and connect to the nearest qnts
for (i in seq_len(nrow(cvns_utm))) {
  # for (i in seq_len(8)) {
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

# library(viridis)
my.brk = 'jenks'
n.classes <- 5
distances <- df.closest$dist
if(my.brk == 'quantiles'){
  breaks <- quantile(distances, probs = seq(0, 1, length.out = 6))
  categories <- cut(distances, breaks = breaks, include.lowest = TRUE, labels = FALSE)
}
if(my.brk == 'jenks'){
  jenks_breaks <- classInt::classIntervals(distances, n = n.classes, style = "jenks")
  # cc <- cut(df.closest$dist,
  #                              breaks = c(jenks_breaks$brks),
  #                              include.lowest = TRUE,
  #                              right = TRUE)
  categories <- cut(df.closest$dist,
                    breaks = c(jenks_breaks$brks),
                    include.lowest = TRUE,
                    right = TRUE)
  labels <- c()
  from <- c()
  to <- c()
  for(i in seq_len(length(jenks_breaks$brks)-1)){
    from <- c(from, round(jenks_breaks$brks[i]))
    to <- c(to, round(jenks_breaks$brks[i+1]))
    labels <- c(labels, paste0("[", round(jenks_breaks$brks[i]), "-", round(jenks_breaks$brks[i+1]), "["))
  }
}
color_palette <- viridis::viridis(n.classes)
# get lighter values for smaller values
color_palette <- rev(color_palette)
df.closest$dist_color <- color_palette[categories]
df.colors <- data.frame(dist_color = color_palette,
                        labels = labels,
                        from = from,
                        to = to)
df.colors$dist_color <- gsub("FF$", "", df.colors$dist_color)

df.closest <- df.closest %>%
  left_join(df.colors)
# df.closest <- merge(df.closest, df.colors, by = "dist_color", all.x = T)
# write GeoJSON
df.closest <- st_transform(df.closest, crs = 4326)
st_write(df.closest, paste0(rootDirOut, "cvns_qnts_closest_lines.geojson"), append=FALSE)
cvns.geojson <- st_transform(cvns.geojson, crs = 4326)
cvns.geojson$dist2qnt_meters <- df.closest$dist
# get rid of transparency (for QGIS)
# cvns.geojson$dist2qnt_color <- gsub("FF$", "", df.closest$dist_color)
cvns.geojson$dist2qnt_labels <- df.closest$labels
st_write(cvns.geojson, paste0(rootDirOut, "cvns_qnts_CVNS_2.geojson"), append=FALSE)
qnts.geojson <- st_transform(qnts.geojson, crs = 4326)
st_write(qnts.geojson, paste0(rootDirOut, "cvns_qnts_QNTS.geojson"), append=FALSE)

# GGplot boxplot on distances
my_theme <- list(
  ggplot2::theme(legend.position = "none",
                 plot.title = ggplot2::element_text(size = 10),
                 plot.subtitle = ggplot2::element_text(size = 8),
                 axis.text.x = ggplot2::element_blank(),
                 axis.title.x = ggplot2::element_blank(),
                 axis.text.y = ggplot2::element_text(size = 8, angle = 90, vjust = 0, hjust=0.5),
                 axis.ticks.length = ggplot2::unit(2, "pt"),
                 axis.ticks = ggplot2::element_line(colour = "black", size = 0.2),
                 panel.border = ggplot2::element_rect(colour= "black", size = 0.2),
                 panel.grid.major.x = ggplot2::element_blank(),
                 panel.grid.minor.x =  ggplot2::element_blank(),
                 panel.grid.major.y = ggplot2::element_line(colour = "lightgrey", size = 0.1),
                 panel.spacing = ggplot2::unit(2, "mm"),
                 strip.text = ggplot2::element_text(size = 8),
                 strip.background = ggplot2::element_rect(colour="black", size = 0.2))
)
gout <- ggplot2::ggplot(df.closest, ggplot2::aes(x = 0, y = dist)) +
  ggplot2::geom_boxplot(data = df.closest,
                        # outlier.shape = NA,
                        ggplot2::aes(x = 0, y = dist),
                        alpha = 0,
                        fatten = 1.5,
                        width = 0.75,
                        lwd = 0.3) +
  ggplot2::geom_jitter(data = df.closest,
                       ggplot2::aes(color = dist_color),
                       position = ggplot2::position_jitter(w = 0.3),
                       size = 2,
                       stroke = 0,
                       alpha = 0.7) +
  ggplot2::stat_summary(fun = mean, geom = "point", shape = 3, size = 3, color = "red") +
  # ggplot2::stat_summary(fun = mean, geom = "text", ggplot2::aes(label = round(..y.., 2)), vjust = -0.5) +
  ggplot2::scale_y_log10(breaks = c(1, 10, 20, 50, 100, 1000, 10000, ceiling(max(df.closest$dist) / 100) * 100),
                         labels = scales::comma) +
  ggplot2::scale_colour_identity() +
  ggplot2::ylab("Distance (m), logarithmic scale") +
  ggplot2::labs(title = paste0("Distance between caravanserais and their closest qanat (in meters)"),
                subtitle = "Khorasan caravanserais and qanats, EAMENA database, July 2024",
                caption = paste0("Data source:", "cvns-qnts.geojson")) +
  ggplot2::theme_bw() +
  my_theme
gout
ggsave(paste0(rootDirOut, "map_distances.jpg"), gout, width = 5, height = 6)
# if(by != "by"){
#   gout <- gout +
#     ggplot2::facet_grid(. ~ df.measurements[[by]], scales = "free")
# }

# Create the density plot
# ggplot2::ggplot(df.closest, ggplot2::aes(x = dist)) +
#   ggplot2::geom_density() +
#   # ggplot2::stat_bin(binwidth = 0.5, geom = "line", ggplot2::aes(y = ..count..)) +
#   ggplot2::labs(title = "Density Plot of Values", x = "Value", y = "Density") +
#   ggplot2::theme_bw()

rounded <- 10
df.closest.df <- as.data.frame(df.closest)
df.closest.df$dist <- round(df.closest.df$dist/rounded) * rounded
df.closest.df <- as.data.frame(table(df.closest.df$dist))
df.closest.df$Var1 <- as.integer(as.character(df.closest.df$Var1))
# gout <- ggplot(df.closest.df, ggplot2::aes(x = Var1, y = Freq))
# loop over the viridis intervals to get colors
# for(i in seq_len(nrow(df.colors))){
#   print(i)
#   # i <- 1
#   gout <<- gout +
#     geom_rect(aes(xmin = df.colors[i, "from"], xmax = df.colors[i, "to"],
#                   ymin = -Inf, ymax = Inf),
#               fill = df.colors[i, "dist_color"])
#   # ggplot2::scale_colour_identity()
# }
# gout <- gout +
#   # geom_rect(data = df.colors,
#   #           aes(xmin = from, xmax = to,
#   #               ymin = -Inf, ymax = Inf,
#   #           fill = dist_color)) +
#   ggplot2::geom_line(df.closest.df, ggplot2::aes(x = Var1, y = Freq),
#                      color = "black", size = .5, inherit.aes = FALSE) +
#   ggplot2::scale_x_log10(breaks = c(1, 10, 20, 50, 100, 1000, 10000, ceiling(max(df.closest.df$Var1) / 100) * 100),
#                          labels = scales::comma) +
#   labs(title = "Count Plot of Values", x = "Value", y = "Count") +
#   ggplot2::scale_colour_identity() +
#   ggplot2::theme_bw()
#
# plotAllLayers<-function(df){
#   p <- ggplot()
#   for(i in seq_len(nrow(df))[-1]){
#     p <- p + geom_rect(aes(xmin = df[i, "from"], xmax = df[i, "to"],
#                   ymin = -Inf, ymax = Inf),
#               fill = df[i, "dist_color"])
#   }
#   return(p)
# }
# plotAllLayers(df.colors)


gout <- ggplot(df.closest.df, ggplot2::aes(x = Var1, y = Freq))
for (i in seq_len(nrow(df.colors))) {
  # loop_input <- paste0("geom_rect(aes(xmin = df.colors[", i ,", 'from'], xmax = df.colors[", i, ", 'to'], ymin = -Inf, ymax = Inf), fill = df.colors[", i,", 'dist_color'])")
  # annotae accepts alpha (unlike geom_rect)
  loop_input <- paste0("annotate(geom = 'rect', xmin = df.colors[", i ,", 'from'], xmax = df.colors[", i, ", 'to'], ymin = -Inf, ymax = Inf, fill = df.colors[", i,", 'dist_color'], alpha = 1)")
  gout <- gout + eval(parse(text=loop_input))
}
gout +
  ggplot2::geom_line(ggplot2::aes(color = "black"), size = .5) +
  # ggplot2::geom_line(df.closest.df, ggplot2::aes(x = Var1, y = Freq,
  #                    color = "black"), size = .5) +
  ggplot2::scale_x_log10(breaks = c(1, 10, 20, 50, 100, 1000, 10000, ceiling(max(df.closest.df$Var1) / 100) * 100),
                         labels = scales::comma) +
  labs(title = "Count Plot of Values",
       x = "Value",
       y = "Count") +
  ggplot2::scale_colour_identity() +
  ggplot2::theme_bw()


  # paste0("annotate(geom = 'rect', xmin = df.colors[", i ,", 'from'], xmax = df.colors[", i, ", 'to'], ymin = -Inf, ymax = Inf, fill = df.colors[", i,", 'dist_color'], alpha = 0.5)")
  #


df<-data.frame(x1=c(1:5),y1=c(2.0,5.4,7.1,4.6,5.0),y2=c(0.4,9.4,2.9,5.4,1.1),y3=c(2.4,6.6,8.1,5.6,6.3))

ggplot(data=df,aes(df[,1]))+geom_line(aes(y=df[,2]))+geom_line(aes(y=df[,3]))

##

#######################################
# conservation
# avoid Unknown
conservation.scale <- data.frame(
  cons.label = c("Good", "Fair", "Poor", "Very Bad", "Destroyed"),
  cons.value = c(1, 2, 3, 4, 5))

cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))
# selected fields
cvns.qnts.geojson <- cvns.qnts.geojson[ , c("EAMENA ID", "Overall Condition State Type")]
# CVNS & QNTS
cvns.qnts.geojson <- sf::st_drop_geometry(cvns.qnts.geojson)
# ...
df.closest <- df.closest[ , -which(names(df.closest) %in% c("dist", "dist_color", "labels"))]
df.closest.condition <- df.closest %>%
  left_join(cvns.qnts.geojson, by = c("cvn" = "EAMENA ID"))
names(df.closest.condition)[names(df.closest.condition) == 'Overall Condition State Type'] <- 'condition_cvn'
df.closest.condition <- df.closest.condition %>%
  left_join(cvns.qnts.geojson, by = c("qnt" = "EAMENA ID"))
names(df.closest.condition)[names(df.closest.condition) == 'Overall Condition State Type'] <- 'condition_qnt'
head(df.closest.condition)
# TODO: rm Unknown

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
st_write(d$paths, paste0(rootDirOut, "cvns_qnts_CVNS_paths.geojson"), append=FALSE)



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

