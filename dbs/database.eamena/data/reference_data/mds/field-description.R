library(readxl)
library(DT)
library(htmlwidgets)

## Generates a DT table of field names and field description from 'mds-template.xlsx'

mds.path <- "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/mds/"
mds.template <- paste0(mds.path, "mds-template.xlsx")
df <- read_excel(mds.template, sheet = 1)
df_filtered <- df[, c("level1", "level2", "level3", "description", "color")]
colnames(df_filtered)[colnames(df_filtered) == 'level3'] <- 'Heritage Place field'
# rm the transparency from colors (ie, mds)
df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
# df_filtered$color <- as.factor(df_filtered$color)
dt_widget <- datatable(df_filtered[ , c("Heritage Place field","description"), drop=FALSE],
                       rownames = FALSE,
                       options = list(pageLength = 25, autoWidth = TRUE)) %>%
  formatStyle(
    columns = c("Heritage Place field"),
    backgroundColor = styleEqual(df_filtered[["Heritage Place field"]], df_filtered$color)
  )
saveWidget(dt_widget, paste0(mds.path, '/fields-description.html'), selfcontained = TRUE)