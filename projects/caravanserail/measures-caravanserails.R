# regression on Area x nb of Stable & Area x nb of Room


d <- hash::hash()
my_con <- RPostgres::dbConnect(drv = RPostgres::Postgres(),
                               user = 'postgres',
                               password = 'postgis',
                               dbname = 'eamena',
                               host = 'ec2-54-155-109-226.eu-west-1.compute.amazonaws.com',
                               port = 5432)
# get ids
crvn.ids <- geojson_stat(stat.name = "geojson_fields", stat = "list_ids", export.stat = TRUE)

# get connected components
df <- list_related_resources(db.con = my_con,
                             d = d,
                             id = "EAMENA-0164943",
                             disconn = F)
df.measures <- select_related_resources(db.con = my_con,
                                        having ="Room",
                                        df = df,
                                        disconn = F)

# get HP ids and areas
geojson.path <- paste0(system.file(package = "eamenaR"),
                      "/extdata/caravanserail.geojson")
hp.geojson <- geojsonsf::geojson_sf(geojson.path)
hps <- as.data.frame(hp.geojson)

df.areas <- data.frame(hp.id = character(),
                       area = numeric())
for(crvn.id in crvn.ids$hp.id){
  exp <- hps[["EAMENA ID"]] ==  crvn.id & hps[["Dimension Type"]] == "Area"
  measure <- hps[exp, "Measurement Number"]
  df.areas <- rbind(df.areas, c(crvn.id, measure))
}


