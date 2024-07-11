closest_HP1_to_HP2 <- function(cvns.geojson, qnts.geojson, local.srid = 32640){
  # closest CVNS to QNTS, create a line from a CVNS (POINT) to QNTS (LINE)
  # convert CRS to WGS 84 / UTM zone 40N
  cvns_utm <- st_transform(cvns.geojson, crs = local.srid)
  qnts_utm <- st_transform(qnts.geojson, crs = local.srid)
  # Calculating the nearest features and the distances in meters
  cvns_utm$nearest_index <- st_nearest_feature(cvns_utm, qnts_utm)
  cvns_utm$distance_m <- st_distance(cvns_utm, qnts_utm[cvns_utm$nearest_index, ], by_element = TRUE) %>%
    set_units("m")
  # empty sf dataframe to store
  df.closest <- st_sf(
    cvn = character(),
    qnt = character(),
    dist = numeric(),
    geometry = st_sfc(crs = local.srid),  # Specify CRS appropriately
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
  df.closest <- df.closest %>%
    left_join(df.colors)
  return(df.closest)
}
