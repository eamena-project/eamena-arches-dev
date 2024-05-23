# Creates an array of map showing the number of HP created by year

library(eamenaR)
source("C:/Rprojects/eamenaR/R/ref_hps_1.R")
d <- hash::hash()
db.con <- RPostgres::dbConnect(drv = RPostgres::Postgres(),
                               user = 'postgres',
                               password = 'postgis',
                               dbname = 'eamena',
                               host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                               port = 5432)
# Heritage places created during the year 2023 as a GeoJSON file
d <- ref_hps_1(db.con = db.con,
               date.after = '2012-12-31',
               date.before = '2032-12-31',
               d = d,
               stat.name = "hps_all")
# df <- d$eamena_hps_all
# df$cdate <- as.POSIXct(df$cdate)
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

buff <- 2.5 ; countries <- rnaturalearth::ne_countries(scale = "medium", returnclass = "sf")

lg <- list()
for(year in unique(sf_df$cdate)){
  sf_df1 <- sf_df[sf_df$cdate == year, ]
  nb_hp <- nrow(sf_df1)
  ggy <- ggplot() +
    geom_sf(data = countries, fill = "white", color = "black", size = 0.5) +
    geom_sf(data = sf_df1, color = "black", size = 1) +
    theme_minimal() +
    labs(title = year,
         caption = paste0("Heritage places created = ", nb_hp),
         x = "",
         y = "") +
    ggplot2::coord_sf(xlim = c(sf::st_bbox(sf_df)[1] - buff, sf::st_bbox(sf_df)[3] + buff),
                      ylim = c(sf::st_bbox(sf_df)[2] - buff, sf::st_bbox(sf_df)[4] + buff))
  lg[[length(lg)+1]] <- ggy
}

margin <- ggplot2::theme(plot.margin = ggplot2::unit(c(.2, -.1, .2, -.1), "cm"))
ggplot2::ggsave(file = "C:/Rprojects/eamena-arches-dev/projects/kites/hps1.png",
                gridExtra::arrangeGrob(grobs = lapply(lg, "+", margin), ncol = 3),
                height = 15, width = 17)
