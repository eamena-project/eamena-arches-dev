library(messydates)
library(lubridate)
library(tibble)
library(dplyr)
dates_comparison <- tibble::tribble(~Example, ~OriginalDate,
                                    "A normal date", "2010-01-01",
                                    "A historical date", "1291-08-01",
                                    "A very historical date", "476",
                                    "A really historical date", "33 BC",
                                    "A clearly future date", "9999-12-31",
                                    "A not so clearly future date", "2599-12-31",
                                    "A range of dates", "2019-11-01:2020-01-01",
                                    "An uncertain date", "2001-01-01?")
dates_comparison %>% dplyr::mutate(base = as.Date(OriginalDate),
                                   lubridate = suppressWarnings(lubridate::as_date(OriginalDate)),
                                   messydates = messydates::as_messydate(OriginalDate)) %>%
print()

dates_annotate <- tibble::tibble(Beg = as_messydate(c("1816-01-01", "1916-01-01", "2016-01-01")),
                                 End = as_messydate(c("1816-12-31", "1916-12-31", "2016-12-31")))
dplyr::mutate(dates_annotate, Beg = ifelse(Beg <= "1816-01-01", on_or_before(Beg), Beg))
dplyr::mutate(dates_annotate, End = ifelse(End >= "2016-01-01", on_or_after(End), End))
dplyr::mutate(dates_annotate, Beg = ifelse(Beg == "1916-01-01", as_approximate(Beg), Beg))
dplyr::mutate(dates_annotate, End = ifelse(End == "1916-12-31", as_uncertain(End), End))

data <- data.frame(Beg = c("1816-01-01", "1916-01-01", "2016-01-01"),
                   End = c("1816-12-31", "1916-12-31", "2016-12-31"))
dplyr::mutate(data, Beg = ifelse(Beg <= "1816-01-01",
                                 on_or_before(Beg), Beg))


dates_expand <- as_messydate(c("2008-03-25", "2001-01?", "2001",
                               "2001-01-01..2001-02-02", "{2001-01-01,2001-02-02}",
                               "2008-XX-31", "28 BC"))
expand(dates_expand)

x <- as_messydate("2013-04-01:2013-04-26")
xs <- expand(x)
as.Date("2013-04-01")

Lines <- "Date Visits
11/1/2010 696537
11/2/2010 718748
11/3/2010 799355
11/4/2010 805800
11/5/2010 701262
11/6/2010 531579
11/7/2010 690068
11/8/2010 756947
11/9/2010 718757
11/10/2010  701768
11/11/2010  820113
11/12/2010  645259"
dm <- read.table(text = Lines, header = TRUE)
dm$Date <- as.Date(dm$Date, "%m/%d/%Y")
plot(Visits ~ Date, dm, xaxt = "n", type = "l")
axis(1, dm$Date, format(dm$Date, "%b %d"), cex.axis = .7)

is_intersecting(as_messydate("2012-01"),
                as_messydate("2012-02-01..2012-02-22"))
is_intersecting(as_messydate("2012-01"),
                as_messydate("2012-01-01..2012-02-22"))
is_element(as_messydate("2012-01-01"), as_messydate("2012-01"))

md_intersect(as_messydate("2012-01-01..2012-01-20"),
             as_messydate("2012-01"))

md_intersect(as_messydate("2004-01-01..2019-12-31"),
             as_messydate(df.syria[i, "date"]))



