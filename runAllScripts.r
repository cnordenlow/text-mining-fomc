###############################################
##            FOMC Word Watching            ##
###############################################

###INFO: Due to lag in parsing, its take time to run it all for now.


#Setup
##Python package

#R packages
library("rstudioapi")   

library(reticulate) #for being able to run python


#install.packages("rstudioapi")
setwd(dirname(getActiveDocumentContext()$path))       # Set working directory to source file locatio


#Run Python Statements
#Run Python Minutes
#Run Markdown



###############################################
##            Run Python scripts             ##
###############################################

#Get statements
reticulate::source_python("getFedFundsRate.py")
reticulate::source_python("iterateMinutes.py")


#Get Minutes


###############################################
##            Run R scripts                  ##
###############################################

##Get last Minutes date
library(tidyverse)
df <- read.table(
  "data\\fomcMinutesSummary.csv",  
  sep=",", header=TRUE)


#Convert dates
df <- df %>%
  mutate(date = as.Date(gsub("\\D", "", date), format = "%Y%m%d"))

date_last_minutes = as.Date(max(df$date))

#Run markdown report
res <- rmarkdown::render("index.rmd", output_file = "index.html")
#save copy of report
file.copy(res,  sprintf("OldReports\\index_%s.html", date_last_minutes))

