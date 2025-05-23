# devtools::install_github("eamena-project/eamenaR")

# library(eamenaR)
library(sf)
library(dplyr)
library(units)

rootDir <- "C:/Users/TH282424/Rprojects/eamena-arches-dev/talks/2025-aram/"
rootDirOut <- paste0(rootDir, "out/")
cvns.qnts.file <- "cvns-qnts.geojson"
CVNS.path <- paste0(rootDir, "caravanserail_paths_1.csv")
# CVNS <- paste0(rootDir, "cvns_1.geojson")



#### Dataset curation ##################################
# cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))
# selected fields
# cvns.qnts.geojson <- cvns.qnts.geojson[, c("EAMENA ID", "Site Feature Interpretation Type")]
# CVNS & QNTS
# site.feat.interp <- cvns.qnts.geojson[["Site Feature Interpretation Type"]]
### Conditions
cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))
cvns.qnts.geojson <- cvns.qnts.geojson[, c("EAMENA ID", "Site Feature Interpretation Type", "Overall Condition State Type", "Disturbance Cause Category Type")]

# remove duplicated
cvns.qnts.geojson <- cvns.qnts.geojson %>%
  distinct(`EAMENA ID`, .keep_all= TRUE)
nrow(cvns.qnts.geojson)

site.feat.interp <- cvns.qnts.geojson[["Site Feature Interpretation Type"]]
cvns.geojson <- cvns.qnts.geojson[grep("Caravanserai/Khan", site.feat.interp), ]
qnts.geojson <- cvns.qnts.geojson[grep("Qanat/Foggara", site.feat.interp), ]
# cvns.geojson <- cvns.qnts.geojson[grep("Caravanserai/Khan", site.feat.interp), ]

# CVNS
# duplicated
n_occur <- data.frame(table(cvns.geojson$`EAMENA ID`))
# cvns.geojson <- cvns.geojson[cvns.geojson$`EAMENA ID` %in% n_occur$Var1[n_occur$Freq == 1],]

cvns.geojson <- cvns.geojson[!sf::st_geometry_type(cvns.geojson) %in% c("POLYGON", "MULTIPOLYGON", "LINESTRING"), ]
# nb of CVNS by geometries
nrow(cvns.geojson[sf::st_geometry_type(cvns.geojson) == 'POINT', ])
nrow(cvns.geojson[sf::st_geometry_type(cvns.geojson) == 'POLYGON', ])

# QNT
qnts.geojson <- cvns.qnts.geojson[grep("Qanat/Foggara", site.feat.interp), ]
# Lines
qnts.geojson <- qnts.geojson[!sf::st_geometry_type(qnts.geojson) %in% c("POLYGON", "MULTIPOLYGON", "POINT"), ]
# nb of qanats by geometries
nrow(qnts.geojson[sf::st_geometry_type(qnts.geojson) == 'POINT', ])
nrow(qnts.geojson[sf::st_geometry_type(qnts.geojson) == 'LINESTRING', ])

### Overall Condition State Type #######################################
# CVNS
source("R/geojson_stat.R")
gout <- geojson_stat(geojson.path = cvns.geojson,
                     stat.name = "overall_cond",
                     stat = "stats",
                     field.names = c("Overall Condition State Type"))
gout <- gout +
  ggplot2::labs(title = "Caravanserai/Khan",
                subtitle = paste0("n = ", nrow(cvns.geojson)),
                caption = paste0("Data source:", cvns.qnts.file))
ggplot2::ggsave(paste0(rootDirOut, "cond-cvns.jpg"), gout, width = 6, height = 4)
# QNTS
gout <- geojson_stat(geojson.path = qnts.geojson,
                     stat.name = "overall_cond",
                     stat = "stats",
                     field.names = c("Overall Condition State Type"))
gout <- gout +
  ggplot2::labs(title = "Qanat/Foggar",
                subtitle = paste0("n = ", nrow(qnts.geojson)),
                caption = paste0("Data source:", cvns.qnts.file))
