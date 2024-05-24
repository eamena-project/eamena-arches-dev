# Read a Zenodo file
# works with geojson_map_1()
map.name <- "sistan_zenodo"
all.g <- geojson_map(map.name = map.name,
                     field.names = c("Damage Extent Type"),
                     geojson.path = "https://doi.org/10.5281/zenodo.10375902",
                     max.maps = 6,
                     hp.color = "black",
                     hp.color.bck = "grey",
                     hp.size = 1.5)
margin <- ggplot2::theme(plot.margin = ggplot2::unit(c(0.2, 0.2, 0.2, 0.2), "cm"))
ggplot2::ggsave(file = paste0("C:/Rprojects/eamena-arches-dev/talks/2024-jcaa/", map.name, ".png"),
                gridExtra::arrangeGrob(#top = field.name,
                  top = grid::textGrob("Damage Extent Type", gp = grid::gpar(fontsize = 14)),
                  grobs = lapply(all.g, "+", margin), ncol = 3),
                width = 18,
                height = 12)
