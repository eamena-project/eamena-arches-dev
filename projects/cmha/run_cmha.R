rootDir <- "C:/Users/TH282424/Rprojects/eamena-arches-dev/projects/cmha/data/"
hps <- "NQT0.geojson"
wn.geojson <- sf::read_sf(paste0(rootDir, hps))
missing.data <- c(NA, "")

output <- unname(unlist(wn.geojson))
exist.data <- subset(output, !(output %in% missing.data))
length(exist.data) # number of existing values
length(exist.data)/14 # average number of existing values by HP (max: 98)
(length(exist.data)/98)/14 # average percent of existing values for the 14 HPs
