import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
import dash_table
import math

from dash.exceptions import PreventUpdate
import datetime

#Database Initialize
header = ['ISBN 13', 'Author', 'Title','Publication Date', 'Stocks', 'Price(Php)']
columnsdB = 'isbn13, authors, title, publication_date, stocks, price'

dbcolumns = ["isbn13","authors","title","publication_date","stocks","price"]

dbcustcolumns = ["customer_id","username","password","first_name","last_name",
             "phone_no","email","street", "baranggay", "city","province", "region", "country",
             "zip_code","admin"]  

dbtranscolumns =["transaction_id","group_no","date","time","customer_id","isbn13","quantity","sub_total"]           

sql = "SELECT " + columnsdB + " FROM books order by bookid asc;"
sqlbestseller = "SELECT isbn13, SUM(quantity) FROM transactions where date_part('month',date) = date_part('month',CURRENT_DATE) and date_part('year',date) = date_part('year',CURRENT_DATE) GROUP BY isbn13 order by SUM(quantity) desc"




app = dash.Dash()

app.layout = html.Div([ #all division
    
     
    html.Div(children = [
    html.Div([dcc.Store(id = 'user-login',storage_type = 'session', data = "mssantiago7"),]),
    html.Div([dcc.Store(id = 'cust-id',storage_type = 'session', data = "39"),]),
     
    html.Button (id = 'try3',children = ["CLICK"], style={'display':'none'}),   
        
   dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
    dcc.Link('Inventory', href='/inventory', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),
    dcc.Link('Reports', href='/reports', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),  
    html.Div(id = 'header-msg3', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    #banner
    html.Div(id = 'banner3',
             children = (html.H1 ('Reports', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    #top div
    html.Div(id = 'top-style3',children=[
    html.Div(children = [
        html.Div('Load Report:', style = {'fontSize':16, 'font-weight':'bold', 'display':'inline-block','width':'30%','margin-left':20}),
        html.Div(style={'height':5}),
    html.Div( id = 'click', children=[
    dcc.Dropdown(
        id='reports-dropdown',
        options=[
            {'label': 'Top Customers of the Year', 'value': 'TopCustomers'},
            {'label': 'Bestseller of the Year', 'value': 'Bestsellers'},
            {'label': 'Most Popular Authors', 'value': 'PopularAuthors'},
            {'label': 'Total Revenues', 'value': 'TotalRevenues'},
            {'label': 'Revenues by Publisher', 'value': 'RevenuesByPublisher'},
            {'label': 'Revenues by Book', 'value': 'RevenuesByBook'},
            
        ],
        value='',
        placeholder="Select a Report",
        style = {'width':'60%', 'margin-left':20}
    ),]),
    ]),
    html.Div(style={'height':20}),
    html.Div(style={'height':2, 'backgroundColor':'lightgrey'}),
    html.Div(id = 'msg-loading',children =
             html.H1(id='loading3',children='Loading data. Please wait...', style={'color':'red', 'textAlign':'center'}),
             style = {'display':'none'}
            ),
    #main body
    html.Div(children = [
        
    #1stcolumn
    html.Div(id='nothing3',children=[
        
        
        ],)
        ])
        ])
        ])
@app.callback(
    Output('header-msg3','children'),
    Input('try3','n_clicks'),
    State('user-login','data'),)

def head3 (click, uname):
     header = 'Hello, ' + uname + '!'
     return header
 
@app.callback(
    Output('msg-loading','style'),
    Input('reports-dropdown','value'))

def loading_msg(report):
    if report == '':
        return {'display':'none'}
    else:
        print(report)
        return {'display':'block'}

@app.callback(
    Output('nothing3','children'),
    Output('loading3','style'),
    Input('reports-dropdown','value'),
    )

def reports(report):
    if report == 'Bestsellers':
        sqlbestseller = "select books.isbn13,books.authors,books.title,books.publication_date,publisher.publisher_name,date_part('year',date),SUM(quantity) from transactions inner join books on books.isbn13 = transactions.isbn13 inner join publisher on books.publisher_id = publisher.publisher_id where date_part('year',date) = date_part('year',CURRENT_DATE) group by 1,2,3,4,5,6 order by SUM(transactions.quantity) desc;" 
        bests = querydatafromdatabase(sqlbestseller,[],["ISBN 13", "Authors", "Title", "Publication Date","Publisher Name","Year", "Revenue (PhP)"])
        bestseller = bests.drop(['Year'],axis=1)
        
        lay = html.Div(children = [
             html.H1('BEST SELLER OF THE YEAR',style={'textAlign':'center','color':'blue'}),                                     
             dash_table.DataTable(
                                id='revbybook',
                                
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False, },
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Revenue (PhP)', 'id':'Revenue (PhP)','editable':False, 'type':'numeric',
                                     'format':{'specifier':'.2f'},}
                                    ],
                                
                                data = bestseller.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold', },
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_action='none',
                                style_table={'width':'50%', 'margin-left':'25%', 'height': '500px', 'overflowY': 'auto' },
                                style_data_conditional =[
                                    
                                    {'if':{'column_id':'Revenue (PhP)'},
                                     'textAlign':'right'},
                                    
                                    ],
                                
                              
                                ), 
            ])
        return lay,{'display':'none'}
    
    elif report == 'TopCustomers':
        
        sqlbestseller = "SELECT customer_id, SUM(sub_total) FROM transactions where date_part('year',date) = date_part('year',CURRENT_DATE) GROUP BY customer_id order by SUM(sub_total) desc"
 
        bestyear = querydatafromdatabase(sqlbestseller,[],["customer_id","SUM"])
        ind = bestyear.index
        totalcust = len(ind)
        tenpercent = math.ceil(totalcust*.1)     
        topcust = bestyear.iloc[0:tenpercent]      
        top10 = []
        for index,row in topcust.iterrows():
            
            sqltopcust = "select concat(first_name,' ',last_name),profession, concat(street,' ', baranggay,' ', city,' ', province,' ',region,' ', country,' ', zip_code), phone_no, email from customer where customer_id = " + str(row['customer_id'])
            tc = querydatafromdatabase(sqltopcust,[],['Name', 'Profession','Address', 'Phone No', 'Email'])
            tc['Accumulated Purcahse of the Year']  = "{0:,.2f}".format(bestyear['SUM'][index])+' Php'     
            top10.append(tc)

        topcustomer = pd.concat(top10)  
        
        lay = html.Div(children = [
            html.Div(style={'height':20}),
             html.H3('Total Number of Customers To Date: '+str(totalcust), style ={'margin-left':'10%' }),
             html.Div(style={'height':20}),
             html.H1('TOP 10% CUSTOMERS OF THE CURRENT YEAR',style={'textAlign':'center','color':'blue'}),                                     
             
             dash_table.DataTable(
                                id='topcustomer',
                                
                                columns = [
                                    {'name': 'Name', 'id':'Name','editable':False, },
                                    {'name': 'Profession', 'id':'Profession','editable':False, },
                                    {'name': 'Address', 'id':'Address','editable':False, },
                                    {'name': 'Phone No', 'id':'Phone No','editable':False, },
                                    {'name': 'Email', 'id':'Email','editable':False, },
                                    {'name': 'Accumulated Purcahse of the Year', 'id':'Accumulated Purcahse of the Year','editable':False, },
                                    ],
                                
                                data = topcustomer.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold'},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_size=20,
                                style_table={'width':'80%', 'margin-left':'10%' },
                                style_data_conditional =[
                                    {'if':{'column_id':'Accumulated Purcahse of the Year'},
                                    'textAlign':'center','font-weight':'bold'},]
                                
                              
                                ), 
            ])
        return lay,{'display':'none'}
    
    elif report == 'PopularAuthors':
        
        sqlpopauthor = "SELECT isbn13, SUM(quantity) FROM transactions where date_part('year',date) = date_part('year',CURRENT_DATE) GROUP BY isbn13 order by SUM(quantity) desc;"
 
        popauthor = querydatafromdatabase(sqlpopauthor,[],["ISBN 13","SUM"]).iloc[0:10]
        listofisbn = popauthor['ISBN 13'].tolist()
        sqldistinct = "select distinct authors from books where isbn13 in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)           "       
        authorsdistinct = querydatafromdatabase(sqldistinct,listofisbn,["Authors"])     
        children = [] 
        for index,row in authorsdistinct.iterrows():
            
            
            sqlbooksofauthor = "select isbn13, title, publication_date, publisher_name publisher_id from books join publisher on books.publisher_id = publisher.publisher_id WHERE authors = '"+ row["Authors"]+"'"
            
            booksofAuthor = querydatafromdatabase(sqlbooksofauthor,[],['ISBN 13','Title','Publication Date','Publisher' ])
             
            addlay = (
               html.Div(children = [
             html.Div(style={'height':20}),
             html.H2(row["Authors"], style ={'textAlign':'center' }),
             html.Div(style={'height':20}),
             
             dash_table.DataTable(
                                id='author_'+str(index),
                                
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Publisher', 'id':'Publisher','editable':False, },
                                    ],
                                
                                data = booksofAuthor.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold'},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'left'
                                    },
                                editable=False,
                                page_size=20,
                                style_table={'width':'80%', 'margin-left':'10%' },
                                
                                ),
                 html.Div(style={'height':30}),
                 ]))
            children.append(addlay)
        
 
        
        return children,{'display':'none'}
    
    elif report == 'TotalRevenues':
        
        sqlyearrev = "select date_part('year',date),sum(sub_total) as total from transactions group by 1 order by 1 desc"
        yearrev = querydatafromdatabase(sqlyearrev,[],['YEAR', "Revenue(Php)"]).astype(int)
        
        children = [(html.Div(children = [
            html.Div(style={'height':20}),
             
            html.H1('YEARLY REVENUE',style={'textAlign':'center','color':'blue'}),                                     
            dash_table.DataTable(
                                id='yearrev',
                                
                                columns = [
                                    {'name': 'YEAR', 'id':'YEAR','editable':False, },
                                    {'name': 'Revenue(Php)', 'id':'Revenue(Php)','editable':False, 'type':'numeric',
                                     'format':{'specifier':'.2f'},},
                                    
                                    ],
                                
                                data = yearrev.to_dict('records'),
                                style_cell = { 'textAlign':'center','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold'},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_size=20,
                                style_table={'width':'40%', 'margin-left':'30%' ,'textAlign':'center'},
                                                              
                                ), 
            html.Div(style={'height':40}),
            
             
             html.H1('MONTHLY REVENUE',style={'textAlign':'center','color':'blue'}), 
             
            ]))]
        
        for index,row in yearrev.iterrows():
            sqlmonrev = "select concat(TO_CHAR(date,'Month'),date_part('year',date)),date_part('month',date) as monthref,sum(sub_total)  from transactions where date_part('year',date) = '" +str(row["YEAR"])+"' group by 1,2 order by monthref asc "  
                                                                                                                                                                          
            monthrev = querydatafromdatabase(sqlmonrev,[],["Month-Year","MonthRef","Revenue(Php)"])
             
            monthrevenue = monthrev.drop(['MonthRef'],axis=1)
            
            
            lay = (html.Div(children = [
                html.Div(children = [
             
             html.H2(str(row["YEAR"]), style ={'textAlign':'center' }),
             
             
             dash_table.DataTable(
                                id='monthlyrev_'+str(index),
                                
                                columns = [
                                    {'name': 'Month-Year', 'id':'Month-Year','editable':False, },
                                    {'name': 'Revenue(Php)', 'id':'Revenue(Php)','editable':False, 'type':'numeric',
                                     'format':{'specifier':'.2f'},},
                                   ],
                                
                                data = monthrevenue.to_dict('records'),
                                style_cell = { 'textAlign':'center','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold'},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_size=20,
                                style_table={'width':'40%', 'margin-left':'30%' ,'textAlign':'center'},
                                
                                ),
                 html.Div(style={'height':30}),
                 ])]))
            
            children.append(lay)
            
        return children,{'display':'none'}
    
    elif report == 'RevenuesByBook':
        
        sqlrevbook = "select books.isbn13,books.authors,books.title,books.publication_date,publisher.publisher_name,SUM(transactions.sub_total) from transactions inner join books on books.isbn13 = transactions.isbn13 inner join publisher on books.publisher_id = publisher.publisher_id group by 1,2,3,4,5 order by SUM(transactions.sub_total) desc;"
        revbook = querydatafromdatabase(sqlrevbook,[],["ISBN 13", "Authors", "Title", "Publication Date","Publisher Name", "Revenue (PhP)"])
        
        lay = html.Div(children = [
             html.H1('REVENUE BY BOOK',style={'textAlign':'center','color':'blue'}),                                     
             dash_table.DataTable(
                                id='revbybook',
                                
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False, },
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Revenue (PhP)', 'id':'Revenue (PhP)','editable':False, 'type':'numeric',
                                     'format':{'specifier':'.2f'},}
                                    ],
                                
                                data = revbook.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold', },
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_action='none',
                                style_table={'width':'50%', 'margin-left':'25%', 'height': '500px', 'overflowY': 'auto' },
                                style_data_conditional =[
                                    
                                    {'if':{'column_id':'Revenue (PhP)'},
                                     'textAlign':'right'},
                                    
                                    ],
                                
                              
                                ), 
            ])
        return lay,{'display':'none'}
    
    
    elif report == 'RevenuesByPublisher':
        
        sqlrevpub = "select publisher.publisher_name,SUM(transactions.sub_total) from transactions inner join books on books.isbn13 = transactions.isbn13 inner join publisher on books.publisher_id = publisher.publisher_id group by publisher.publisher_name"
        revpub = querydatafromdatabase(sqlrevpub,[],["Publisher", "Revenue (PhP)"])
        
        
        lay = html.Div(children = [
             html.H1('REVENUE BY PUBLISHER',style={'textAlign':'center','color':'blue'}),                                     
             dash_table.DataTable(
                                id='revbypub',
                                
                                columns = [
                                    
                                    {'name': 'Publisher', 'id':'Publisher','editable':False, },
                                    {'name': 'Revenue (PhP)', 'id':'Revenue (PhP)','editable':False, 'type':'numeric',
                                     'format':{'specifier':'.2f'},}
                                    ],
                                
                                data = revpub.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 12, 'font-family':'Arial',
                                               'font-weight':'bold', },
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'lightblue',
                                    'fontWeight': 'bold',
                                    'textAlign':'center'
                                    },
                                editable=False,
                                page_action='none',
                                style_table={'width':'30%', 'margin-left':'35%','height': '500px', 'overflowY': 'auto' },
                                style_data_conditional =[
                                    
                                    {'if':{'column_id':'Revenue (PhP)'},
                                     'textAlign':'right'},
                                    
                                    ],
                                
                              
                                ), 
            ])
        return lay,{'display':'none'}
    
    else:
        raise PreventUpdate
    

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
    
  


if __name__ == '__main__':
    app.run_server()
