# For eamenaR

## GE Imagery Acquisition Date
# https://stackoverflow.com/questions/10770698/understanding-dates-and-plotting-a-histogram-with-ggplot2-in-r

geojson.path <- "C:/Users/Thomas Huet/Desktop/Sistan/data/sistan_part1_hps.geojson"
ea.geojson <- sf::read_sf(geojson.path)
ge.dates <- ea.geojson[["GE Imagery Acquisition Date"]]
ge.dates <- trimws(unlist(strsplit(ge.dates, ",")))
ge.dates <- na.omit(ge.dates)
ge.dates <- as.Date(ge.dates)
# data <- data.frame(ge.dates)
df <- as.data.frame(t(table(ge.dates)))
df$ge.dates <- as.Date(df$ge.dates)
# Plot
ggplot2::ggplot(df, ggplot2::aes(x = ge.dates, y = Freq)) +
  ggplot2::ggtitle("GE Imagery Acquisition Date") +
  # ggplot2::geom_histogram(stat = "count", binwidth = 1) +
  ggplot2::geom_col() +
  # ggplot2::scale_x_date(date_labels = "%Y-%m-%d", date_breaks = "1 day") +
  ggplot2::scale_y_log10() +
  ggplot2::xlab("Date") +
  ggplot2::ylab("Frequency")

# # # #

library(lubridate)
library(ggplot2)
library(plotly)

ggplot(df, aes(x=ge.dates)) +
  theme_bw() +  geom_histogram(binwidth=7, fill="darkblue",color="black") +
  labs(x="Fecha", y="Nº casos") +
  theme(axis.text.x=element_text(angle=60, hjust=1)) +
  scale_x_date(date_breaks = "weeks", date_labels = "%d-%m-%Y")

# # # #

library(ggplot2)
library(lubridate)

ge.dates <- as.Date(ge.dates)
df <- data.frame(date = ge.dates)
df$week <- floor_date(df$date, "week")
df_week_counts <- aggregate(date ~ week, data=df, FUN=length)
ggplot(df_week_counts, aes(x = week, y = date)) +
  geom_col() +
  scale_x_date(date_labels = "%Y-%m-%d", date_breaks = "1 week") +
  labs(x = "Week", y = "Counts", title = "Weekly Counts of Dates") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))



# # # #

hist(ge.dates, breaks = "weeks", format = "%Y-%m-%d", main = "GE Imagery Acquisition Date")

# # # #

library("ggplot2")
library("scales")

dates <- read.csv("http://pastebin.com/raw.php?i=sDzXKFxJ", sep=",", header=T)
dates$Date <- as.Date(dates$Date)
dates$num <- as.numeric(dates$Date)
bin <- 60 # used for aggregating the data and aligning the labels
p <- ggplot(dates, aes(num, ..count..))
p <- p + geom_histogram(binwidth = bin, colour="white")
p <- p + scale_x_date(breaks = seq(min(dates$num)-20, # change -20 term to taste
                                   max(dates$num),
                                   bin),
                      labels = date_format("%Y-%b"),
                      limits = c(as.Date("2009-01-01"),
                                 as.Date("2011-12-01")))
p <- p + theme_bw() +
  xlab(NULL) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))
p

#####################################################################
## list the Grids num

d <- hash::hash()
db.con <- RPostgres::dbConnect(drv = RPostgres::Postgres(),
                               user = NA,
                               password = NA,
                               dbname = 'eamena',
                               host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                               port = 5432)

library(eamenaR)
gridid <- eamenaR::ref_ids("Grid.ID",
                           choice = "db.concept.uuid")
hpgrid <- eamenaR::ref_ids("hp.grid",
                           choice = "db.concept.uuid")
sqll <- stringr::str_interp(
  "
    SELECT q1.grid_id, q1.nb_hp, q2.grid_num
    FROM (
        SELECT COUNT(resourceinstanceid::text) AS nb_hp,
            tiledata -> '${hpgrid}' #>> '{0, resourceId}' AS grid_id
        FROM tiles
        WHERE tiledata ->> '${hpgrid}' IS NOT NULL
        GROUP BY grid_id
    ) q1
    INNER JOIN(
        SELECT resourceinstanceid::text AS grid_id,
            tiledata -> '${gridid}' -> 'en' ->> 'value' AS grid_num
        FROM tiles
        WHERE tiledata -> '${gridid}' IS NOT NULL
    ) q2
    ON q1.grid_id = q2.grid_id;
  "
)
gs <- DBI::dbGetQuery(db.con, sqll)
pat <- "^[EW]\\d{2}N\\d{2}-\\d{2}$"
l.not.matching <- c()
for(i in seq(1, nrow(gs))){
  grid.num <- gs[i, "grid_num"]
  if(!stringr::str_detect(grid.num, pat)){
    l.not.matching <- c(l.not.matching, grid.num)
  }
}
l.not.matching.b <- sort(paste0(" - [ ] ", l.not.matching))
cat(l.not.matching.b, sep = "\n")


#####################################################################
# Sistan data paper, functions
# load eamenaR functions

geojson.path <- "C:/Users/Thomas Huet/Desktop/Sistan/data/sistan_OK_OK.geojson"
ea.geojson <- sf::read_sf(geojson.path)
# ea.geojson <- sf::st_transform(ea.geojson, crs = 3857)
bbox <- sf::st_as_sfc(sf::st_bbox(ea.geojson))
bbox <- sf::st_as_sf(bbox)
# bbox <- sf::st_transform(bbox,  crs = sf::st_crs(3857))

