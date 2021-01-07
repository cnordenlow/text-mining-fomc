
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
#from nltk.corpus import stopwords

##change the number of minutes to parse further down in the code
number= 100


urls = ['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
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

topics =    {'broad_topics' :
                {
                'Economy' : ["economy", "economic", "gdp"],
                'Labor' : ["labor", "employment", "unemployment", "payroll", "participation rate"],
                'Consumer' : ["consumer", "consumption", "household"],
                'Inflation' : ["inflation", "pce", "cpi", "core"],
                'Manufacturing' : ["manufacturing", "business", "production", "productivity","businesses","investment spending"],
                'Housing' : ["housing", "house", "home", "housing-sector", "residential"],
                'Commodities' : ["energy", "commodity", "commodities", "oil","gas", "gasoline"],
                'Trade' : ["export", "trade", "import"],
                'Demand' : ["demand"],
                'Foreign' : ["foreign", "international", "china", "europe", "india", "canada", "brexit", "emerging"]
                },

            'financial_conditions' :
                {
                'Money market' : ["money market"],
                'Financial markets' : ["financial market", "market for"],
                'Credit markets' : ["speculative grade", "investment grade", "credit spread", "credit market", "consumer loan", "bond issuance"],
                'Stocks' : ["equity", "equities", "stock"],
                'Yield curve' : ["yield curve", "steepened", "flattened","treasury curve"],
                'Financing conditions' : ["funding markets", "financing conditions", "financing for", "refinancing activity", "loan origination"],
                'US Dollar' : ["against the dollar", "dollar index", "exchange value of the dollar", "broad dollar", "dollar depreciating", "dollar apreciating"],
                'Volatility' : ["volatility", "vix", "volatile"]
                },


            'policy_topics' :
                {
                'Federal funds rate' : ["federal funds rate", "target range"],
                'Yield curve control' : ["yct", "YCT", "yield caps or target", "capped",  "yield curve control","yield caps", "target interest rate", "cap rate", "capping longer term interest", "cap shorter-term"],
                'Asset purchases' : ["asset purchase", "asset purchases", "asset holding", "holding of "],
                'Repo operations' : ['repurchase agreement', 'reverse repurchase', "rrps", "repo facility", "rrp","repo operation", "repurchase agreement operation", "overnight reverse repurchase"],
                'Forward guidance' : ['forward guidance', "expect"],
                #'Excess reserves' : ["excess reserve", "ioer"],
                'Negative interest rates' :  ["negative interest", "negative rates"],
                #'Swap agreements' : ["swap arrangement", "swap agreement"],
                'Liquidity facilities' : ["liquidity facility", 'liquidity swap', "liquidity and lending"]
                #'ample reserve' : ["ample reserve"]
                },

            'policy_words' :
                {
                'Patient' : ["patient"],
                'Gradual' : ["gradual", "gradually"],
                'Normalization' : ["normalization", "normalize", "normal stance"],
                'Data dependent' : ["data dependent", "data dependency", "realized and expected economic", "access incoming data", "incoming information"],
                'Accommodative' : ["accommodative", "accommodation", "accomodate"],
                'Outcome-based guidance' : ["outcome based"]
                #'Supportive' : ["supportive", "supporting"]

                },

            'quantitative_words' :
                {
                'Consensus' : ["unanimously", "majority", "most participant", "all participant", "participant supported", "all but one", "almost all", "member judged","participant all agreed", "participants generally"],
                'Few' : ["few participant", "one member", "a couple of participant", "one participant", "few other"]
                },

            'sentiment_words' :
                {
                'Strong' : ["stronger", "strong", "strongest", "strongly", "strength","strengthening", "strengthen", "strengthened"],
            #    'Covid' : ["covid", "virus", "coronavirus", "covid-19", "covid19","pandemic"],
                #'But' : ["but"],
                'Weak' : ["weak", "weakness", "weaker","weakening", "subdue", "subdued"],
                'Moderate' : ["moderate", "modestly", "moderately", "modest"],
                'Uncertainty' : ["uncertainty", "uncertain","risk", "riskier", "risky"],
                #'Weather' : ["weather", "storm", "hurricane"],
                "Recession" : ["recession"],
                'Recovery' : ["recovery", "recovered", "recovering", "rebound", "rebounded", "improve"],
                'Expand' : ["expand", "increase"],
                'Decline' : ["decline", "decrease", "deteriorate", "deterioration","plummeted"],
                'Stress' : ["stress", "turbulence"]

                }
            }

sentiment_words = {
                'negative' : ["weaker", "tension", "unfavorable", "weak", "slowdown", "difficult", "decreased", "subdued", "riskier", "stress", "meltdown", "sluggish", "shortage", "cautioned", "disturbance", "limitation", "vulnerability", "deviation", "deficit", "underutilization", "lackluster", "underperformed", "concern", "recession", "weakness", "volatility","adverse", "slack", "incomplete", "plummeted", "softness", "negative", "uncertainty", "moderate", "cut", "disrupted", "turbulence", "eased", "downward", "reduction", "weigh", "hardship", "negative", "disruption", "virus", "pressed", "risk", "lower", "shutdown", "badly", "severe", "permit", "hurt", "strain", "interruption", "decline", "uncertain", "closures","slowed","declined", "loss", "disruption", "concern", "stress", "crisis","severely", "downward","deteriorated", "deterioration","vulnerability", "downturn","loss","hardship","default","cease","challenging"],

                'positive' : ["picked up", "favorable", "deal", "stable", "above", "solid", "robust", "confidence", "rose", "expansion", "expand", "raise", "favored", "encouraging", "boost", "strengthen", "exceptional", "benefit","strong", "advantage","strengthening", "accomplish","progress" "sustained", "roughly balanced", "improved", "rebounded", "gain", "rapid", "rise", "positive", "tightening", "advanced", "above", "recovered", "expanded","smooth", "good","boosted","confident","achieving", "exceptionally","improvement","positive","greatly","strengthened","rebound","success","stability","effective","improve","improvement","confident","benefit","tremendous","better","progress","enhance","achieved"]
                    }

intensifiers = ["very", "terribly", "exceptionally", "extremely", "significant", "extreme", "significantly", "rapid", "rapidly", "sharp", "severely","substantial", "substantially", "terribly", "sharply"] ###ny


in_deep_topics = {
            'asset_program' : {
                'Size' : ["size"],
                'Composition' : ["composition"],
                'Pace' : ["pace"],
                'Keep same size' : ["rolling out at auction all principal", "roll over at auction all principal payments", "rolling over at auction all principal payment", "continue reinvesting all principal", "ending the reduction", "rolling over maturing treasury securities at auction", "existing policy of reinvesting principal payment"],
                'Increase size' : ["increase its holdings","expanding", "increase the system open market account holdings of treasury", "increase holdings of", "increasing"],
                'Reduce size' : ["decrease", "reduce", "reduction", "that exceed", "unwind", "withdrawal"],
                'Taper amounts' : ["taper", "tapering", "billion per month rather than", "reduce the pace of asset purchase", "net purchases cease"],
                'Guidance' : ["guidance"],
                'Longer maturity' : ["longer maturity", "lengthening the maturity"]

                },

            'inflation' : {
                'Symmetric' : ["symmetric"],
                'Compensation' : ["compensation"],
                'Core' : ["core"],
                'Term premium' : ["term premium"],
                'Wages' : ["wages", "wage"],
                'Energy' : ["energy"],
                'Long-term expectations' : ["long-term", "longer-term"],
                "Average inflation targeting" : ["average"]
                },

            'labor' : {
                'Slack ' : ["slack"],
                'Job gains' : ["job gain"],
                'Supply' : ["supply"],
                'Participation rate' : ["participation rate"],
                'Unemployment' : ["unemployment"],
                'Maximum employment' : ["maximum employment", "full employment"]

                }
}


#create empty dataframe
count = 0
count_outer = 0
count_inner = 0

minutes_all_tables = pd.DataFrame(columns=['date','category','additional','subject','frequency', 'frequency_share'])
temp_table = pd.DataFrame(columns=['date','category','additional','subject','frequency', 'frequency_share'])


##change the number of statements to parse further down in the code

#get each url link
for each in minutes_list_url[0:number]:
    time.sleep(random.uniform(3,7))

    url2 = 'https://www.federalreserve.gov' + each  #get url for each side
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, 'html.parser')

    text = soup.get_text() ##get all text


