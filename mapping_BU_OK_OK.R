#' Fill an empty BU template with data from an unformatted XLSX
#' @name list_mapping_bu
#' @description Use a mapping file to recast the values of a source file into a format adapted to the bulk upload process (BU)

#' @param bu.path the path to the BU folder. The BU folder (`bu/`) is the root of different subfolder: the folder where are the different jobs containing the unformatted XLSX datasets (ex: 'mk/'). The output subfolder `out/` will be created by the function to store the output files.
#' @param bu.template.path the path to the BU template
#' @param mapping.file the path to the XLSX or Google Sheet file providing the equivalences (mapping) between the source file (unformatted) and the target file (formatted as a BU).
#' @param mapping.file.ggsheet is the mapping file a Google Sheet (for example: 'https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625'), by default: FALSE.
#' @param job the subfolder of `bu/` where are the unformatted XLSX datasets. `job` is also the name of the source fields in the mapping file. By default 'mk'.
#' @param job.type the name of the field in the `mapping.file` XLSX giving the name of the mapping function to do:
#'   - 'field': one-to-one correspondences, the source values will be copied as it into the target file;
#'   - 'value': constant values (ie, always the same value) that will be copied into the target file;
#'   - 'expression': logical functions (mainly if statements). These functions are written directly in the appropriate cell of the mapping file;
#'   - 'escape': values depending from another column evaluated by 'expression'. This field is
#'       not read;
#' @param eamena.field the name of the field in the `mapping.file` XLSX with the name of the EAMENA fields in a R format ('UNIQUEID', 'Assessment.Investigator.-.Actor', 'Investigator.Role.Type', etc.)
#' @param eamena.id the unique key identifier for a single resource, by default 'UNIQUEID'
#' @param verb if TRUE (by default): verbose
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
#'
#' @export
list_mapping_bu <- function(bu.path = paste0(system.file(package = "eamenaR"), "/extdata/bu/"),
                            bu.template.path = "C:/Rprojects/eamena-arches-dev/data/bulk/templates/Heritage Place BUS Template.xlsx",
                            mapping.file = paste0(system.file(package = "eamenaR"), "/extdata/mapping_bu.xlsx"),
                            mapping.file.ggsheet = F,
                            job = "mk",
                            job.type = "mk_type",
                            eamena.field = "EAMENA",
                            eamena.id = "UNIQUEID",
                            verb = T){

  dirOut <- paste0(bu.path, job, "/out/")
  dir.create(dirOut, showWarnings = FALSE)

  # data source
  data.path.folder <- paste0(bu.path, job, "/")
  l.bus <- setdiff(list.files(data.path.folder),
                   list.dirs(data.path.folder,
                             recursive = FALSE, full.names = FALSE))

  # mapping file
  if(mapping.file.ggsheet){
    mapping.file <- googlesheets4::read_sheet(mapping.file)
  } else {
    mapping.file <-  openxlsx::read.xlsx(mapping.file)
  }
  cpt <- 0
  for(bu.name in l.bus){
    cpt <- cpt + 1
    if(verb){print(paste0(cpt, "- read: ", bu.name))}
    data.path <- paste0(bu.path, job, "/", bu.name)
    data <- xlsx::read.xlsx(data.path,
                            sheetIndex = 1)
    data <- data[rowSums(is.na(data)) != ncol(data),]
    if(verb){print(paste0(" - nb of rows: ", nrow(data)))}
    data[is.na(data)] <- "" # rm NA value for logical tests
    # BU template for BU structure only
    bu <- openxlsx::read.xlsx(bu.template.path, startRow = 3)
    bu <- bu[0, ]
    for(i in seq(1, nrow(data))){
      bu[nrow(bu) + 1, ] <- NA
    }
#
#     # BU structure only
#     mapping.file.header <- na.omit(mapping.file[ , eamena.field])
#     bu <- data.frame(matrix(ncol = length(mapping.file.header),
#                             nrow = 0))
#     colnames(bu) <- mapping.file.header
#     for(i in seq(1, nrow(data))){
#       bu[nrow(bu) + 1, ] <- NA
#     }

    # - - - - - - - - - - - - - -
    # loops

    # 'field'
    if(verb){print(paste0("     works on 'field' field type"))}
    mapping.file.fields <- mapping.file[mapping.file[ , job.type] == "field", ]
    for(i in seq(1, nrow(mapping.file.fields))){
      ea <- as.character(mapping.file.fields[i, eamena.field])
      if(verb){print(paste0("           ... and read '", ea,"'"))}
      x <- as.character(mapping.file.fields[i, job])
      bu[ , ea] <- data[ , x]
    }

    # 'value'
    if(verb){print(paste0("     works on 'value' field type"))}
    mapping.file.value <- mapping.file[mapping.file[ , job.type] == "value", ]
    for(i in seq(1, nrow(mapping.file.value))){
      ea <- as.character(mapping.file.value[i, eamena.field])
      if(verb){print(paste0("           ... and read '", ea,"'"))}
      x <- as.character(mapping.file.value[i, job])
      bu[ , ea] <- x
    }

    # 'expression'
    if(verb){print(paste0("     works on 'expression' field type"))}
    mapping.file.expres <- mapping.file[mapping.file[ , job.type] == "expression", ]
    for(i in seq(1, nrow(mapping.file.expres))){
      ea <- as.character(mapping.file.expres[i, eamena.field])
      if(verb){print(paste0("           ... and read '", ea,"'"))}
      x.text <- as.character(mapping.file.expres[i, job])
      x.text <- gsub("[\r\n]", "\n", x.text)
      eval(parse(text = x.text)) # the XLSX cell text is executed
    }

    # 'value'
    if(verb){print(paste0("     works on 'value' field type"))}
    mapping.file.value <- mapping.file[mapping.file[ , job.type] == "value", ]
    for(i in seq(1, nrow(mapping.file.value))){
      ea <- as.character(mapping.file.value[i, eamena.field])
      if(verb){print(paste0("           ... and read '", ea,"'"))}
      x <- as.character(mapping.file.value[i, job])
      bu[ , ea] <- x
    }

    # 'other' column
    if(verb){print(paste0("     works on 'other' field values"))}
    mapping.file.other <- mapping.file[mapping.file[ , job.type] == "other", ]
    for(i in seq(1, nrow(mapping.file.other))){
      x.text <- as.character(mapping.file.other[i, job])
      x.text <- gsub("[\r\n]", "\n", x.text)
      eval(parse(text = x.text)) # the XLSX cell text is executed
    }

    # delete surnumerary rows
    bu <- bu[!is.na(bu[ , eamena.id]), ]
    bu <- bu[order(bu[ , eamena.id]),]
    row.names(bu) <- seq(1, nrow(bu))

    out.bu <- paste0(dirOut, bu.name)
    out.bu.xlsx <- paste0(out.bu, "_out.xlsx")
    openxlsx::write.xlsx(bu, out.bu.xlsx, row.names = F, showNA = FALSE)
    if(verb){print(paste0(" - '", bu.name, "' done: ", out.bu.xlsx))
      print("")
    }
  }
}

library(dplyr)

list_mapping_bu(bu.path = "C:/Rprojects/eamena-arches-dev/data/bulk/bu/",
                job = "mk",
                verb = T,
                mapping.file = 'https://docs.google.com/spreadsheets/d/1nXgz98mGOySgc0Q2zIeT1RvHGNl4WRq1Fp9m5qB8g8k/edit#gid=1083097625',
                mapping.file.ggsheet = T)
