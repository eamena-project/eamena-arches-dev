library(openxlsx)
library(dplyr)

tables.path <- paste0(dirname(rstudioapi::getActiveDocumentContext()$path), "/db_data/tables")
tables <- list.files(path = tables.path)

ltables <- list()
for(i in tables){
  a.table <- paste0(tables.path, "/", i)
  ltables <- append(ltables, a.table)
}

ltables

# read tables
condition <- read.xlsx(ltables[[1]])
dating <- read.xlsx(ltables[[2]])
features <- read.xlsx(ltables[[3]])
featuresnumbers <- read.xlsx(ltables[[4]])
photos <- read.xlsx(ltables[[5]])
records <- read.xlsx(ltables[[6]])
# records1 <- read.xlsx(ltables[[7]])
smallpics <- read.xlsx(ltables[[8]])

### Reference data
write.table(condition, 
            "C:/Rprojects/eamena-arches-dev/projects/cairo/reference_data/condition.csv", 
            sep = ",", row.names = F)


## HP
records <- merge(records, photos, by = "ID", all.x = T)
df <- records
df <- merge(df, condition, by = "conditionID", all.x = T)
df <- df %>%
  select(where(function(x) any(!is.na(x))))
df <- merge(df, smallpics, by.x = "ID", by.y = "UnitNumber", all.x = T)
df <- df %>%
  select(where(function(x) any(!is.na(x))))
df <- merge(df, dating, by.x = "datetypenumber", by.y = "TypeNumber", all.x = T)
df <- df %>%
  select(where(function(x) any(!is.na(x))))


df[nrow(df) + 1,] <- NA
write.table(df, 
            "C:/Rprojects/eamena-arches-dev/projects/cairo/business_data/hp.csv",
            sep = ",", row.names = F)

# View(df)
# colnames(df)

# BC
# Features as Built Components
df <- features
# df <- merge(df, features, by = "ID", all.x = T)
# df <- df %>%
#   select(where(function(x) any(!is.na(x))))
df <- merge(df, featuresnumbers, by.x = "featureID1", by.y = "featureID", all.x = T)
df <- df %>%
  select(where(function(x) any(!is.na(x))))

df[nrow(df)+1,] <- NA
write.table(df, "C:/Rprojects/eamena-arches-dev/projects/cairo/business_data/bc.csv",
            sep = ",", row.names = F)

# View(df)
# colnames(df)