ggplot2::ggsave(paste0(rootDirOut, "cond-qnts.jpg"), gout, width = 6, height = 4)

######## Disturbance Cause Category Type #######################################
# CVNS
source("R/geojson_stat.R")
gout <- geojson_stat(geojson.path = cvns.geojson,
                     chart.type = "hist",
                     field.names = c("Disturbance Cause Category Type"),
                     stat = "stats")
gout <- gout +
  ggplot2::labs(title = "Caravanserai/Khan",
                subtitle = paste0("n = ", nrow(cvns.geojson)),
                caption = paste0("Data source:", cvns.qnts.file))
ggplot2::ggsave(paste0(rootDirOut, "disturb-cvns.jpg"), gout, width = 9, height = 6)
# QNTS
gout <- geojson_stat(geojson.path = qnts.geojson,
                     chart.type = "hist",
                     field.names = c("Disturbance Cause Category Type"),
                     stat = "stats")
gout <- gout +
  ggplot2::labs(title = "Qanat/Foggar",
                subtitle = paste0("n = ", nrow(qnts.geojson)),
                caption = paste0("Data source:", cvns.qnts.file))
ggplot2::ggsave(paste0(rootDirOut, "disturb-qnts.jpg"), gout, width = 9, height = 6)

#############################
# x,y map
source("R/geojson_map_path.R")
source("R/geojson_format_path.R")
source("R/geojson_stat.R")
d <- hash::hash()
d[['cvns']] <- cvns.geojson
d <- geojson_map_path(d = d,
                      # geojson.path = CVNS,
                      geojson.path = d[['cvns']],
                      csv.path = CVNS.path,
                      show.ids = TRUE,
                      lbl.size = 2.5,
                      map.name = "Khorasan caravanserais network")
d$map
# the map
ggplot2::ggsave(paste0(rootDirOut, "map_paths_ids.jpg"),
                d$map,
                width = 14, height = 11)
# the df
write.table(d$ids, paste0(rootDirOut, "caravanserais_id.tsv"), sep = "\t", row.names = FALSE)
# st_write(d$paths, paste0(rootDirOut, "cvns_qnts_CVNS_paths.geojson"), append=FALSE)

#############################
# boxplot distances btw CVN
source("R/geojson_boxplot.R")
source("R/geojson_map_path.R")
source("R/geojson_format_path.R")
source("R/geojson_stat.R")
source("R/ref_routes.R")
gout <- geojson_boxplot(geojson.path = cvns.geojson,
                        by = "route",
                        csv.path = CVNS.path,
                        stat = "dist")
ggplot2::ggsave(paste0(rootDirOut, "boxplot_distances.jpg"),
                gout,
                width = 7,
                height = 6)

#############################
# thematic map
geojson_map(map.name = "caravanserail",
            field.names = c("Damage Extent Type"),
            fig.width = 11,
            export.plot = T)


#######################################
# closest
# cvns.qnts.geojson <- sf::read_sf(paste0(rootDir, cvns.qnts.file))
# # selected fields
# cvns.qnts.geojson <- cvns.qnts.geojson[, c("EAMENA ID", "Site Feature Interpretation Type")]
# # CVNS & QNTS
# site.feat.interp <- cvns.qnts.geojson[["Site Feature Interpretation Type"]]
# cvns.geojson <- cvns.qnts.geojson[grep("Caravanserai/Khan", site.feat.interp), ]
# # Points
# cvns.geojson <- cvns.geojson[!sf::st_geometry_type(cvns.geojson) %in% c("POLYGON", "MULTIPOLYGON", "LINESTRING"), ]
# qnts.geojson <- cvns.qnts.geojson[grep("Qanat/Foggara", site.feat.interp), ]
# # Lines
# qnts.geojson <- qnts.geojson[!sf::st_geometry_type(qnts.geojson) %in% c("POLYGON", "MULTIPOLYGON", "POINT"), ]
# checks geometry types
unique(st_geometry_type(qnts.geojson)) # LINESTRING only
unique(st_geometry_type(cvns.geojson)) # POINT only


