library(DT)
library(readxl)
library(stringr)

## Link level 1 (groups), color groups, add hyperlinks to TSVs
# ex: https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bulk/templates/doc/bu_Condition%20Assessment.tsv

base_url <- "https://github.com/eamena-project/eamena-arches-dev/blob/main/data/bulk/templates/doc/bu_"

mds.path <- "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/mds/"
mds.template <- paste0(mds.path, "mds-template.xlsx")
df <- read_excel(mds.template, sheet = 1)
df_filtered <- df[, c("level1", "color")]
df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
# df_filtered$color <- paste0(df_filtered$color, "95")
df_filtered <- df_filtered[!duplicated(df_filtered), ]
colnames(df_filtered)[colnames(df_filtered) == 'level1'] <- 'Groups'
df_filtered$Groups <- stringr::str_to_title(df_filtered$Groups)

# Apply the color and hyperlink together
df_filtered$Groups <- mapply(function(group, color) {
  # sprintf("<a href='%s%s.tsv' target='_blank' style='background-color:%s; padding: 5px; font-size: 20px;'>%s</a>", 
  #         base_url, gsub(" ", "%20", group), color, group)
  sprintf("<a href='%s%s.tsv' target='_blank' style='font-size: 20px; font-family:arial; color:%s'>%s</a>", 
          base_url, gsub(" ", "%20", group), color, group)
}, df_filtered$Groups, df_filtered$color)

dt_widget <- datatable(df_filtered[ , c("Groups"), drop=FALSE], escape = FALSE,
                       rownames = FALSE,
                       options = list(paging = FALSE, searching = FALSE, info = FALSE, autoWidth = TRUE)) 
# dt_widget
saveWidget(dt_widget, paste0(mds.path, '/field-to-tsv.html'), selfcontained = TRUE)

