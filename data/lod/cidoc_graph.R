library(visNetwork)
library(htmlwidgets)
library(dplyr)
library(openxlsx)


#' Read creates a graph from CIDOC-CRM case studies
#'
#' @name cidoc_graph
#'
#' @description Read creates a graph from CIDOC-CRM case studies.
#'
#' @param prj to subset the dataframe. Default "thera", other possible value: "palmyra".
#' @param local uses a local path instead of the GitHub dataset. Default: FALSE.
#' @param rootDir path to the main directory.
#' @param dataDir path to the data directory.
#' @param inFile the data file name.
#' @param export.plot if TRUE will export into outDir.
#' @param outFile the name of the output data in a TSV format. Default, the name of the project.
#' @outDir the path to the output directory. If NA (Default) export in the same directory as the R script
#' @verbose if TRUE, print messages
#'
#' @return an interactive plot
#'
#' @examples
#'
#' ## Plot the "thera" CIDOC graph
#' cidoc-graph()
#'
#' ## Plot the "thera" CIDOC graph and export data as TSV format
#' cidoc-graph(export.data = T, export.plot = T, outDir = "C:/Rprojects/histime-datasample/cidoc-crm/")
#'
#' @export
cidoc_graph <- function(prj = "thera",
                        local = F,
                        rootDir = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/",
                        dataDir = paste0(rootDir, "data/lod/"),
                        inFile = "data.xlsx",
                        export.plot = F,
                        export.data = F,
                        outDir = NA,
                        outFile = NA,
                        verbose = T){
  `%>%` <- dplyr::`%>%` # used to not load dplyr
  # paths
  if(local){rootDir <- paste0(getwd(), "/")} # local
  dataFile <- paste0(dataDir, inFile)
  # multimedia (images)
  if(prj == "palmyra"){
    imgDir <- paste0(rootDir, "www/")
    tit <- "A CIDOC-CRM example <br>for the destruction of Palmyra"
  }
  # prj thera is in historiacl-time GH
  if(prj == "thera"){
    imgDir <- paste0("https://raw.githubusercontent.com/historical-time/data-samples/main/", "cidoc-crm/")
    tit <- "A CIDOC-CRM example <br>for the dating of the Thera-Santorini eruption"
  }
  if(verbose){print(paste0("Read the XLSX file '",
                           inFile,"'"))}
  # read
  raw.nodes <- openxlsx::read.xlsx(dataFile, sheet = "nodes")
  raw.edges <- openxlsx::read.xlsx(dataFile, sheet = "edges")
  if(verbose){print(paste0("Filter on '",
                           prj,"'"))}
  # subset on project
  nodes <- raw.nodes[raw.nodes$prj == prj, ]
  edges <- raw.edges[raw.edges$prj == prj, ]
  nodes$prj <- edges$prj <- NULL
  if(verbose){print(paste0("    - nodes: '", nrow(nodes),"'"))}
  if(verbose){print(paste0("    - edges: '", nrow(edges),"'"))}

  # nodes with or without (by default) multimedia (eg. image)
  if(verbose){print(paste0("Prepare nodes"))}
  idx.images <- which(nodes$multimedia != "")
  nodes.shapes <- nodes$id %in% which(nodes$multimedia != "")
  nodes.shapes[nodes.shapes == TRUE] <- "image"
  nodes.shapes[nodes.shapes == FALSE] <- "box"
  nodes[idx.images, "multimedia"] <- paste0(imgDir, nodes[which(nodes$multimedia != ""), "multimedia"], ".png")

  nodes <- data.frame(id = nodes$id,
                      label = paste0(nodes$name,"\n", nodes$class),
                      color = c(rep("#000080", nrow(nodes))),
                      # title = "A simple CIDOC-CRM example",
                      # title.color = "white",
                      font.size = rep(18, nrow(nodes)),
                      font.color = c(rep("white", nrow(nodes))),
                      image = nodes$multimedia,
                      shape = nodes.shapes,
                      size = c(rep(24, nrow(nodes))),
                      group = c(rep("dmp", nrow(nodes)))
  )
  # enlarge images
  nodes <- nodes %>%
    mutate(size = ifelse(shape == "image", 36, 24))
  if(verbose){print(paste0("    - nodes preparation: done"))}

  if(verbose){print(paste0("Prepare edges"))}
  edges$length <- c(rep(400, nrow(edges)))
  edges$font.color <- c(rep("black", nrow(edges)))
  edges$font.size <- c(rep(20, nrow(edges)))
  edges$font.strokeWidth <- c(rep(0, nrow(edges)))
  edges$label <- gsub(" \\(", "\\\n\\(", edges$property)
  if(verbose){print(paste0("    - edges preparation: done"))}
  if(verbose){print(paste0("Creates CIDOC graph"))}
  gout <- visNetwork::visNetwork(nodes,
                                 edges,
                                 main = list(text = tit,
                                             style = "font-family:Arial;text-align:center;"
                                             # style = "text-align:right; font-family:Arial; color:#ffffff"
                                 ),
                                 # background = "black",
                                 width = "100%",
                                 height = "100vh") %>%
    visNetwork::visEdges(shadow = TRUE,
                         smooth = TRUE,
                         arrows =list(to = list(enabled = TRUE,
                                                scaleFactor = 1)),
                         color = list(color = "lightblue",
                                      highlight = "blue"))
  if(verbose){print(paste0("    - done"))}
  if(export.data){
    if(verbose){print(paste0("Export data as TSV"))}
    if(is.na(outFile)){
      outFile.nodes <- paste0(prj, "-cidoc-data-nodes.tsv")
      outFile.edges <- paste0(prj, "-cidoc-data-edges.tsv")
    }
    if(is.na(outDir)){
      outDir <- dirname(rstudioapi::getSourceEditorContext()$path)
    }
    exp.nodes <- raw.nodes[raw.nodes$prj == prj, ]
    exp.edges <- raw.edges[raw.edges$prj == prj, ]
    exp.nodes$prj <- exp.nodes$multimedia <- NULL
    exp.edges$prj <- NULL
    write.table(exp.nodes, sep = "\t", paste0(outDir, outFile.nodes), row.names = F)
    write.table(exp.edges, sep = "\t", paste0(outDir, outFile.edges), row.names = F)
    if(verbose){print(paste0("Data exported in folder'", outFile.nodes,"' and '", outFile.edges,"'"))}
    if(verbose){print(paste0("Data exported in folder'", outDir,"'"))}
  }

  if(export.plot){
    path.out <- paste0(outDir, prj, "-cidoc-graph.html")
    htmlwidgets::saveWidget(gout,path.out)
    if(verbose){print(paste0("HTML graph saved in: ", path.out))}
  } else {
    gout %>% visNetwork::visIgraphLayout(layout = 'layout.davidson.harel')
  }
}

cidoc_graph(export.data = T, export.plot = T, outDir = "C:/Rprojects/histime-datasample/cidoc-crm/")
