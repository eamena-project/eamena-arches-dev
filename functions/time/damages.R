library(openxlsx)
library(messydates)
library(lubridate)
library(tibble)
library(dplyr)
library(plotly)
library(htmlwidgets)


plot_ly <- T
export.to.ts <- F
filter.on.id <- T
id.filter <- c("AM009") # select these/this IDs

path_time <- paste0(getwd(), "/functions/time/")

# df <- read.xlsx(paste0(path_time, "data.xlsx"))
data_file <- "Disturbances_EDTF.xlsx"
date_field <- "EDTF"
site_field <- "S_ID"
cause_field <- "Disturbance.Cause" # R doesn't accept spaces in headers
type_field <- "Disturbance.Type"
# data_file <- "data.xlsx"
# date_field <- "date"
# site_field <- "site"
# cause_field <- "cause"
# type_field <- "type"

file_out <- "df_syria_out"

df_syria <- read.xlsx(paste0(path_time, data_file),
                      sheet = "Sheet1")
# export XLSX to TSV
if(export.to.tsv){
  write.table(df_syria,  paste0(path_time, file_out, ".tsv"),
              quote = FALSE, sep = "\t", col.names = TRUE)
}
if(filter.on.id){
  df_syria <- df_syria[df_syria$S_ID %in% id.filter, ]
  file_out <- paste0(file_out, "_", paste0(as.character(id.filter), collapse = "_"))
}


# reformat dataframe and dates
df_syria.out <- data.frame(#region = character(),
                           site = character(),
                           date = character(),
                           cause = character(),
                           type = character(),
                           density = integer())
for(i in seq_len(nrow(df_syria))){
  # intersect with the limits of the study: "2004-01-01..2019-12-31"
  # loop to read the date field
  if (i %% 50 == 0){print(paste0("   - ", i, "/", nrow(df_syria)))}
  var.date <- md_intersect(as_messydate("2004-01-01..2019-12-31"),
                           as_messydate(df_syria[i, date_field]))
  n.dates <- length(var.date)
  # var.region <- rep(df_syria[i, "region"], n.dates)
  var.site <- rep(df_syria[i, site_field], n.dates)
  var.cause <- rep(df_syria[i, cause_field], n.dates)
  var.type <- rep(df_syria[i, type_field], n.dates)
  df.damage <- data.frame(#region = var.region,
                          site = var.site,
                          date = var.date,
                          cause = var.cause,
                          type = var.type,
                          density = 1/n.dates)
  df_syria.out <- rbind(df_syria.out, df.damage)
}
# # export XLSX to TSV
# write.table(df_syria.out,  paste0(path_time, file_out, "_ext.tsv"),
#             quote = FALSE, sep='\t', col.names = TRUE)
# plot
df_syria.out$date <- as.Date(df_syria.out$date)
df_syria.out <- df_syria.out %>%
  group_by(date) %>%
  summarise(density = sum(density))
png(paste0(path_time, file_out, ".png"), width = 18, height = 12, res = 300, units = "cm")
plot(density ~ date, df_syria.out, xaxt = "n", type = "l")
axis(1, df_syria.out$date, format(df_syria.out$date, "%b %y"), cex.axis = .7)
dev.off()

if(plot_ly){
  # if TRUE, export as plot_ly widget
  p <- plot_ly(df_syria.out, type = 'scatter',
               x = ~date, y = ~round(density, 4),
               mode = 'line')
  p
  saveWidget(as_widget(p), paste0(getwd(),"/functions/time/results/", file_out, ".html"))
  # saveWidget(as_widget(p), paste0(getwd(),"/results/threats.html"))
}
#
# if(plot_ly){
#   # if TRUE, export as plot_ly widget
#   p <- plot_ly(df, type = 'scatter', x = ~date, y = ~hp, color = ~threat,
#                mode = 'line', stackgroup='one')
#   p
#   saveWidget(as_widget(p), paste0(getwd(),"/results/threats_stacked.html"))
#   #
# }
