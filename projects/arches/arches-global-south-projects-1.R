#' Show the extension of the different Global South projects based in Arches in an interactive leaflet map.
#'
#' @name prj_arches_gs
#'
#' @description Creates a leaflet map (HTML widget) showing the extension of different Arches-powered projects
#'
#' @param bu.path the path to the BU folder. The BU folder (`bu/`) is the root of job folders (ex: 'mk/', see the 'job' option description). Each job contains one to several BU worksheets. The output subfolder `out/` will be created by the function to store the output files. BU files could be either XLSX or CSV.
#' @param bu.template.path the path to the BU template. The output will be written into this structure
#' @param mapping.file the path to the XLSX or Google Sheet file providing the equivalences (mapping) between the source file (unformatted) and the target file (formatted as a BU).
#' @param mapping.file.ggsheet is the mapping file a Google Sheet (for example: 'https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625'), by default: FALSE.
#' @param job the job folder is a subfolder of `bu/`. It contains the unformatted XLSX datasets. `job` is also the name of the source fields in the mapping file. By default 'mk'.
#' @param job.type the name of the field in the `mapping.file` XLSX giving the name of the mapping function to do:
#'   - 'field': one-to-one correspondences, the source values will be copied as it into the target file;
#'   - 'value': constant values (ie, always the same value) that will be copied into the target file;
#'   - 'expression': logical functions (mainly if statements). These functions are written directly in the appropriate cell of the mapping file;
#'   - 'escape': values depending from another column evaluated by 'expression'. This field is
#'       not read
#'   - 'other': when a column (ex: 'Seen') as a value (ex: 'Yes') that refers to several values scattered on different target columns.
#'   - 'supplem': to add supplementary rows like pipes '|' for already existing rows (ex: the alternative name of a place, two different actors)
#' @param eamena.field the name of the field in the `mapping.file` XLSX with the name of the EAMENA fields in a R format ('UNIQUEID', 'Assessment.Investigator.-.Actor', 'Investigator.Role.Type', etc.)
#' @param eamena.id the unique key identifier for a single resource, by default 'UNIQUEID'
#' @param verbose if TRUE (by default): verbose
#'
#' @return One or various XLSX files (almost) ready for an bulk upload process in the EAMENA DB. These files are names in the same way as the input file, except a `_out` suffix is added.
#'
#' @examples
#'
#' list_mapping_bu()
#'
#' list_mapping_bu(mapping.file = 'https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625',
#'                 mapping.file.ggsheet = T)
#'
#' @export
prj_arches_gs <- function(root.project = "https://raw.githubusercontent.com/achp-project/cultural-heritage/main/map-projects/",
                          list.projects = "list-projects.txt",
                          bck = paste0(root.project, "bckgrd/globalsouth.geojson"),
                          map.title = "<a href='https://www.archesproject.org/'>Arches</a> projects in the Global South",
                          col.ramp = "Set1",
                          export.map = TRUE,
                          dirOut = paste0(getwd(),"/projects/arches/"),
                          fileOut = "arches-global-south.html"){
  l.projects <- read.csv(paste0(root.project, list.projects), header = F)
  l.projects <- l.projects[ , 1]
  projects.colors <- RColorBrewer::brewer.pal(length(l.projects), col.ramp)
  gs <- geojsonsf::geojson_sf(bck)
  gs.globalsouth <- gs[!is.na(gs$globalsout), ]
  # leaflet map
  ggs <- leaflet::leaflet(gs.globalsouth,
                          width = "100%",
                          height = "100vh") %>%
    leaflet::addProviderTiles(providers$Stamen.Toner,
                              options = providerTileOptions(noWrap = TRUE)
    ) %>%
    leaflet::setView(lng = 53,
                     lat = 25,
                     zoom = 3) %>%
    leaflet::addPolygons(color = "red",
                         weight = 0,
                         opacity = .5,
                         fillOpacity = .5)
  if(verbose){
    print(paste0("loop over ", list.projects, " to add the project layers"))
  }
  for(i in seq(1, length(l.projects))){
    if(verbose){
      print(paste0(" - read: ", l.projects[i]))
    }
    arches.projects <- readLines(paste0(root.project, "geojson/", l.projects[i], ".geojson")) %>%
      paste(collapse = "\n") %>%
      jsonlite::fromJSON(simplifyVector = FALSE)
    ggs <- ggs %>%
      leaflet.extras::addGeoJSONv2(geojson = arches.projects,
                                   labelProperty = "project",
                                   popupProperty = "description",
                                   weight = 1,
                                   color = projects.colors[i],
                                   opacity = 1,
                                   fillOpacity = 0)
  }
  ggs <- ggs %>%
    leaflet::addControl(map.title,
                        position = "topright")
  if(export.map){
    dir.create(file.path(dirOut))
    mapOut <- paste0(dirOut, fileOut)
    htmlwidgets::saveWidget(ggs, mapOut)
    if(verbose){
      print(paste0(fileOut, " has been saved into: ", dirOut))
    }
  } else {
    print(ggs)
  }
}

