library(visNetwork)
library(htmlwidgets)
library(dplyr)

rootDir <- "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/"
dataDir <- paste0(rootDir, "data/lod/")
imgDir <- paste0(rootDir, "www/")

vertices <- read.csv2(paste0(dataDir, "palmyra-vertices-1.tsv"), sep = "\t")
edges <- read.csv2(paste0(dataDir, "palmyra-edges-1.tsv"), sep = "\t")

idx.images <- which(vertices$multimedia != "")

vertices.shapes <- vertices$id %in% which(vertices$multimedia != "")
vertices.shapes[vertices.shapes == TRUE] <- "image"
vertices.shapes[vertices.shapes == FALSE] <- "box"

vertices[idx.images, "multimedia"] <- paste0(imgDir, vertices[which(vertices$multimedia != ""), "multimedia"], ".png")

nodes <- data.frame(id = vertices$id,
                    label = paste0(vertices$name,"\n", vertices$class),
                    color = c(rep("#000080", nrow(vertices))),
                    # title = "A simple CIDOC-CRM example",
                    # title.color = "white",
                    font.size = rep(18, nrow(vertices)),
                    font.color = c(rep("white", nrow(vertices))),
                    image = vertices$multimedia,
                    shape = vertices.shapes,
                    size = c(rep(24, nrow(vertices))),
                    group = c(rep("dmp", nrow(vertices)))
)
# enlarge images
nodes <- nodes %>%
  mutate(size = ifelse(shape == "image", 36, 24))

edges$length <- c(rep(400, nrow(edges)))
edges$font.color <- c(rep("black", nrow(edges)))
edges$font.size <- c(rep(20, nrow(edges)))
edges$font.strokeWidth <- c(rep(0, nrow(edges)))
edges$label <- gsub(" \\(", "\\\n\\(", edges$property)
gout <- visNetwork(nodes,
                   edges,
                   main = list(text = "a CIDOC-CRM example",
                               style = "font-family:Arial;text-align:center;"
                               # style = "text-align:right; font-family:Arial; color:#ffffff"
                               ),
                   # background = "black",
                   width = "100%",
                   height = "100vh") %>%
  visEdges(shadow = TRUE,
           smooth = TRUE,
           arrows =list(to = list(enabled = TRUE,
                                  scaleFactor = 1)),
           color = list(color = "lightblue",
                        highlight = "blue"))
gout %>% visIgraphLayout(layout = 'layout.davidson.harel')

path.out <- paste0(getwd(),"/data/lod/palmyra-cidoc-graph.html")
# saveWidget(gout,path.out)
print(paste("saved in:", path.out))
