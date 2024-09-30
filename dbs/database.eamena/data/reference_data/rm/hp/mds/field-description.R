library(readxl)
library(DT)
library(htmlwidgets)

## Generates a DT table of field names and field description from 'mds-template.xlsx'

# paths
root.path <- "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/"
mds.path <- paste0(root.path, "mds/")
tsv.path <- paste0(root.path, "values/")
# 
mds.template <- paste0(mds.path, "mds-template.xlsx")
df <- read_excel(mds.template, sheet = 1)

# TODO: add URL links to TSV files, ex: 
# https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/data/reference_data/rm/hp/values/Archaeological_Assessment/Absolute_Chronology.tsv
df$level1.url <- stringr::str_to_title(gsub(" ", "_", df$level1))
df$level3.url <- stringr::str_to_title(gsub("//", "_", gsub(" ", "_", df$level3)))
sort(df$level3.url)

description.field <- "description"
df_filtered <- df[, c("num", "level1", "level2", "level3", description.field, "color")]
colnames(df_filtered)[colnames(df_filtered) == 'level3'] <- 'Heritage Place field'
# rm the transparency from colors (ie, mds)
df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
# df_filtered$color <- as.factor(df_filtered$color)
dt_widget <- datatable(df_filtered[ , c("num", "Heritage Place field", description.field), drop=FALSE],
                       escape = FALSE,
                       rownames = FALSE,
                       options = list(pageLength = 25, autoWidth = TRUE)) %>%
  formatStyle(
    columns = c("Heritage Place field"),
    backgroundColor = styleEqual(df_filtered[["Heritage Place field"]], df_filtered$color)
  )
outFile <- paste0(mds.path, '/fields-description.html')
saveWidget(dt_widget, outFile, selfcontained = TRUE)

