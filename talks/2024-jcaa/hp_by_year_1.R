# Creates an array of maps showing the number of HP created each year

# library(eamenaR)
source("C:/Rprojects/eamenaR/R/ref_hps_1.R")
`%>%` <- dplyr::`%>%` # used to not load dplyr
d <- hash::hash()

source("C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.R") # the Pg connection (hidden pwd)

# Heritage places created during the year 2023 as a GeoJSON file
d <- ref_hps_1(db.con = db.con,
               date.after = '2012-12-31',
               date.before = '2032-12-31',
               d = d,
               stat.name = "hps_all")
df <- d$hps_all
df <- df %>%
  dplyr::mutate(cdate = as.POSIXct(cdate)) %>%
  dplyr::group_by(ei) %>%
  dplyr::filter(cdate == min(cdate)) %>%
  dplyr::ungroup() %>%
  dplyr::mutate(cdate = format(cdate, "%Y")) %>%
  dplyr::select(-ei, -teamname) %>%
  dplyr::arrange(desc(cdate))
sf_df <- sf::st_as_sf(df, coords = c("x", "y"), crs = 4326)
sf_df <- sf::st_transform(sf_df, 3857)

buff <- 2 ; countries <- rnaturalearth::ne_countries(scale = "medium", returnclass = "sf")

GSpath <- "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/grids/"
GSnew <- sf::st_read(paste0(GSpath, "EAMENA_Grid_contour.geojson"))
GSold <- sf::st_read(paste0(GSpath, "(archives)/EAMENA_Grid_contour.geojson"))

ggmap::register_stadiamaps("aa5c9739-90c7-410b-9e9b-6c904df6e4dd")
stamenbck <- ggmap::get_stadiamap(bbox = c(left = as.numeric(sf::st_bbox(GSnew)$xmin),
                                           bottom = as.numeric(sf::st_bbox(GSnew)$ymin),
                                           right = as.numeric(sf::st_bbox(GSnew)$xmax),
                                           top = as.numeric(sf::st_bbox(GSnew)$ymax)),
                                  maptype = "stamen_terrain_background",
                                  crop = FALSE,
                                  zoom = 6)
lg <- list()
for(year in unique(sf_df$cdate)){
  GS <- GSold
  if(as.integer(year) > 2022){
    GS <- GSnew
  }
  sf_df1 <- sf_df[sf_df$cdate == year, ]
  nb_hp <- nrow(sf_df1)
  ggy <- ggmap::ggmap(stamenbck) +
    # ggplot2::geom_sf(data = ea.geojson, fill = 'red', inherit.aes = FALSE) +
    ggplot2::geom_sf(data = GS, fill = NA, color = "black", size = 0.5, inherit.aes = FALSE) +
    ggplot2::geom_sf(data = sf_df1, color = "black", size = 1, inherit.aes = FALSE) +
    ggplot2::labs(title = year,
                  caption = paste0("Heritage places created = ", nb_hp),
                  x = "",
                  y = "") +
    ggplot2::theme_minimal()
  lg[[length(lg) + 1]] <- ggy
  print(paste("map: ", year, " is done"))
}

margin <- ggplot2::theme(plot.margin = ggplot2::unit(c(.2, -.1, .2, -.1), "cm"))
plots_with_margin <- lapply(lg, "+", margin)
arranged_plots <- gridExtra::arrangeGrob(grobs = plots_with_margin, ncol = 3)
title_grob <- grid::textGrob("Heritage places in the EAMENA database by years", gp = grid::gpar(fontsize = 20, fontface = "bold"))
subtitle_grob <- grid::textGrob(paste0("n = ", nrow(sf_df)), gp = grid::gpar(fontsize = 16))
final_plot <- gridExtra::grid.arrange(
  arranged_plots,
  top = title_grob,
  bottom = subtitle_grob
)
ggplot2::ggsave(
  file = "C:/Rprojects/eamena-arches-dev/talks/2024-jcaa/hps.png",
  plot = final_plot,
  height = 12, width = 19
)
# ggplot2::ggsave(file = "C:/Rprojects/eamena-arches-dev/projects/kites/hps1.png",
#                 gridExtra::arrangeGrob(grobs = lapply(lg, "+", margin), ncol = 3),
#                 height = 15, width = 17)
