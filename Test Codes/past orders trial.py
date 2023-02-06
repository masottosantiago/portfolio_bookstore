import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
import dash_table

from dash.exceptions import PreventUpdate
import datetime

#Database Initialize
booksHeader = ['I','ISBN 13', 'Author', 'Title','Publication Date', 'Stocks', 'Price(Php)']
booksColumnsdB = 'isbn13, authors, title, publication_date, stocks, price'

dbbookscolumns = ["isbn13","authors","title","publication_date","stocks","price"]

dbcustcolumns = ["customer_id","username","password","first_name","last_name",
             "phone_no","email","street", "baranggay", "city","province", "region", "country",
             "zip_code","admin"]  

dbtranscolumns =["transaction_id","group_no","date","time","customer_id","isbn13","quantity","sub_total"]           

sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"


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



app = dash.Dash()

app.layout = html.Div([ #all division
    
     
    html.Div(children = [
    html.Div([dcc.Store(id = 'user-login',storage_type = 'session', data = "mssantiago7"),]),
    html.Div([dcc.Store(id = 'cust-id',storage_type = 'session', data = "39"),]),
     
    html.Button (id = 'try1',children = ["CLICK"], style={'display':'none'}),   
        
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
    dcc.Link('Order Form', href='/orderform', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),
    dcc.Link('Past Orders', href='/pastorders', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}), 
    html.Div(id = 'header-msg2', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    #banner
    html.Div(id = 'banner2',
             children = (html.H1 ('Past Orders', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    #top div
    html.Div(id = 'top-style1',children=[
    
    #main body
    html.Div(children = [
        html.H1(id='loading',children='Loading data. Please wait...', style={'color':'red', 'textAlign':'center'}),
    #1stcolumn
    html.Div(id='nothing1',children=[
        
        dash_table.DataTable(id='past-orders',
                             data = [0],
                             columns = [
                                    {'name': 'Order Details', 'id':'Order Details','editable':False,},
                                    
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False,},
                                    {'name': 'Authors', 'id':'Authors','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Price(Php)', 'id':'Price(Php)','editable':False,'type':'numeric',
                                     'format':{'specifier':'.2f'}, },
                                    {'name': 'Quantity', 'id':'Quantity','editable':False, },
                                    {'name': 'Sub Total(Php)', 'id':'Subtotal(Php)','editable':False,'type':'numeric',
                                     'format':{'specifier':'.2f'}, },
                                    ],
                              style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 11, 'font-family':'Arial',},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                    },
                                style_table={'height': '500px', 'overflowY': 'auto', },)
        ], style={'display':'none', 'width':'55%','float':'center', 'margin-left':'40%'})
        ])
        ])
        ])
@app.callback(
    Output('header-msg2','children'),
    Input('try1','n_clicks'),
    State('user-login','data'),)

def head2 (click, uname):
     header = 'Hello, ' + uname + '!'
     return header
 
@app.callback(
    Output('past-orders','data'),
    Output('loading','style'),
    Output('nothing1', 'style'),
    Input('try1','n_clicks'),
    State('cust-id','data'),
    )

def group(click, custid):
    sqltrans = "SELECT group_no FROM transactions WHERE customer_id = " + str(custid)+" GROUP BY group_no;"
    print(sqltrans)
    dt = querydatafromdatabase(sqltrans,[],['group_no'])      
    setlist = []
   
    for row in dt.iterrows():
    
        sqlgroup = "SELECT * FROM transactions WHERE customer_id = " + str(custid)+" and group_no = "+str(row[1]['group_no'])
        group = querydatafromdatabase(sqlgroup,[],dbtranscolumns)
        total = 0
        tabledata = []
        for row in group.iterrows():
            total = total + row[1]['sub_total']
            sqlbook = "SELECT "+booksColumnsdB+" FROM books WHERE isbn13 = " +str(row[1]['isbn13'])
            b = querydatafromdatabase(sqlbook,[],dbbookscolumns)
            v = [{'Order Details' :'','ISBN 13':row[1]['isbn13'],'Authors':b['authors'][0],
                  'Title':b['title'][0],'Publication Date':b['publication_date'][0],
                  'Price(Php)':b['price'][0],'Quantity':row[1]['quantity'],
                  'Subtotal(Php)':row[1]['sub_total']}]
            z = pd.DataFrame.from_dict(v)
            tabledata.append(z)
            gr = row[1]
        head = [{'Order Details':'Order ID:'+ str(gr['group_no']), 
                'ISBN 13':'','Authors':'','Title':'','Publication Date':'',
                      'Price(Php)':'','Quantity':'','Subtotal(Php)':''},
                    {'Order Details':'Date:'+ str(gr['date']), 
                      'ISBN 13':'','Authors':'','Title':'','Publication Date':'',
                      'Price(Php)':'','Quantity':'','Subtotal(Php)':''},
                    {'Order Details':'Time: '+ str(gr['time']), 
                      'ISBN 13':'','Authors':'','Title':'','Publication Date':'',
                      'Price(Php)':'','Quantity':'','Subtotal(Php)':''},
                    {'Order Details':'Total: '+ str(total)+' Php ', 
                      'ISBN 13':'','Authors':'','Title':'','Publication Date':'',
                      'Price(Php)':'','Quantity':'','Subtotal(Php)':''}
                    ]
        
        headercol = pd.DataFrame.from_dict(head)
        tabledata.insert(0,headercol)
        gh = pd.concat(tabledata)
        setlist.append(gh)
    df = pd.concat(setlist)
    
    
    return df.to_dict('records'), {'display':'none'}, {'display':'inline-block','width':'55%','float':'center', 'margin-left':'23%'}
        
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