######CLEAN DATA
#remove special characters, spaces, lines and punctatuation

    text = text.strip()
    text = text.replace('\r', '') #replace r with minutes_list_url
    while '  ' in text:
        text = text.replace('  ', ' ') #replace extra spaces
    while '-' in text:
        text = text.replace('-', ' ') #replace line with space

    #Get minutes date as string
    minutes_x = re.findall('[0-9]+', url2)
    minutes_x = ''.join(minutes_x)


    temp_words = word_tokenize(text) #get words
    sentences = sent_tokenize(text) #get all sentences
    wordnet_lemmatizer = WordNetLemmatizer()

    words = []
    for w in temp_words:
        if w.isalpha(): #checks if string consists of alphabetical characters only
            words.append(w.lower())

    words = [wordnet_lemmatizer.lemmatize(w) for w in words]

    #do all words in sentence lower case?




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


####divide sentences into subsenteces. change each comma to dot.
#we like to find out if intensifiers are connected to pos or neg words
    sentences_no_comma = []
    temp_dict = dict()
    sentences_no_comma = [item.replace(",", ".', '") for item in sentences] #divide into sentences

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

###word count for fed mandate? employment, inflation, interest rate

minutes_all_tables.to_csv("data/fomcMinutesSummary.csv", encoding='utf-8', index=False)
