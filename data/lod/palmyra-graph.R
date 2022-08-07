library(visNetwork)
library(htmlwidgets)

dataDir <- "https://raw.githubusercontent.com/eamena-oxford/eamena-arches-dev/main/data/lod/"
imgDir <- "https://raw.githubusercontent.com/zoometh/thomashuet/main/img/"

vertices <- read.csv2(paste0(dataDir, "palmyra-vertices.tsv"), sep = "\t")
edges <- read.csv2(paste0(dataDir, "palmyra-edges.tsv"), sep = "\t")

# vertices$multimedia <- vertices[vertices$multimedia == '', "multimedia"] <- paste0(dataDir, vertices$multimedia)

idx.images <- which(vertices$multimedia != "")
shapes <- vertices$id %in% idx.images
shapes[shapes == TRUE] <- "image"
shapes[shapes == FALSE] <- "box"

vertices[idx.images, "multimedia"] <- paste0(imgDir, vertices[which(vertices$multimedia != ""), "multimedia"], ".png")

nodes <- data.frame(id = vertices$id,
                    label = paste0(vertices$name,"\n", vertices$class),
                    color = c(rep("#808080", nrow(vertices))),
                    title = "A simple CIDOC-CRM example",
                    title.color = "white",
                    font.size = rep(15, nrow(vertices)),
                    font.color = c(rep("white", nrow(vertices))),
                    image = vertices$multimedia,
                    shape = shapes,
                    size = c(rep(24, nrow(vertices))),
                    group = c(rep("dmp", nrow(vertices)))
)

edges$font.color <- c(rep("white", nrow(edges)))
edges$font.strokeWidth <- c(rep(0, nrow(edges)))
edges$label <- gsub(" \\(", "\\\n\\(", edges$property)
visNetwork(nodes,
           edges,
           main = list(text = "A simple CIDOC-CRM example",
                       style = "color:#ffffff"),
           background = "black",
           width = "100%",
           height = "100vh") %>%
  visEdges(shadow = TRUE,
           smooth = TRUE,
           arrows =list(to = list(enabled = TRUE,
                                  scaleFactor = 1)),
           color = list(color = "lightblue",
                        highlight = "red"))


# dmp.logo.root <- "https://raw.githubusercontent.com/zoometh/thomashuet/main/img/"
# name.im <- c(paste0(dmp.logo.root, "lod-data-create.png"),
#              paste0(dmp.logo.root, "lod-data-tag.png"),
#              paste0(dmp.logo.root, "lod-data-store.png"),
#              paste0(dmp.logo.root, "lod-data-process.png"),
#              paste0(dmp.logo.root, "lod-data-archive.png"),
#              paste0(dmp.logo.root, "lod-data-publish.png"))
