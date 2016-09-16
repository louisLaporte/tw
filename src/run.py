#!/usr/bin/env python3

from tw import Tw
from plot import Plot

import string
from collections import Counter, OrderedDict

if __name__ == '__main__':

    companies = [ "Total", "Chevron", "Shell", "BP_America","exxonmobil" ]
    #companies = [ "Chevron","Shell" ]
    #companies = [ "Total" ]
    q = ["stat"]
    
    l = []


    
    for company in companies:
        cnt = Counter()
        c = Tw(name = company)
        d = c.get_info_tweet(count = 400, query = q)
        
        for e in d:
            cnt += e["stat"]
        cnt = sorted(cnt.items())
        
        l.append(cnt)
    #print(l[0])
    p = Plot(name = companies, stat = l)
    p.draw()
    #print(l[0])
        #print_result(d)

#
#        print("---------------")
