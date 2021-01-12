
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
from nltk.tokenize.treebank import TreebankWordDetokenizer
import random
wordnet_lemmatizer = WordNetLemmatizer()
#from nltk.corpus import stopwords

###Import topic definitions
from fomcTopicDefinitions import intensifiers, sentiment_words,in_deep_topics, topics

###

########################################################################################################
####  Clean data function. Return words, sentences and adjusted sentences with break for each comma. ###
####  Remove special characters, spaces, lines and punctatuation.                                    ###
########################################################################################################
def cleanData(text):
    text = text.strip()
    text = text.replace('\r', '') #replace r with minutes_list_url
    while '  ' in text:
        text = text.replace('  ', ' ') #replace extra spaces
    while '-' in text:
        text = text.replace('-', ' ') #replace line with space

    temp_words = word_tokenize(text) #get words
    sentences = sent_tokenize(text) #get all sentences

    ####Divide sentences into subsenteces. change each comma to dot. Then detokenize it back to smaller sentences.
    #This is for checking for intensifier words that usually are in sen same sub-sentence
    sentences_no_comma = []
    sentences_no_comma = [item.replace(",", ".', '") for item in sentences] #divide into sub-sentences


    words = []
    for w in temp_words:
        if w.isalpha(): #checks if string consists of alphabetical characters only
            words.append(w.lower())

    words = [wordnet_lemmatizer.lemmatize(w) for w in words]
    return words, sentences, sentences_no_comma




##change the number of minutes to parse further down in the code
number= 100


urls = ['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2015.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2014.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2013.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2012.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm',
        'https://www.federalreserve.gov/monetarypolicy/fomchistorical2010.htm'

]

#url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
list_fomc_word_freq = []
minutes_list_url = []
for url in urls:
    time.sleep(random.uniform(3,7))
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select("a[href*=minutes]") #find minutes in href

    for link in links:
        if ".htm" in link.get('href'):
            minutes_list_url.append(link.get('href')) ##get all href that are htm page



###For topics: then the text is cleaned.
###For in deep topics: full sentences
##########################################################################################
### Classifications of topics, negative & positive words, intentifiers etc.            ###
##########################################################################################



#create empty dataframe
count = 0
count_outer = 0
count_inner = 0

minutes_all_tables = pd.DataFrame(columns=['date','category','additional','subject','frequency', 'frequency_share'])
temp_table = pd.DataFrame(columns=['date','category','additional','subject','frequency', 'frequency_share'])


#get each url link
for each in minutes_list_url[0:number]:
    time.sleep(random.uniform(3,7))

    url2 = 'https://www.federalreserve.gov' + each  #get url for each side
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, 'html.parser')

    text = soup.get_text() ##get all text

    #Get minutes date as string
    minutes_x = re.findall('[0-9]+', url2)
    minutes_x = ''.join(minutes_x)

######CLEAN DATA
#remove special characters, spaces, lines and punctatuation
    words, sentences, sentences_no_comma = cleanData(text)

    ####
    ##Get descriptive information
    ####
    temp_dict = dict()
    temp_dict['number_words'] = len(words)
    temp_dict['number_sentences'] = len(sentences)
    temp_dict['word_per_sentences'] = len(words) / len(sentences)

    #print(minutes_general)
    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "general_information" # gör en lång dplyrtabell för output till R
    temp_dict['additional'] = "N/A"
    temp_dict['frequency_share'] = 0


    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])

###
###Count neg and pos words
###
    count = 0
    temp_dict = dict()
    for w in words:
        for key, value in sentiment_words.items():
            if w in value:
                temp_dict[key] = temp_dict.get(key, 0) + 1
                if key == "positive":
                    temp_dict['net_sentiment'] = temp_dict.get('net_sentiment', 0) + 1
                if key == "negative":
                    temp_dict['net_sentiment'] = temp_dict.get('net_sentiment', 0) - 1

    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "sentiment" # gör en lång dplyrtabell för output till R
    temp_dict['additional'] = "N/A"
    temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100


    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])


