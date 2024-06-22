library(eamenaR)

rootDir <- "C:/Rprojects/eamena-arches-dev/talks/2024-aram/"


cvn <- geojson_map_path(geojson.path = paste0(system.file(package = "eamenaR"),
                                              "/extdata/caravanserail.geojson"),
                        csv.path = paste0(system.file(package = "eamenaR"),
                                          "/extdata/caravanserail_paths.csv"),
                        map.name = "caravanserail_paths",
                        export.plot = F)
