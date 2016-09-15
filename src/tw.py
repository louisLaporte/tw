#!/usr/bin/env python3

#from __future__ import unicode_literals
import tweepy
import json
import string
from string import punctuation
from collections import Counter

import time
import operator
import re
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


class Tw(object):
    """
    This class provides info for a twitter account. 
    Furthermore it provides tweet statistics.

    Example for an account:

    >>>t = Tw(name="twitter")
    >>>t.get_info_account(query = ["name","description"])

    Example for tweets:
    >>>t = Tw(name="twitter")
    >>>t.get_info_tweet(query=["stat","hashtag"], count = 10)

    """

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

    def __init__(self,name):
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

    def get_info_account(self, query = None):
        """ Return account info
        
        Keyword arguments:
           query -- info to retrieve
        """
        if query in Tw.account_info:
            return self.d[query]
        else:
            print("Cannot print info: query = " + query)
            print("list of queries:")
            for i in Tw.account_info:
                print("\t- " + i)
            return None

    def get_info_tweet(self, count = 1, query = None):
        """ Return info from tweet
        
        Keyword arguments:
           count -- number of last tweet to retrieve
           query -- info to retrieve
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
                for key, value in self.d["tweet"].items():
                    if q in key:
                        d[q] = value
                #val  = [value for key, value in self.d["tweet"].items() if q in key ]
            l.append(d)
        return l

    def statistic(self,text):
        """ Return a Counter for ascii lowercase and digitis
        
        Keyword arguments:
           text -- tweet string
        """
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
        return counts
                
    def search(self):
        for tweet in tweepy.Cursor(api.search,
                               q="#IS",
                               count=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
            print(tweet.text)

    def meta(self, text):
        """
        extracting list of hashtag, at and url
        """
        h_list, a_list, u_list = [], [], []
         
        for s in list(text):
            if re.match('#.*', s):
                h_list.append(s)
            elif re.match('@.*', s):
                a_list.append(s)
            elif re.match('http.*', s):
                u_list.append(s)
        return (h_list, a_list, u_list)

def print_result(result):
    
    r = result
    i = string.ascii_lowercase + string.digits
    cnt = Counter()
    
    for l in r:
        cnt += l["stat"]
    print(cnt)
            
    for k,v in cnt.items():
        if k in i:
            print("{}: {}".format(k,v))
        else:
            print("{}: {}".format(k,0))
#    for i in index:
#        for l in r:
#            for k,v in l["stat"].items():
#                if k is i:
#                    print("{}: {}".format(i,v))

if __name__ == '__main__':

    #companies = [ "Total", "Chevron", "Shell", "BP_America","exxonmobil" ]
    companies = [ "Total" ]
    nb_last_tw = 30
    q = ["created_at","stat"]

    for company in companies:
        c = Tw(name=company)
        #c.print_info_account(query="description")
        d = c.get_info_tweet(count = 2, query = q)
        print_result(d)

#
#        print("---------------")
