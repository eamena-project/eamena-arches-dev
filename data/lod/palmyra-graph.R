library(visNetwork)
library(htmlwidgets)

dataDir <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/lod/"
imgDir <- "https://raw.githubusercontent.com/zoometh/thomashuet/main/img/"

vertices <- read.csv2(paste0(dataDir, "palmyra-vertices.tsv"), sep = "\t")
edges <- read.csv2(paste0(dataDir, "palmyra-edges.tsv"), sep = "\t")

# idx.images <- which(vertices$multimedia != "")
vertices.shapes <- vertices$id %in% which(vertices$multimedia != "")
vertices.shapes[vertices.shapes == TRUE] <- "image"
vertices.shapes[vertices.shapes == FALSE] <- "box"

vertices[idx.images, "multimedia"] <- paste0(imgDir, vertices[which(vertices$multimedia != ""), "multimedia"], ".png")

nodes <- data.frame(id = vertices$id,
                    label = paste0(vertices$name,"\n", vertices$class),
                    color = c(rep("#808080", nrow(vertices))),
                    # title = "A simple CIDOC-CRM example",
                    # title.color = "white",
                    font.size = rep(15, nrow(vertices)),
                    font.color = c(rep("white", nrow(vertices))),
                    image = vertices$multimedia,
                    shape = vertices.shapes,
                    size = c(rep(24, nrow(vertices))),
                    group = c(rep("dmp", nrow(vertices)))
)

edges$length <- c(rep(300, nrow(edges)))
edges$font.color <- c(rep("white", nrow(edges)))
edges$font.strokeWidth <- c(rep(0, nrow(edges)))
edges$label <- gsub(" \\(", "\\\n\\(", edges$property)
gout <- visNetwork(nodes,
                   edges,
                   main = list(text = "A simple CIDOC-CRM example",
                               style = "text-align:right; font-family:Arial; color:#ffffff"),
                   background = "black",
                   width = "100%",
                   height = "100vh") %>%
  visEdges(shadow = TRUE,
           smooth = TRUE,
           arrows =list(to = list(enabled = TRUE,
                                  scaleFactor = 1)),
           color = list(color = "lightblue",
                        highlight = "red"))
gout

path.out <- paste0(getwd(),"/data/lod/palmyra-cidoc-graph.html")
saveWidget(gout,path.out)
print(paste("saved in:", path.out))
