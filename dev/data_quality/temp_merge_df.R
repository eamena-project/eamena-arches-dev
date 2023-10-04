meds <- read.csv2("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/bulk/templates/doc/bu_Minimum%20Enhanced%20Data%20Standards.tsv", sep = "\t")
meds[meds == ''] <- NA
meds <- meds[rowSums(is.na(meds)) == 0,]

uuids <- openxlsx::read.xlsx("C:/Rprojects/eamena-arches-dev/dev/data_quality/template.xlsx")
uuids$id <- 1:nrow(uuids)

all.uuids <- read.csv2("https://raw.githubusercontent.com/achp-project/cultural-heritage/main/data/rm/prj-eamena-marea-rm-nodes.tsv", sep = "\t")

setdiff(meds$Enhanced.record.minimum.standard, uuids$level3)

sapply(uuids, class)

all <- merge(uuids, meds, by.x = "level3", by.y = "Enhanced.record.minimum.standard", all.x = T)
all <- merge(all, all.uuids, by.x = "level3", by.y = "rm_node_name", all.x = T)
all <- all[order(all$id), ]

openxlsx::write.xlsx(all, "C:/Rprojects/eamena-arches-dev/dev/data_quality/template_complete.xlsx")