# ext$geometry <- bbox$x
# bbox <- sf::st_transform(bbox, crs = 3857)

library(basemaps)
data(ext)
# data(bbox)
set_defaults(map_service = "esri", map_type = "world_imagery")
# basemaps::get_maptypes()
library(ggplot2)
ggplot() +
  basemap_gglayer(bbox) +
  scale_fill_identity() +
  coord_sf()

library(ggmap)
ggmap::register_stadiamaps("aa5c9739-90c7-410b-9e9b-6c904df6e4dd")
stamenbck <- get_stadiamap(bbox = c(left = as.numeric(sf::st_bbox(ea.geojson)$xmin),
                                    bottom = as.numeric(sf::st_bbox(ea.geojson)$ymin),
                                    right = as.numeric(sf::st_bbox(ea.geojson)$xmax),
                                    top = as.numeric(sf::st_bbox(ea.geojson)$ymax)),
                           maptype = "stamen_terrain_background",
                           crop = FALSE,
                           zoom = 10)
ggmap::ggmap(stamenbck) +
  ggplot2::geom_sf(data = ea.geojson, fill = 'red',
                    inherit.aes = FALSE)

# plot map
ggmap(myMap)


# or, when combined with an sf vector object,
# make sure to use Web/Pseudo Mercator (EPSG 3857), as this is
# the CRS in which all basemaps are returned (see "Value"):
library(sf)
ext <- st_transform(ext,  crs = st_crs(3857))
ggplot() +
  basemap_gglayer(ext) +
  geom_sf(data = ext, color = "red", fill = "transparent") +
  coord_sf() +
  scale_fill_identity()



library(dplyr)

# List GS which have 0 HPs

ea.geojson.grids <- sf::read_sf(geojson.grids)
plot(ea.geojson.grids)
cat(sort(setdiff(ea.geojson.grids$square, ea.geojson$`Grid ID`)), sep = ", ")
# - - - - - - - - -


# grids_nb_hp <- as.data.frame(table(ea.geojson$`Grid ID`))
# colnames(grids_nb_hp) <- c("GridID", "n")
# grids_nb_hp <- grids_nb_hp[order(grids_nb_hp$GridID),]


setwd("C:/Rprojects/eamenaR")
source("R/ref_periods.R")
# ...

# Basic statistics
source("R/geojson_stat.R")
geojson_stat(geojson.path = geojson.path, stat = "stats", chart.type = "basics")

# # checks
# bronze.age.hp <- "EAMENA-0165008"
# ea.geojson <- sf::read_sf(geojson.path)
# head(ea.geojson$`EAMENA ID`)
# bronze.age.hp %in% ea.geojson$`EAMENA ID`

# field.names = c("Disturbance Cause Category Type")
# symbology = paste0(system.file(package = "eamenaR"),
#                    "/extdata/symbology.xlsx")
# dirOut = "C:/Users/Thomas Huet/Desktop/Sistan/out/"
# map.name = "img2"
# fig.width = 16
# fig.height = 16

# geojson.path.2 <- "C:/Users/Thomas Huet/Desktop/Sistan/data/temp3857.geojson"
# ea.geojson.2 <- sf::read_sf(geojson.path.2)
# ea.geojson.point.all <- sf::st_transform(ea.geojson, crs = 3857)
source("R/geojson_map_1.R")
geojson.path <- "C:/Users/Thomas Huet/Desktop/Sistan/data/sistan_OK_OK.geojson"
geojson.grids <- "C:/Users/Thomas Huet/Desktop/Sistan/data/sistan_grids_OK_OK_OK.geojson"
geojson_map(map.name = "img7",
            geojson.path = geojson.path,
            geojson.grids = geojson.grids,
            field.names = c("Disturbance Cause Category Type"),
            dirOut = "C:/Users/Thomas Huet/Desktop/Sistan/out/",
            symbology = paste0(system.file(package = "eamenaR"),
                               "/extdata/symbology.xlsx"),
            hp.color = "black",
            hp.color.bck = "#a3a3a3",
            hp.size = 1,
            ncol = 2,
            # maptype = list("osm", "topographic"),
            fig.width = 14,
            fig.height = 19,
            max.maps = 6,
            export.plot = T)

#
# ggsave(file = paste0(chm.analysis,"sens.png"),
#        arrangeGrob(grobs = lapply(lg.angles, "+", margin),
#                    top = grid::textGrob(mytit,x=0,hjust=0,gp = gpar(fontsize =10)),
#                    padding = unit(0.1, "line"), ncol = 5),
#        width = nrow(l.objet)/1.5)



#
# # Disturbance map
# source("R/geojson_map.R")
# geojson_map(geojson.path,
#             map.name = "xxx",
#             field.names = c("Disturbance Cause Category Type"),
#             export.plot = F)
#
#
# library(basemaps)
# data(ext)
# set_defaults(map_service = "osm", map_type = "topographic")
# basemaps::get_maptypes()
# library(ggplot2)
# ggplot() +
#   basemap_gglayer(bbox) +
#   scale_fill_identity() +
#   coord_sf()
#
# library(basemaps)
# data(ext)
# # or use draw_ext() to interactively draw an extent yourself
#
# # view all available maps
# get_maptypes()
#
# # set defaults for the basemap
# set_defaults(map_service = "osm", map_type = "topographic")
#
# # load and return basemap map as class of choice, e.g. as image using magick:
# basemap_magick(ext)

basemaps::get_maptypes()
