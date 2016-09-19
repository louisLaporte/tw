#!/usr/bin/env python3

from tw import Tw
from plot import Plot
from pgsql import Pg

import string
from collections import Counter, OrderedDict

import sys, getopt
import json

with open("../../secret/database.json") as json_file:
    data = json.load(json_file)

DBNAME  = data["DBNAME"  ] 
USER    = data["USER"    ]
HOST    = data["HOST"    ]
PASSWORD= data["PASSWORD"]



companies = [ 
        "Total"       ,
        "Chevron"     ,
        "Shell"       ,
        "BP_America"  ,
        "exxonmobil"  ,
        "SinopecNews" ,
        "Saudi_Aramco"
        ]


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hn:",["name="])
    except getopt.GetoptError:
        print ('run.py -n twitterAccount')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -n twitterAccount')
            print('run.py --name=twitterAccount')
            sys.exit()
        elif opt in ("-n", "--name"):
            companies.append(str(arg))
    


    pg = Pg(dbname = DBNAME, user = USER, host = HOST, password = PASSWORD)
    tbname = "account"
    
    if pg.table_exist(name = tbname):
        print("Table {} exists ".format(tbname))
        #print("Removing table")
        #pg.remove_table(tbname)
    else:
        pg.create_table(name = tbname)
    

    q = ["stat"]
    l = []

    #pg.flush_table(name = tbname)
    for company in companies:
        c = Tw(name = company)
        ql = []
        if not pg.track_exists(name = tbname, entry = c.get_info_account(query = "user_id")):
            print("+ Creating new row for {}".format(company))
            for t in Tw.account_info:
                i = c.get_info_account(query = t)
                ql.append(i)

            ln = '%s' % ','.join(Tw.account_info)
            pg.add_entry(name = ln, val = tuple(ql))
        else:
            print("Row for: {} already exists".format(company))


    table = pg.get_table(name = tbname)
    #print(table)
    pg.close
    
    #for company in companies:
    #    cnt = Counter()
    #    c = Tw(name = company)
    #    d = c.get_info_tweet(count = 400, query = q)
    #    
    #    for e in d:
    #        cnt += e["stat"]
    #    cnt = sorted(cnt.items())
    #    
    #    l.append(cnt)

    #p = Plot(name = companies, stat = l)
    #p.draw()


if __name__ == '__main__':
    main(sys.argv[1:])

