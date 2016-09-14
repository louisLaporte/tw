#!/usr/bin/env python3

#from __future__ import unicode_literals
import tweepy
import string
import yaml
import json
# -*- coding: latin-1 -*-

with open("../../secret/key_secret.json") as json_file:
    data = json.load(json_file)

access_token_key    = data["ACCESS_TOKEN_KEY"   ] 
access_token_secret = data["ACCESS_TOKEN_SECRET"]
consumer_key        = data["CONSUMER_KEY"       ]
consumer_secret     = data["CONSUMER_SECRET"    ]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
 
api = tweepy.API(auth)

from string import punctuation
import time
import operator                             #Importing operator module
import re
from collections import Counter

class Tw(object):

    account_info = [
            "name"            ,
            "user_id"         ,
            "description"     ,
            "lang"            ,
            "created_at"      ,
            "location"        ,
            "time_zone"       ,
            "number_tweets"   ,
            "number_followers",
            "following"       ,
            "member_of"
            ]

    tweet_info = [
            "id_str",
            "retweet_count",
            "favorite_count",
            "created_at",
            "place",
            "source",
            "coordinates"
            ]

    def __init__(self,name,count = 1):
        self.u = api.get_user(screen_name=name)
        self.d = {}
        self.d["name"]              = self.u.name
        self.d["user_id"]           = self.u.id
        self.d["description"]       = self.u.description
        self.d["lang"]              = self.u.lang
        self.d["created_at"]        = self.u.created_at
        self.d["location"]          = self.u.location
        self.d["time_zone"]         = self.u.time_zone
        self.d["number_tweets"]     = self.u.statuses_count
        self.d["number_followers"]  = self.u.followers_count
        self.d["following"]         = self.u.friends_count
        self.d["member_of"]         = self.u.listed_count

        self.d["tweet"] = {}

    
    def print_info_account(self,query=None):
        """
        info for twitter account
        """
        if query is None or not isinstance(query, str):
            for a in Tw.account_info:
                print("{:<20}: {}".format(a,self.d[a]))
        elif query in Tw.account_info:
            print("{:<20}: {}".format(query,self.d[query]))
        else:
            print("Cannot print info: query = " + query)
            print("list of queries:")
            for a in Tw.account_info:
                print("\t- " + a)


    def get_info_account(self, query = None):
        """
        info for twitter account
        """
        if query in Tw.account_info:
            return self.d[query]
        else:
            print("Cannot print info: query = " + query)
            print("list of queries:")
            for i in Tw.account_info:
                print("\t- " + i)


    def get_info_tweet(self, count = 1, query = None):
        """
        private 
        """
        l = []
        for status in  tweepy.Cursor( api.user_timeline, id=self.u.id ).items(count):
        
            d = {}
            self.d["tweet"]["id"]               = status.id_str
            self.d["tweet"]["retweet_count"]    = status.retweet_count
            self.d["tweet"]["favorite_count"]   = status.favorite_count
            self.d["tweet"]["created_at"]       = status.created_at
            self.d["tweet"]["place"]            = status.place
            self.d["tweet"]["source"]           = status.source
            self.d["tweet"]["coordinates"]      = status.coordinates

            self.d["tweet"]["text"] = status.text
            (self.d["tweet"]["hashtag"],
            self.d["tweet"]["at"],
            self.d["tweet"]["url"]) = self.meta(status.text)
            self.d["tweet"]["stat"] = self.statistic(status.text)

            for q in query:
                val  = [value for key, value in self.d["tweet"].items() if q in key ]
                d[q] = val
            l.append(d)
        return l

    def statistic(self,text):
        text = text.split()
        for s in list(text):
            if re.match('@.*',s):
                text.remove(s)
            elif  re.match('http.*',s):
                text.remove(s)
            elif re.match('&.*', s):
                text.remove(s)
            elif  s == 'cc':
                text.remove(s)

        text_norm = [''.join(c for c in s if c not in string.punctuation) for s in text]
        #remove blank in array
        text_norm = [s for s in text_norm if s]
        text_norm = [x.lower() for x in text_norm]

        counts = Counter()

        for words in text_norm:
            for letters in set(words):
                if not re.match("\W+",letters):
                    counts[letters]+=1

        counts = sorted(counts.items(),key = operator.itemgetter(1),reverse = True)
        return counts
                
    def search(self):
        for tweet in tweepy.Cursor(api.search,
                               q="#IS",
                               count=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
            print(tweet.text)


#
    def meta(self, sentence):
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


if __name__ == '__main__':

    companies = [ "Total", "Chevron", "Shell", "BP_America","exxonmobil" ]
   # companies = [ "Total" ]
    nb_last_tw = 30
    for company in companies:
        c = Tw(name=company)
        #c.print_info_account(query="description")
        d = c.get_info_tweet(count = 2, query=["created_at","stat"])
        print(d)

        print("---------------")