source(paste0(rootDir, "closest_HP1_to_HP2.R"))
df.closest <- closest_HP1_to_HP2(cvns.geojson, qnts.geojson)
# write GeoJSON
df.closest <- st_transform(df.closest, crs = 4326)
# get rid of transparency (for QGIS)
df.closest$dist_color <- gsub("FF$", "", df.closest$dist_color)
st_write(df.closest, paste0(rootDirOut, "cvns_qnts_closest_lines_1.geojson"), append=FALSE)
cvns.geojson <- st_transform(cvns.geojson, crs = 4326)
cvns.geojson$dist2qnt_meters <- df.closest$dist
cvns.geojson$dist2qnt_color <- df.closest$dist_color
cvns.geojson$dist2qnt_labels <- df.closest$labels
st_write(cvns.geojson, paste0(rootDirOut, "cvns_qnts_CVNS_1.geojson"), append=FALSE)
qnts.geojson <- st_transform(qnts.geojson, crs = 4326)
st_write(qnts.geojson, paste0(rootDirOut, "cvns_qnts_QNTS_1.geojson"), append=FALSE)

# reusable labels
lbl.dist.log <- "Distance (m), logarithmic scale"
lbl.tit <- "Distance between caravanserais and their closest qanat (in meters)"
lbl.capt <- paste0("Data source:", "cvns-qnts.geojson")

subtit <- paste0("Khorasan caravanserais (n=", nrow(cvns.geojson),") and qanats (n=", nrow(qnts.geojson),")")

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
  ggplot2::ylab(lbl.dist.log) +
  ggplot2::labs(title = paste0(lbl.tit),
                subtitle = subtit,
                caption = lbl.capt) +
  ggplot2::theme_bw() +
  my_theme
gout
ggplot2::ggsave(paste0(rootDirOut, "map_distances.jpg"),
                gout,
                width = 5, height = 7)

#
rounded <- 10
df.closest.df <- as.data.frame(df.closest)
df.closest.df$dist <- round(df.closest.df$dist/rounded) * rounded
df.closest.df <- as.data.frame(table(df.closest.df$dist))
df.closest.df$Var1 <- as.integer(as.character(df.closest.df$Var1))
# change to histogram?
gout <- ggplot(df.closest.df, ggplot2::aes(x = Var1, y = Freq))
# gout <- ggplot(df.closest, ggplot2::aes(x = dist))
for (i in seq_len(nrow(df.colors))) {
  # loop_input <- paste0("geom_rect(aes(xmin = df.colors[", i ,", 'from'], xmax = df.colors[", i, ", 'to'], ymin = -Inf, ymax = Inf), fill = df.colors[", i,", 'dist_color'])")
  # annotae accepts alpha (unlike geom_rect)
  loop_input <- paste0("annotate(geom = 'rect', xmin = df.colors[", i ,", 'from'], xmax = df.colors[", i, ", 'to'], ymin = -Inf, ymax = Inf, fill = df.colors[", i,", 'dist_color'], alpha = 1)")
  gout <- gout + eval(parse(text=loop_input))
}
gout <- gout +
  # ggplot2::geom_line(ggplot2::aes(color = "black"), size = .5) +
  ggplot2::geom_histogram(binwidth = 10, fill = "blue", color = "black", alpha = 0.7) +
  ggplot2::scale_x_log10(breaks = c(1, 10, 20, 50, 100, 1000, 10000, ceiling(max(df.closest.df$Var1) / 100) * 100),
                         labels = scales::comma) +
  labs(title = lbl.tit,
       caption = lbl.capt,
       x = lbl.dist.log,
       y = "Number of caravanserais") +
  ggplot2::scale_y_continuous(breaks = scales::breaks_pretty()) +
  ggplot2::scale_colour_identity() +
  ggplot2::theme_bw()
gout
ggsave(paste0(rootDirOut, "dist_distances.jpg"), gout, width = 6, height = 5)

