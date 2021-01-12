import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import time
from nltk.corpus import stopwords
import random

##change the number of statements to parse
number = 100

#######################################################################################
### Get links for statements (get links for Minutes works the same.)                ###
#######################################################################################
urls = ['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2015.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2014.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2013.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2012.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2010.htm'
]

list_fomc_word_freq = []
statements_list_url = []
for url in urls:
    time.sleep(random.uniform(3,7))
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

##links = soup.find_all("a") #find all links
    links = soup.select("a[href*=monetary]") #find minutes in href


#print(links)
    for link in links:
        if "a.htm" in link.get('href'):
            statements_list_url.append(link.get('href')) ##get all href that are htm page


rate_changes = dict()
rate_changes = pd.DataFrame(columns=['date','bound','rate'])


#### function
def convertRate(rate):
    try:
        i = 0
        if '/' in rate:
            if ' ' in rate:
                i, rate = rate.split(' ')
            if '-' in rate:
                i, rate = rate.split('-')
            if '‑' in rate: #even if they look the same thats not the case in some minutes
                i, rate = rate.split('‑')
            N, D = rate.split('/')
            temp =  float(i) + float(N) / float(D)
            return temp
        else:
            temp =  float(i)+float(rate)
            return temp
    except:
        pass

#####################################################################################################
### Main loop that iterates all  statements. The loop for iterating Minutes works in the same way ###
#####################################################################################################

#get each url link
for each in statements_list_url[0:number]:
    time.sleep(random.uniform(3,7))
    url2 = 'https://www.federalreserve.gov' + each  #get url for each side
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text() ##get all text

    ######CLEAN DATA
    #remove special characters, spaces and punctatuation

    text = text.strip()
    text = text.replace('\r', '') #replace r with minutes_list_url
    while '  ' in text:
        text = text.replace('  ', ' ') #replace extra spaces

        #Get minutes date as string
    minutes_x = re.findall('[0-9]+', url2)
    minutes_x = ''.join(minutes_x)

    sentences = sent_tokenize(text) #get all sentences

    rate_changes_temp = dict()

    match = 0
    for sen in sentences:

        if "federal funds rate" in sen and "target" in sen and "to" in sen and "percent" in sen:
#        if "federal funds rate" in sen and "target" in sen and "to" in sen and "percent" in sen and "decided" in sen or "decision" in sen and not "voting against" in sen:
            target = "percent"
            sen_words = word_tokenize(sen)
            for i,w in enumerate(sen_words):
                if w == target:
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
