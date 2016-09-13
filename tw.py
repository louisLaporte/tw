#!/usr/bin/env python3

#from __future__ import unicode_literals
import tweepy
import string
import yaml
import json
# -*- coding: latin-1 -*-

with open("../secret/key_secret.json") as json_file:
    data = json.load(json_file)

access_token_key    = data["ACCESS_TOKEN_KEY"   ] 
access_token_secret = data["ACCESS_TOKEN_SECRET"]
consumer_key        = data["CONSUMER_KEY"       ]
consumer_secret     = data["CONSUMER_SECRET"    ]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
 
api = tweepy.API(auth)
 
#api.update_status(status='This is a tweet sent automatically by a Python script!')



def unique_words(sentence):
    return set(sentence.translate(None, punctuation).lower().split())

def getUniqueWords(allWords) :
    uniqueWords = [] 
    for i in allWords.split():
        if not i in uniqueWords:
            uniqueWords.append(i)
    return uniqueWords


class Punctuation:
    #def __init__(self, sentence):
    #    self.s = str(sentence)

    def rm_all_punct(self, sentence):
        translator = str.maketrans({key: None for key in (string.punctuation)})
        s = sentence.translate(translator)
        return s
    #
    #def rm_punct(sentence):
    #    pass

      


from string import punctuation
import time
import re
from collections import Counter

class ParseContent:

    def __init__(self,name,count = 1):
        
        self.c = count
        self.u = api.get_user(screen_name=name)
        
        self.d = {}
        self.d["name"] = self.u.name
        self.d["user_id"] = self.u.id_str
        self.d["description"] = self.u.description
        self.d["lang"] = self.u.lang
        self.d["account_created_at"] = self.u.created_at
        self.d["location"] = self.u.location
        self.d["time_zone"] = self.u.time_zone
        self.d["number_tweets"] = self.u.statuses_count
        self.d["number_followers"] = self.u.followers_count
        self.d["following"] = self.u.friends_count
        self.d["member_of"] = self.u.listed_count
        self.d["location"] = self.u.location
        self.d["tweet"] = {}
        
        
    def info(self):
        print(self.d["name"])
        print("Location: "  +            self.d["location"]      )
        print("Time zone: " +            self.d["time_zone"]     )  
        print("Number of tweets: " + str(self.d["member_tweets"]))

    def extract(self, sentence):
        """
        extracting list of hashtag, at and url
        """
        h_list, a_list, u_list = [], [], []
         
        for s in list(sentence):
            if re.match('#.*', s):
                h_list.append(s)
            elif re.match('@.*', s):
                a_list.append(s)
            elif re.match('http.*', s):
                u_list.append(s)
        
        return (h_list, a_list, u_list)

    def normalize(self, sentence):
        #TODO use beautifulsoup to convert html special char
        #http://stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
        """
        - remove url and @
        - remove punctuation
        """
        for s in list(sentence):
            if re.match('@.*',s):
                sentence.remove(s)
            elif  re.match('http.*',s):
                sentence.remove(s)
            elif re.match('&.*', s):
                #print("+++++++++++" + s)
                #print(self.d["tweet"]["content"]["text"])
                sentence.remove(s)
            elif  s == 'cc':
                #print("+++++++++++" + s)
                #print(self.d["tweet"]["content"]["text"])
                sentence.remove(s)

        sentence_norm = [''.join(c for c in s if c not in string.punctuation) for s in sentence]
        #remove blank in array
        sentence_norm = [s for s in sentence_norm if s]
        return sentence_norm

    def run(self):
        statuses = api.user_timeline(id = self.u.id, count = self.c)
        status_list = []
        
        counts = Counter()
        for status in statuses:
            self.d["tweet"]["id"] = status.id_str
            self.d["tweet"]["retweet_count"] = status.retweet_count
            self.d["tweet"]["favorite_count"] = status.favorite_count
            self.d["tweet"]["created_at"] = status.created_at
            self.d["tweet"]["place"] = status.place
            self.d["tweet"]["source"] = status.source
            self.d["tweet"]["coordinates"] = status.coordinates
            self.d["tweet"]["content"] = {}
            self.d["tweet"]["content"]["text"] = status.text

            #print(status.created_at)
            #print(status.text)

            tw = status.text 
            tw_list = str(status.text).split()  
            self.extract(tw)
            (self.d["tweet"]["content"]["hashtag"],
            self.d["tweet"]["content"]["at"], 
            self.d["tweet"]["content"]["url"]) = self.extract(tw_list)

            #print(self.d["tweet"]["content"]["hashtag"])
            #print(self.d["tweet"]["content"]["at"])
            #print(self.d["tweet"]["content"]["url"] )

            tw_norm = self.normalize(tw_list)
            tw_norm_tolower = [x.lower() for x in tw_norm]
            #print(tw_norm_tolower)

            for words in tw_norm_tolower:
                  for letters in set(words):
                      counts[letters]+=1

        import operator                             #Importing operator module

        counts = sorted(counts.items(),key = operator.itemgetter(1),reverse = True)
        tot = 0
        for key,value in counts:
            if not re.match('\W+',key):
                tot += value 

        for key,value in counts:
            if not re.match('\W+',key):
                print("{:<10}{:.2f}%".format(key,100*value/tot))

if __name__ == '__main__':

    #companies = [ "Total", "Chevron", "Shell", "BP_America","exxonmobil" ]
    companies = [ "Total" ]
    nb_last_tw = 30
    for company in companies:
        print(company)
        a = ParseContent(name = company,count = nb_last_tw) 
        a.run()
        print("---------------")
