# install.packages("readxl")
# install.packages("DT")
library(readxl)
library(DT)
library(htmlwidgets)


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
saveWidget(dt_widget, paste0(mds.path, '/fields_description.html'), selfcontained = TRUE)


# 
# datatable(df_filtered, options = list(pageLength = 25, autoWidth = TRUE)) %>%
#   formatStyle("level1", backgroundColor = styleEqual(df_filtered$level1, df_filtered$color.1)) %>%
#   # formatStyle("level2", backgroundColor = styleInterval(df_filtered$level2, df_filtered$color)) %>%
#   formatStyle("level3", backgroundColor = styleEqual(df_filtered$level3, df_filtered$color))

# Ts[, "col1", drop=FALSE]

# data2 <- cbind(ID = "some ID",iris[,1:4])
# datatable(
#   data2, rownames = FALSE, class = 'cell-border stripe',
#   options = list(
#     dom = 't', pageLength = -1, lengthMenu = list(c(-1), c('All'))
#   )
# ) %>%
#   formatStyle(colnames(data2)[2:ncol(data2)], 
#               backgroundColor = styleEqual(help_3, hepl_1))

# datatable(
#   data2, rownames = FALSE, class = 'cell-border stripe',
#   options = list(
#     dom = 't', pageLength = -1, lengthMenu = list(c(-1), c('All')),
#     rowCallback=JS(paste0("function(row, data) {\n",
#                           paste(sapply(2:ncol(data2),function(i) paste0("var value=data[",i-1,"]; if (value!==null) $(this.api().cell(row,",i-1,").node()).css({'background-color':value <=", mean(data2[[i]])," ? 'red' : 'green'});\n")
#                           ),collapse = "\n"),"}" ))
#   )
# ) 

#############


# Create the DT object
dt_widget <- datatable(df_filtered) %>%
  formatStyle('level1', 'level2', 'level3',
              backgroundColor = JS(
                "function(value, row, data, type){",
                "return data.color;",
                "}")
  )

# Save the DT object as an HTML file
saveWidget(dt_widget, 'datatable.html', selfcontained = TRUE)