#######################################
# Ordinal Logistic regression on HP conservations (CVN <-> QNT)
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
df.closest.condition <- df.closest[ , -which(names(df.closest) %in% c("dist", "dist_color", "labels", "from", "to"))]
# fetch conditions
df.closest.condition <- df.closest.condition %>%
  left_join(cvns.qnts.geojson, by = c("cvn" = "EAMENA ID"))
names(df.closest.condition)[names(df.closest.condition) == 'Overall Condition State Type'] <- 'condition_cvn'
df.closest.condition <- df.closest.condition %>%
  left_join(cvns.qnts.geojson, by = c("qnt" = "EAMENA ID"))
names(df.closest.condition)[names(df.closest.condition) == 'Overall Condition State Type'] <- 'condition_qnt'
#
head(df.closest.condition)
# rm Unknown, '', etc.
to.rm <- c('', 'Unknown')
df.closest.condition.rm.unkn <- df.closest.condition[!(df.closest.condition$condition_cvn) %in% to.rm, ]
df.closest.condition.rm.unkn <- df.closest.condition.rm.unkn[!(df.closest.condition.rm.unkn$condition_qnt) %in% to.rm, ]
df.closest.condition.rm.unkn <- df.closest.condition.rm.unkn %>%
  left_join(conservation.scale, by = c("condition_cvn" = "cons.label"))
names(df.closest.condition.rm.unkn)[names(df.closest.condition.rm.unkn) == 'cons.value'] <- 'condition_cvn_value'
df.closest.condition.rm.unkn <- df.closest.condition.rm.unkn %>%
  left_join(conservation.scale, by = c("condition_qnt" = "cons.label"))
names(df.closest.condition.rm.unkn)[names(df.closest.condition.rm.unkn) == 'cons.value'] <- 'condition_qnt_value'
head(df.closest.condition.rm.unkn)

# Logistic ordinal regression
df.closest.condition.rm.unkn$condition_cvn_value <- factor(df.closest.condition.rm.unkn$condition_cvn_value, ordered = TRUE)
df.closest.condition.rm.unkn$condition_qnt_value <- factor(df.closest.condition.rm.unkn$condition_qnt_value, ordered = TRUE)
df.closest.condition.rm.unkn.df <- sf::st_drop_geometry(df.closest.condition.rm.unkn)
df.closest.condition.rm.unkn.df <- df.closest.condition.rm.unkn.df[,c("condition_qnt_value", "condition_cvn_value")]
head(df.closest.condition.rm.unkn.df)
write.csv(df.closest.condition.rm.unkn.df, paste0(rootDirOut, "reg_conserv_cvn_qnt.csv"), row.names = F)

model <- MASS::polr(condition_cvn_value ~ condition_qnt_value, data = df.closest.condition.rm.unkn.df, Hess=TRUE, method="logistic")

summary(model)
# Check model AIC
AIC(model)

# Calculate standardized residuals
std_res <- residuals(model, type = "pearson")

# Plot standardized residuals
plot(std_res, main = "Standardized Residuals", ylab = "Standardized Residual", xlab = "Index")
abline(h = 0, col = "red")



model <- MASS::polr(condition_qnt_value ~ condition_cvn_value, data = df.closest.condition.rm.unkn, Hess = TRUE)
summary(model)
# run le reg log ord
source(paste0(rootDir, "closest_HP1_to_HP2_reg_log_ord.R"))
df.closest.condition.rm.unkn.df <- sf::st_drop_geometry(df.closest.condition.rm.unkn)
d <- closest_HP1_to_HP2_reg_log_ord(data = df.closest.condition.rm.unkn.df, x = "condition_cvn_value", y = "condition_qnt_value")
d$result_table






# profiles/section
source("R/geojson_addZ.R")
# e <- hash::hash()
d <- geojson_addZ(d = NA,
                  geojson.path = d[['cvns']])
# geojson.path = CVNS)

source("R/geojson_map_path_1.R")
source("R/geojson_stat.R")
d <- geojson_map_path(d = d,
                      geojson.path = d$withZ,
                      csv.path = CVNS.path,
                      map.name = "caravanserail_paths",
                      stats = "profile")

