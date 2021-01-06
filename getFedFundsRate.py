import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
#import ssl
from collections import Counter, defaultdict
from operator import itemgetter
import json
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#import jinja2
#import pysentiment2
import time
from nltk.corpus import stopwords




urls = ['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2014.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2013.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2012.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2010.htm'
]

list_fomc_word_freq = []
statements_list_url = []
for url in urls:
    time.sleep(2)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

##links = soup.find_all("a") #find all links
    links = soup.select("a[href*=monetary]") #find minutes in href


#print(links)
    for link in links:
        if "a.htm" in link.get('href'):
            statements_list_url.append(link.get('href')) ##get all href that are htm page


#get each url link
rate_changes = dict()
rate_changes = pd.DataFrame(columns=['date','bound','rate'])


#### funktion
def convertRate(rate):
    try:
        i = 0
        if '/' in rate:
            if ' ' in rate:
                i, rate = rate.split(' ')
            if '-' in rate:
                i, rate = rate.split('-')
            if '‑' in rate: #even iof they look the same thats not the case in some minutes
                i, rate = rate.split('‑')
            N, D = rate.split('/')
            temp =  float(i) + float(N) / float(D)
            return temp
        else:
            temp =  float(i)+float(rate)
            return temp
    except:
        pass



#get each url link
for each in statements_list_url:
    time.sleep(3)
    url2 = 'https://www.federalreserve.gov' + each  #get url for each side

#    html = urllib.request.urlopen('https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130a.htm').read()
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, 'html.parser')

    text = soup.get_text() ##get all text


    ######CLEAN DATA
    #remove special characters, spaces, stop words and punctatuation

    text = text.strip()
    text = text.replace('\r', '') #replace r with minutes_list_url
    while '  ' in text:
        text = text.replace('  ', ' ') #replace extra spaces

        #Get minutes date as string
    minutes_x = re.findall('[0-9]+', url2)
    minutes_x = ''.join(minutes_x)

    sentences = sent_tokenize(text) #get all sentences



    list_decision = ["raise", "maintain", "lower"]
    rate_changes_temp = dict()



    #minutes_x = each
    match = 0
    for sen in sentences:

        if "federal funds rate" in sen and "target" in sen and "to" in sen and "percent" in sen:
#        if "federal funds rate" in sen and "target" in sen and "to" in sen and "percent" in sen and "decided" in sen or "decision" in sen and not "voting against" in sen:
            target = "percent"
            sen_words = word_tokenize(sen)
            for i,w in enumerate(sen_words):
                if w == target:
#                    if sen_words[i-2] == "to":
#                    if sen_words[i-5] == "funds" or sen_words[i-6] == "funds" or sen_words[i-7] == "funds" and sen_words[i-5] != "inflation" or sen_words[i-4] != "inflation" or sen_words[i-3] != "inflation":
                    if sen_words[i-7] != "inflation" or sen_words[i-6] != "inflation" or sen_words[i-5] != "inflation" or sen_words[i-4] != "inflation" or sen_words[i-3] != "inflation" or sen_words[i+3] != "inflation" or sen_words[i+2] != "inflation" or sen_words[i+1] != "inflation":

                        if i>0:

                            lower = sen_words[i-3]
                            upper = sen_words[i-1]
                            if "0" in lower or "/" in lower or "-" in lower or "‑" in lower or lower.isnumeric():
                                if "0" in upper or "/" in upper or "-" in upper or "‑" in upper or upper.isnumeric():

                                    if match == 0: ##only take the first correct match
                                #print(lower)
                                        temp = lower #ifall det blir false med konstiga tecken får vi ngt iaf
                                        temp = convertRate(lower)
                                        rate_changes_temp["lower_bound"] = temp

                                #print(upper)
                                        temp = upper #ifall det blir false med konstiga tecken får vi ngt iaf
                                        temp = convertRate(upper)
                                        rate_changes_temp["upper_bound"] = temp
                                        match = match + 1

    rate_changes_temp = pd.DataFrame(rate_changes_temp.items(), columns=['bound', "rate"])
    rate_changes_temp['date'] = minutes_x


    rate_changes = pd.concat([rate_changes, rate_changes_temp])

#print(rate_changes)
rate_changes.to_csv("data/fedFundsRate.csv", encoding='utf-8', index=False)