####divide sentences into subsenteces. change each comma to dot. Then detokenize it back to smaller sentences.
#we like to find out if intensifiers are connected to pos or neg words
    sentences_no_comma = []
    sentences_no_comma = [item.replace(",", ".', '") for item in sentences] #divide into sentences
    temp_dict = dict()

    #print(sentences_no_comma)
    for sen in sentences_no_comma:
        word = word_tokenize(sen)
        word = [wordnet_lemmatizer.lemmatize(w) for w in word]
        sen = TreebankWordDetokenizer().detokenize(word) ## put words back in sentence


        if any(item in sen for item in intensifiers):
    #if word in intensifiers:
            temp_dict["intensifiers"] = temp_dict.get("intensifiers", 0) + 1 ##check if word is in intensifiers
            if any(item in sen for item in sentiment_words['negative']):
                temp_dict["intensifiers_neg"] = temp_dict.get("intensifiers_neg", 0) + 1
                temp_dict["intensifiers_net"] = temp_dict.get("intensifiers_net", 0) - 1
            if any(item in sen for item in sentiment_words['positive']):
                temp_dict["intensifiers_pos"] = temp_dict.get("intensifiers_pos", 0) + 1
                temp_dict["intensifiers_net"] = temp_dict.get("intensifiers_net", 0) + 1

#    print(temp_dict)
    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "intensifiers" # gör en lång dplyrtabell för output till R
    temp_dict['additional'] = "count_words"
    temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100
    #print(temp_dict)
    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])





    #Count paragraphs that include topics, and how many of those paragraph that contains positive vs negative words.


    for i in topics: #run each dictionary
        temp_dict = dict() #create empty temporary dictionary
        temp_dict_neg = dict()
        temp_dict_pos = dict()
        temp_dict_sentiment = dict()
        category = i #subject is the dictionary name
        for sen in sentences: #for each sentence in text
            list_sentence = word_tokenize(sen)
            list_sentence = [wordnet_lemmatizer.lemmatize(w) for w in list_sentence]

            sen = word_tokenize(sen)
            sen = [wordnet_lemmatizer.lemmatize(w) for w in sen]
            sen = TreebankWordDetokenizer().detokenize(sen)


            for key, value in topics[i].items():
                for v in value:
                    if v in sen:
                        temp_dict[key] = temp_dict.get(key, 0) + 1 #count. one count per paragraph that includes one or more of the words
                    #    temp_dict[key] = temp_dict.get(key, 0) + 1
                        if any(item in list_sentence for item in sentiment_words['negative']): #här fångas väl alla negativa ord
                            temp_dict_neg[key] = temp_dict_neg.get(key, 0) + 1
                            temp_dict_sentiment[key] = temp_dict_sentiment.get(key, 0) - 1
                        if any(item in list_sentence for item in sentiment_words['positive']):
                            temp_dict_pos[key] = temp_dict_pos.get(key, 0) + 1
                            temp_dict_sentiment[key] = temp_dict_sentiment.get(key, 0) + 1
                    else:
