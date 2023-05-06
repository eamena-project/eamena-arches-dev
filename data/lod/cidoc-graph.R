library(visNetwork)
library(htmlwidgets)
library(dplyr)
library(openxlsx)

# local or GH
local <- F

# to subset the dataframe
prj <- "palmyra"
prj <- "thera"

# paths
rootDir <- "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/"
if(local){rootDir <- paste0(getwd(), "/")} # local
dataDir <- paste0(rootDir, "data/lod/")
dataFile <- paste0(dataDir, "data.xlsx")
# multimedia (images)
if(prj == "palmyra"){imgDir <- paste0(rootDir, "www/")}
# prj thera is in historiacl-time GH
if(prj == "thera"){imgDir <- paste0("https://raw.githubusercontent.com/historical-time/data-samples/main/", "cidoc-crm/")}

# read
nodes <- read.xlsx(dataFile, sheet = "nodes")
edges <- read.xlsx(dataFile, sheet = "edges")

# subset on project
nodes <- nodes[nodes$prj == prj, ]
edges <- edges[edges$prj == prj, ]
nodes$prj <- edges$prj <- NULL

# nodes with or without (by default) multimedia (eg. image)
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
