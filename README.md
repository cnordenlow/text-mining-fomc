## Text Mining FOMC

What did Fed say? With the help of text mining, this project aims to gain insights and colour from FOMC Minutes and to make plots out of words.

### Methodology

The approach of this project are as follows.

* Words and topics are divided into bag of words of its meaning (e.g. the word "strong" may consists of ["strong", "stronger", "strongest", "strengthen"]). All bag of words dictionaries are located in the iterateMinutes.py.

* All web parsing is done using BeautifulSoup package. The code first parse all .htm pages with the url of "Minutes" in it for the years of interest. Then, a second loop parse all the (chosen) Minutes for the text mining. In both parsing steps, there are a time delay of a couple of seconds.

* Text are divided into sentences as well as words. For some parts we use the full sentences, and for some cleaned sentences and words are used. NLTK package is used.

* All sentences are iterated where it checks for the different bag of words and then counted, (e.g. if the word "stronger" is found in a sentence, the count adds one regardless of how many time strong is in the sentence.) For most topics, a second loop followed which counts negative and positive words in the same sentence to get the net sentiment for each topic. 

* R is used for some further calculations and Markdown for creating a report.

*To be able to to compare Minutes by different length with each other, everything is set in relation to total the number of words or paragraph in their respective Minutes.*

*The purpose with the bag of words format is to being able to get part  of sentences grouped for their meaning. E.g. for being able to find more colour on asset purchases (tapering amounts, reducing the program, increasing the program), it may not be sufficient to map a sentence with the word of "increase" and "asset purchase" in the same, but there a for some subjects meaningful to have longer parts of a meaning.*


### Technologies

For this project, both Python and R are used. Please see a short description for each script.

* **getFedFundsRate.py** are parsing all chosen statements to get the Fed Funds rate for each meeting. It´s saved as an csv named fedFundsRate in subfolder Data.
* **iterateMinutes.py** is the main loop for parsing and text mining all chosen Minutes. Each minutes are iterated in a for loop that extract word data. Everything is then joined in a table that is saved as a .csv saved in subfolder Data. The purpose of saving these files are to be able to put down more time on the plotting between meetings without needing to parse all Minutes each time.

* **r_plots.r** is a script with a couple of plots that are reused multiple times in the Markdown report.
* **index.rmd** is doing some additional data wrangling and are sen producing the report. Gglots are used.
* **runAllScripts.r** can run all scripts together using Reticulate-package in R for running Python.


### Setup

To run this project, cloone it and install it locally. It´s takes aprox 20 minutes to run due to sleep-function of 3 to 7 seconds between each parsed Statement and Minutes.

In the beginning of both Python scripts there it is a possibility to write in the number of statements and minutes to parse. I would recommend to change it to 5 when trying.

#### Packages needed
**Python**

import urllib.request, urllib.parse, urllib.error <br>
from bs4 import BeautifulSoup <br>
import nltk <br>
from nltk.stem import WordNetLemmatizer <br>
from nltk.tokenize.treebank import TreebankWordDetokenizer <br>
import re <br>
import pandas as pd <br>
import time <br>
import random <br>


**R**

install.packages("rmarkdown") <br>
library(tidyverse) <br>
library(slider) <br>
library(lubridate) <br>
library(ggrepel) <br>
library(rstudioapi)    <br>
library(reticulate) <br>
