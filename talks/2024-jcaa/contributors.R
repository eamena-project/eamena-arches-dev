# TODO:
# this functions should go in eamenaR
# Join these SQL staement in one query

`%>%` <- dplyr::`%>%` # used to not load dplyr
d <- hash::hash()
source("C:/Rprojects/eamena-arches-dev/credentials/pg_credentials.R") # the Pg connection (hidden pwd)

# return the UUID of the Actors
nbmax <- 100 # 500
sqll <- stringr::str_interp("
SELECT
tiledata -> '34cfea8a-c2c0-11ea-9026-02e7594ce0a0' -> 0 ->> 'resourceId' AS AssInvestUUID,
count(*) as nb
FROM
tiles
WHERE
nodegroupid::text LIKE '34cfea2e-c2c0-11ea-9026-02e7594ce0a0' -- the node 'Assessment Investigator'
GROUP BY
tiledata -> '34cfea8a-c2c0-11ea-9026-02e7594ce0a0' -> 0 ->> 'resourceId'
ORDER BY nb DESC
LIMIT '${nbmax}';
")

d['AssInvestUUID'] <- DBI::dbGetQuery(db.con, sqll)
d$AssInvestUUID$assinvestname <- NA
verbose = T
# find the human-readable name and add it in the df
for(i in 1:nrow(d$AssInvestUUID)){
  if(verbose & (i %% 10 == 0)){
    print(paste0("Read ", i))
    print(paste0("   name: ", assinvestname))
  }
  AssInvestUUID <- d$AssInvestUUID[i, "assinvestuuid"]
  nb <- d$AssInvestUUID[i, "nb"]
  sqll <- stringr::str_interp("
  SELECT tiledata -> 'e98e1cfe-c38b-11ea-9026-02e7594ce0a0' -> 'en' ->> 'value' as AssInvestName
  FROM tiles
  WHERE resourceinstanceid::text LIKE '%${AssInvestUUID}%'
  AND tiledata -> 'e98e1cfe-c38b-11ea-9026-02e7594ce0a0' -> 'en' ->> 'value' IS NOT NULL
  ")
  assinvestname <- DBI::dbGetQuery(db.con, sqll)
  if(nrow(assinvestname) > 0){
    d$AssInvestUUID[i, "assinvestname"] <- assinvestname
  }
}
df <- d$AssInvestUUID[!is.na(d$AssInvestUUID$assinvestuuid), ] # rm NA
df <- df[!duplicated(df$assinvestname), ] # rm possible duplicates (TODO: add a suffix instead of rm)
df$assinvestname <- factor(df$assinvestname, levels = df$assinvestname, ordered = T)

# this part directly comes from  geojson_stats.R
blank_theme <- ggplot2::theme_minimal()+
  ggplot2::theme(
    axis.title.x = ggplot2::element_blank(),
    axis.title.y = ggplot2::element_blank(),
    panel.border = ggplot2::element_blank(),
    panel.grid = ggplot2::element_blank(),
    axis.ticks = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(size=14, face="bold")
  )
gg <- ggplot2::ggplot(df, ggplot2::aes(x = assinvestname, y = nb)) +
  ggplot2::geom_bar(stat = "identity", fill = "lightblue") +
  blank_theme +
  ggplot2::geom_text(ggplot2::aes(label = nb), vjust = -0.5, color = "black") + # Adding text above bars
  ggplot2::labs(title = paste0("Names of the ", nbmax, " highest contributors in the EAMENA DB"),
                # subtitle = my_subtitle,
                caption = paste0("Data source: \n",
                                 "on the number of occurences in the fieldname 'Appellation', ",
                                 "nodeid = e98e1cfe-c38b-11ea-9026-02e7594ce0a0")) +
  # ggplot2::ylab(paste0(field.name, " %")) +
  ggplot2::ylab(paste0("nb of contributions")) +
  ggplot2::scale_x_discrete(labels = function(x) stringr::str_wrap(x, width = 20)) +
  ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, vjust = 1, hjust = 1),
                 axis.title.y = ggplot2::element_text(angle = 90))
gg
# #   ggplot2::theme(plot.margin = ggplot2::margin(0, 0, 1, 1, "cm"))
# # axis.title.y = ggplot2::element_blank()
ggplot2::ggsave(
  file = "C:/Rprojects/eamena-arches-dev/talks/2024-jcaa/contrib_100.jpg",
  plot = gg,
  height = 21, width = 29
)

