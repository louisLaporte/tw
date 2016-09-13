#!/usr/bin/env python3
import urllib  # works fine with Python 2.7.9 (not 3.4.+)
from urllib import request  # works fine with Python 2.7.9 (not 3.4.+)
import json
import time
 
def fetchPreMarket(symbol, exchange):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s:%s" % (exchange, symbol)
    u = urllib.request.urlopen(url)
    content = str(u.read(), 'utf-8')
    #print(content)
    data = json.loads(content[3:])[0]
    data = dict(data)
    print ("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(data['t'],
     data['cp_fix'],
      data['c_fix'],
       data['lt'],
       data['cp'],
       data['c'],
       data['l']
    ))
    print(data)
    #print(data)
    #for key, value in data:
    #    print("{}{}".format(key, value))
    #info = data[0]
#    t = str(info["elt"])    # time stamp
    #l = float(info["l"])    # close price (previous trading day)
    #p = float(info["el"])   # stock price in pre-market (after-hours)
    #return (t,l,p)
    #return (l,p)
 
 
#p0 = 0
while True:
    fetchPreMarket("AAPL","NASDAQ")
    #if(p!=p0):
     #    p0 = p
#    #    #print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,
#    #    #                                         (p/l-1)*100.))
#    #    print("\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % ( l, p, p-l,
#    #                                             (p/l-1)*100.))
    time.sleep(2)
