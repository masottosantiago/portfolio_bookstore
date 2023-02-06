# -*- coding: utf-8 -*-

import dash
import pandas as pd
import psycopg2



app = dash.Dash(__name__)
server = app.server

df_region = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refregion.csv')
df_province = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refprovince.csv')
df_cities = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refcitymun.csv')
df_brgy = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refbrgy.csv')
dbcustcolumns = ["customer_id","username","password","first_name","last_name",
             "phone_no","email","street", "baranggay", "city","province", "region", "country",
             "zip_code","admin","profession"]

booksHeader = ['ISBN 13', 'Author', 'Title','Publication Date', 'Stocks', 'Price(Php)', "Publisher ID"]
booksColumnsdB = 'isbn13, authors, title, publication_date, stocks, price, publisher_id'

dbbookscolumns = ["isbn13","authors","title","publication_date","stocks","price", "publisher_id"]
dbtranscolumns =["transaction_id","group_no","date","time","customer_id","isbn13","quantity","sub_total"]           


sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
sqlbestseller = "select books.isbn13,books.authors,books.title,concat(TO_CHAR(date,'Month'),date_part('year',date)),SUM(quantity) from transactions inner join books on books.isbn13 = transactions.isbn13 where concat(TO_CHAR(date,'Month'),date_part('year',date)) = concat(TO_CHAR(CURRENT_DATE,'Month'),date_part('year',CURRENT_DATE)) group by 1,2,3,4 order by SUM(quantity) desc;"

def querydatafromdatabase(sql, values,dbcolumns):
    db = psycopg2.connect(
        user="postgres",
        password="abc123",
        host="localhost",
        port=5432,
        database="bookstore")
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = psycopg2.connect(
            user="postgres",
            password="abc123",
            host="localhost",
            port=5432,
            database="bookstore")
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()
    
df = querydatafromdatabase(sql,[],dbbookscolumns)
df = df.set_axis(booksHeader,axis=1)  
bests = querydatafromdatabase(sqlbestseller,[],["ISBN 13","Authors", "Title","Date", "Revenue (PhP)"])
bestsellermonth = bests[['Authors','Title']].iloc[0:10]
sqlpub= "select publisher_name, publisher_id from publisher"
publist = querydatafromdatabase(sqlpub,[],["Publisher Name", "Publisher ID"])