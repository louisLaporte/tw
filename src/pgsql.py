#!/usr/bin/env python3
import psycopg2

con = None

class Pg():
    def __init__(self,dbname,user,host,password):
        try:
            self.con = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    host=host,
                    password=password
                    )

            self.cur = self.con.cursor()

        except psycopg2.ProgrammingError as e:
            print('--->Error {}'.format(e))
            sys.exit(1)

    def table_exist(self,name):
        self.n = name
        try:
            self.cur.execute('SELECT 1 from {}'.format(name))          
            ver = self.cur.fetchone()
            print(ver)

        except psycopg2.ProgrammingError as e:
            print('--->Error {}'.format(e))
            return 0
        else:
            return 1

    def get_table(self,name):
        self.cur.execute("SELECT * FROM {};".format(name))
        return self.cur.fetchall()

    def remove_table(self,name):
        self.cur.execute("DROP TABLE IF EXISTS {}".format(name))

    def flush_table(self,name):
        self.cur.execute("TRUNCATE {};".format(name))

    def track_exists(self, name, entry):
        #SQL = "SELECT name FROM {} WHERE name = '{}' ".format(name,entry)
        SQL = "SELECT user_id FROM {} WHERE user_id = '{}' ".format(name,entry)

        self.cur.execute(SQL)
        return self.cur.fetchone() is not None


    def add_entry(self,name,val):
        SQL = "INSERT INTO {} ({}) VALUES".format(self.n,name)
        l = len(val)-1
        SQL += "(%s" + ",%s" * l + ")"
        DATA = val

        self.cur.execute(SQL,DATA)
        self.con.commit()


    def create_table(self,name):
        self.cur.execute("""CREATE TABLE {} (
                id serial PRIMARY KEY     ,
                name              varchar ,
                user_id           bigint  ,
                description       varchar ,
                lang              varchar ,
                created_at        date    ,
                location          varchar ,
                time_zone         varchar ,
                number_tweets     int     ,
                number_followers  int     ,
                following         int     ,
                member_of         int
                );
                """.format(name))
        self.con.commit()
    
    
    def close(self):
        self.cur.close()
        self.con.close()
