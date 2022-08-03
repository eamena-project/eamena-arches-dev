library(visNetwork)
library(htmlwidgets)

dmg.steps <- c("collect",
               "description",
               "storage",
               "curation",
               "archiving",
               "publishing")
# dmg.steps.url <- c("#wp3.step.collec",
#                    "#wp3.step.describ",
#                    "#wp3.bdweb",
#                    "#wp3.step.anal",
#                    "#wp3.step.archiv",
#                    "#wp3.step.public")
# dmg.steps.tit <- paste0("<a href='",dmg.steps.url,"'>",dmg.steps,"</a>")
dmg.steps.url <- c("<em>'publish once and reuse often'</em>",
                   "assign & register data",
                   "short- to middle term storing",
                   "process",
                   "long-term preservation",
                   "sharing")
dmg.steps.tit <- paste0("<b>", dmg.steps,"</b><br>",dmg.steps.url)
# dmg.steps.tit <- paste0(dmg.steps)
dmp.logo.root <- "https://raw.githubusercontent.com/zoometh/thomashuet/main/img/"
name.im <- c(paste0(dmp.logo.root, "lod-data-create.png"),
             paste0(dmp.logo.root, "lod-data-tag.png"),
             paste0(dmp.logo.root, "lod-data-store.png"),
             paste0(dmp.logo.root, "lod-data-process.png"),
             paste0(dmp.logo.root, "lod-data-archive.png"),
             paste0(dmp.logo.root, "lod-data-publish.png"))
n.dmg.steps <- length(dmg.steps)
nodes <- data.frame(id=dmg.steps,
                    label = dmg.steps,
                    # label = paste0("[",dmg.steps,"](",dmg.steps.url,")"),
                    color = c(rep("#808080", n.dmg.steps)),
                    title = dmg.steps.tit,
                    font.size = rep(15, n.dmg.steps),
                    font.color = c(rep("white", n.dmg.steps)),
                    image = name.im,
                    shape = c(rep("image", n.dmg.steps)),
                    size = c(rep(24, n.dmg.steps)),
                    group = c(rep("dmp", n.dmg.steps))
)
a <- data.frame(from = dmg.steps[1:length(dmg.steps)-1],
                to = dmg.steps[2:length(dmg.steps)])
b <- data.frame(from = dmg.steps[length(dmg.steps)],
                to = dmg.steps[1])
edges <- rbind(a,b)
gout <- visNetwork(nodes,
                   edges,
                   background = "black",
                   width = "700px",
                   height = "700px") %>%
  visEdges(shadow = TRUE,
           smooth = TRUE,
           arrows =list(to = list(enabled = TRUE,
                                  scaleFactor = 1)),
           color = list(color = "lightblue", highlight = "red"))

path.out <- paste0(getwd(),"/data/dmp.html")
saveWidget(gout,path.out)
print(paste("saved in:", path.out))
