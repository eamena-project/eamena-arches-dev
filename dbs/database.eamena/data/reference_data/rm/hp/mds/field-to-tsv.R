# Creates an HTML widget (datatable) from an XLSX listing the groups of fields (i.e. `level1` groups: Assessment Summary, Resource Summary, etc.) and export an HTML table with hyperlinks. 

fileIn <- "mds-template.xlsx"
fileOut <- "field-to-tsv-temp.html"

base_url <- "https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/data/reference_data/rm/hp/values/"
mds.path <- "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/data/reference_data/rm/hp/mds/"
mds.template <- paste0(mds.path, fileIn)
df <- openxlsx::read.xlsx(mds.template, sheet = 1)
df_filtered <- df[, c("level1", "color")]
df_filtered$color <- sub("^(.{7}).*", "\\1", df_filtered$color)
df_filtered <- df_filtered[!duplicated(df_filtered), ]
colnames(df_filtered)[colnames(df_filtered) == 'level1'] <- 'Groups'
df_filtered$Groups <- stringr::str_to_title(df_filtered$Groups)
# Apply the color and hyperlink together
df_filtered$Groups <- mapply(function(group, color) {
  sprintf("<a href='%s%s' target='_blank' style='font-size: 16px; font-family:arial; color:%s'>%s</a>", 
          base_url, gsub(" ", "_", group), color, stringr::str_to_upper(group))
}, df_filtered$Groups, df_filtered$color)
dt_widget <- DT::datatable(df_filtered[ , c("Groups"), drop=FALSE], 
                           escape = FALSE,
                           rownames = FALSE,
                           options = list(paging = FALSE, 
                                          searching = FALSE, 
                                          info = FALSE, 
                                          autoWidth = TRUE)) 
dt_widget #plot
htmlwidgets::saveWidget(dt_widget, paste0(mds.path, '/', fileOut), selfcontained = TRUE)