#                        temp_dict[key] = temp_dict.get(key, 0) + 0
                        temp_dict[key] = temp_dict.get(key, 0) + 0 ###To get the word in the dataframe. Its an answer that it wasent included.
                        temp_dict_pos[key] = temp_dict_pos.get(key, 0) + 0
                        temp_dict_neg[key] = temp_dict_neg.get(key, 0) + 0
                        temp_dict_sentiment[key] = temp_dict_sentiment.get(key, 0) + 0




        temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
        temp_dict['date'] = minutes_x
        temp_dict['category'] = category
        temp_dict['additional'] = "count_words"
        temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100

        temp_dict_neg = pd.DataFrame(temp_dict_neg.items(), columns=['subject', "frequency"])
        temp_dict_neg['date'] = minutes_x
        temp_dict_neg['category'] = category
        temp_dict_neg['additional'] = "count_negative_words_in_paragraph"
        temp_dict_neg['frequency_share'] = (temp_dict_neg['frequency'] / len(sentences))*100

        temp_dict_pos = pd.DataFrame(temp_dict_pos.items(), columns=['subject', "frequency"])
        temp_dict_pos['date'] = minutes_x
        temp_dict_pos['category'] = category
        temp_dict_pos['additional'] = "count_positive_words_in_paragraph"
        temp_dict_pos['frequency_share'] = (temp_dict_pos['frequency'] / len(sentences))*100

        temp_dict_sentiment = pd.DataFrame(temp_dict_sentiment.items(), columns=['subject', "frequency"])
        temp_dict_sentiment['date'] = minutes_x
        temp_dict_sentiment['category'] = category
        temp_dict_sentiment['additional'] = "net_sentiment_per_topic"
        temp_dict_sentiment['frequency_share'] = (temp_dict_sentiment['frequency'] / len(sentences))*100


        temp_table = pd.concat([temp_table, temp_dict,temp_dict_neg, temp_dict_pos,temp_dict_sentiment])


###dig deeper topics.

    #print(asset_program)
    temp_dict = dict()
    for sen in sentences:
        if "asset purchase" in sen or "asset purchases" in sen or  "asset program" in sen or "holdings of" in sen or "securities holdings" in sen:
            #for key, value in asset_program.items(): #for each key and value in sub dictionaries
            for key, value in in_deep_topics['asset_program'].items(): #for each key and value in sub dictionaries
#            for key, value in asset_program.items(): #for each key and value in sub dictionaries
                if any(item in sen for item in value):
                    temp_dict[key] = temp_dict.get(key, 0) + 1
                #print(sen)
                else:
                   temp_dict[key] = temp_dict.get(key, 0) + 0 ###To get the word in the dataframe. Its an answer that it wasent included.

    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "in_deep_asset_program"
    temp_dict['additional'] = "count_words"
    temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100
    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])

    temp_dict = dict()
    for sen in sentences:
        if "inflation" in sen or "cpi" in sen or "pce" in sen:
            #for key, value in asset_program.items(): #for each key and value in sub dictionaries
            for key, value in in_deep_topics['inflation'].items(): #for each key and value in sub dictionaries
#           for key, value in inflation.items(): #for each key and value in sub dictionaries
                if any(item in sen for item in value):
                    temp_dict[key] = temp_dict.get(key, 0) + 1
                #print(sen)
                else:
                   temp_dict[key] = temp_dict.get(key, 0) + 0 ###To get the word in the dataframe. Its an answer that it wasent included.



    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "in_deep_inflation"
    temp_dict['additional'] = "count_words"
    temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100
    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])

    #Labor

    temp_dict = dict()
    for sen in sentences:
        if "labor" in sen or "employment" in sen or "unemployment" in sen:
            #for key, value in asset_program.items(): #for each key and value in sub dictionaries
            for key, value in in_deep_topics['labor'].items(): #for each key and value in sub dictionaries
#           for key, value in inflation.items(): #for each key and value in sub dictionaries
                if any(item in sen for item in value):
                    temp_dict[key] = temp_dict.get(key, 0) + 1
                #print(sen)
                else:
                   temp_dict[key] = temp_dict.get(key, 0) + 0 ###To get the word in the dataframe. Its an answer that it wasent included.



    temp_dict = pd.DataFrame(temp_dict.items(), columns=['subject', "frequency"])
    temp_dict['date'] = minutes_x
    temp_dict['category'] = "in_deep_labor"
    temp_dict['additional'] = "count_words"
    temp_dict['frequency_share'] = (temp_dict['frequency'] / len(sentences))*100
    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])



    ###Join with other
minutes_all_tables = pd.concat([minutes_all_tables, temp_table])


#print(minutes_all_tables)

#
minutes_all_tables.to_csv("data/fomcMinutesSummary.csv", encoding='utf-8', index=False)
