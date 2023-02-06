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
header = ['ISBN 13', 'Author', 'Title','Publication Date', 'Stocks', 'Price(Php)']
columnsdB = 'isbn13, authors, title, publication_date, stocks, price'

dbcolumns = ["isbn13","authors","title","publication_date","stocks","price"]

dbcustcolumns = ["customer_id","username","password","first_name","last_name",
             "phone_no","email","street", "baranggay", "city","province", "region", "country",
             "zip_code","admin", "profession"]  

dbtranscolumns =["transaction_id","group_no","date","time","customer_id","isbn13","quantity","sub_total"]           

sql = "SELECT " + columnsdB + " FROM books order by bookid asc;"
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

df = querydatafromdatabase(sql,[],dbcolumns)
df = df.set_axis(header,axis=1)
df['Quantity'] = 0
cartdata = {'ISBN 13': None, 'Author': None, 'Title': None, 'Price(Php)': None, 'Quantity': None, 'SubTotal(Php)': None}

bests = querydatafromdatabase(sqlbestseller,[],["ISBN 13","Authors", "Title","Date", "Revenue (PhP)"])
bestsellermonth = bests[['Authors','Title']]



app = dash.Dash()

app.layout = html.Div([ #all division
    
     
    html.Div(children = [
    html.Div([dcc.Store(id = 'user-login',storage_type = 'session', data = "mssantiago7"),]),
    html.Div([dcc.Store(id = 'cust-id',storage_type = 'session', data = "39"),]),
      
    html.Button (id = 'try', style={'display':'none'}),   
        
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
   
    html.Div(id = 'header-msg', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    #banner
    html.Div(id = 'banner',
             children = (html.H1 ('Order Form', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    #top div
    html.Div(id = 'top-style',children=[
    
    #main body
    html.Div(children = [
                                             
          html.H1('BESTSELLERS OF THE MONTH',style={'textAlign':'center','color':'blue'}),                                     
          dash_table.DataTable(
                                id='bestseller',
                                
                                columns = [
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    ],
                                
                                data = bestsellermonth.to_dict('records'),
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
                                page_size=10,
                                style_table={'width':'40%', 'margin-left':'30%' },
                                
                              
                                ),  
html.Div(style = {'height':30}),
html.Div(style = {'backgroundColor':'lightgrey', 'height':5}), 
html.Div(style = {'height':30}),         
    #1stcolumn
    html.Div(id='nothing',children=[
    

        
        
        html.Div(children = [
            html.Label('Search Database:',style={'fontSize':20,'color':'dark grey','font-weight':'bold'}),
            html.Div(style={'height':20}),
            
            html.Div(children = [html.Label(children = 'Author:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='author',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 'margin-right':'10%'}),
                                   ], 
                     style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
            html.Div(children = [html.Label(children = 'Title:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='title',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 'margin-right':'10%'})
                                 ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                             'margin-top':3,'margin-bottom':0,'padding':1,}),
           html.Div(children = [html.Button(id ='search_button',n_clicks = 0,children='Search',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white','display':'block',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%'}),
                                ],style = {'height':25}),                            
          html.Div(children = [html.Button(id='show_all',n_clicks = 0,children='Show All',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white','display':'block',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%'}),
                                ],style = {'height':25}), 
          html.Br(),
          
          html.Div(style = {'height':10, 'backgroundColor':'lightgrey'}),
          html.Br(),
          html.Label("Select Book, Update Quantity and Add to Cart:", style={'fontSize':20, 'color':'dark grey','font-weight':'bold'}),
          html.Div(style = {'height':30}),
          html.Div(id = 'quantity-msg',
                      style = {'display':'none'}),  
            dash_table.DataTable(
                                id='firstdatatable',
                                row_selectable="single",
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False,},
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Stocks', 'id':'Stocks','editable':False, },
                                    {'name': 'Price(Php)', 'id':'Price(Php)','editable':False,'type':'numeric',
                                     'format':{'specifier':'.2f'}, },
                                    {'name': 'Quantity', 'id':'Quantity','editable':True, 'type':'numeric',},
                                    ],
                                
                                data = df.to_dict('records'),
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 11, 'font-family':'Arial',},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                    },
                                page_size=5,
                                style_data_conditional =[
                                    {'if':{'column_id':'Quantity'},
                                     'backgroundColor':'skyblue','textAlign':'center','font-weight':'bold'},
                                    {'if':{'column_id':'Stocks'},
                                     'textAlign':'center'},
                                    {'if':{'column_id':'Price(Php)'},
                                     'textAlign':'right',},
                                    {"if": {"state": "selected"},
                                     "backgroundColor": "inherit !important",
                                     "border": "inherit !important",
                                     }   
                                    ],
                                selected_rows = [],
                                
                              
                                ),
             html.Div(children = [html.Button(id='add_to_cart',n_clicks = 0,children='Add to Cart',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white','display':'block',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'left', 'margin-right':'10%'}),
                                ],style = {'height':25}), 
             
       ], style = {'width':'45%','display': 'inline-block'}),
                                             
         #2nd column start
         html.Div(children = [
             #summary start
             html.Div(id='summary', children = [
             html.H3('Customer Information'),
             html.Div(children = [html.Label(children = 'Name:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='name',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
             html.Div(children = [html.Label(children = 'Adress:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='address',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),                               
             html.Div(children = [html.Label(children = 'Contact:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='contact_no',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
             html.Div(children = [html.Label(children = 'Email:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='email',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
            html.Div(children = [html.Div(style={'height':1.5,})], style = {'backgroundColor': 'lightgrey',
                                                                            'margin-top':10,'margin-bottom':3, 
                                                                            'padding':0}), 
                                              
           html.Div(children=[ html.H3('Cart',style={'width':'45%', 'float':'left'}),
                              ]),
              dash_table.DataTable(
                                id='cartdatatable',
                               
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False,},
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Stocks', 'id':'Stocks','editable':False, },
                                    {'name': 'Price(Php)', 'id':'Price(Php)','editable':False,'type':'numeric',
                                     'format':{'specifier':'.2f'}, },
                                    {'name': 'Quantity', 'id':'Quantity','editable':False, 'type':'numeric',},
                                    {'name': 'SubTotal(Php)', 'id':'SubTotal(Php)','type':'numeric',
                                     'format':{'specifier':'.2f'}, },
                                     ],
                                data = [cartdata],
                                style_cell = { 'textAlign':'left','padding': '5px',
                                               'whiteSpace': 'normal',
                                               'height': 'auto','fontSize': 11, 'font-family':'Arial',},
                                style_as_list_view=True,
                                style_header = {
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                    },
                                
                                row_deletable=True,
                                 page_action='none',
                                 style_table={'height': '220px', 'overflowY': 'auto'},
                                  style_data_conditional =[
                                    {'if':{'column_id':'Quantity'},
                                     'textAlign':'center',},
                                    {'if':{'column_id':'SubTotal(Php)'},
                                     'textAlign':'center',},
                                    {'if':{'column_id':'Price(Php)'},
                                     'textAlign':'right',},
                                    {'if':{'column_id':'Stocks'},
                                     'textAlign':'center',},
                                    ],
                                
                                ),
              html.Div(children = [html.Label(children = 'Total (Php):', style = {'fontSize':12,'fontWeight': 'bold'}), 
                                 dcc.Input(id ='total',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'font-weight': 'bold',
                                                 'margin-left':'5%'}),
                               ],
                       style = {'height':25}),
             
              html.Div(children=[
                  html.Div(id='date',children = datetime.datetime.now().strftime('%Y-%m-%d'),style = {'width':65, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                                 
                  html.Div(id='time',children = datetime.datetime.now().strftime('%H:%M:%S'),style = {'width':100, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                  dcc.Input(id = 'cust_id', value='',type='number',style={'display':'none'}),
                                 
                                 ]),
              ]),#summary end
                                               
                                              
              html.Button(id='checkout',n_clicks = 0,children='Checkout',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%','display': 'block'}),
                                
            
            ], style = {'width':'50%','display': 'inline-block', 'margin-right':'1%', 'float':'right'}),
                                             
        ]),
        ]),
                                   
    ]),
    html.Div(id='bottom-style', children = [
        html.Div([
        html.Label(children = 'Transaction ID:', style = {'fontSize':12,'fontWeight': 'bold'}), 
                                 html.Div(id ='transaction',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'font-weight': 'bold',
                                                 'margin-left':'5%'}),]),
         dcc.Link([html.Button(id='new-order',n_clicks = 0,children='New Order',
                                             style = {'backgroundColor':'blue','width':'20%','height':40,
                                                      'borderRadius':5,'color':'white',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%','display': 'block'}),
                   ],href='/orderform'),
                                ],
        style={'float':'center', 'display':'none', 'margin-left':'40%'})                                           
    ])


@app.callback([Output('header-msg','children'),
               Output('name','value'),
               Output('address','value'),
               Output('contact_no', 'value'),
               Output('email','value'),
               Output('cust_id','value')
              ],
               
              [Input('try','children'),
               
               ],
              [State('user-login','data'),
               State('cust-id','data')
              
               ])
               
def return_3(click,username,custid):
    header = 'Hello, ' + username + '!'
    
    
    sqlsearch = "SELECT * FROM customer WHERE customer_id = " + str(custid)
    
    cust_data = querydatafromdatabase(sqlsearch,[custid], dbcustcolumns)
          
    name = str(cust_data['first_name'][0])+ ' '+str(cust_data['last_name'][0])
    address = str(cust_data['street'][0])+ ' '+str(cust_data['baranggay'][0])+ ' '+str(cust_data['city'][0])+ ' '+str(cust_data['province'][0])+ ' '+str(cust_data['region'][0])+ ' '+str(cust_data['country'][0])+ ' '+str(cust_data['zip_code'][0])
    contact_no = cust_data['phone_no'][0]
    email = cust_data['email'][0]
    return header, name, address, contact_no, email, cust_data['customer_id'][0]



@app.callback(
      [   Output('firstdatatable', 'data'),
        
           ],
      [   Input('search_button', 'n_clicks'),
          Input('show_all','n_clicks'),
          
           ],
      [   State('author', 'value'),
          State('title', 'value'),
           ])

def output(search_button,show_all,author, title):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="show_all":
          sql = "SELECT " + columnsdB + " FROM books order by bookid asc;"
          df = querydatafromdatabase(sql,[],dbcolumns)
          df = df.set_axis(header,axis=1)
          df['Quantity'] = 0
          data = df.to_dict('records'),
          return data
      
       elif eventid =="search_button":
           
          sqlsearch = "SELECT " + columnsdB + " FROM books WHERE authors ~* '(\m"+ author +"\M)' OR title ~* '(\m" + title + "\M)' order by bookid asc;" 
          df = querydatafromdatabase(sqlsearch,[author, title], dbcolumns)
          df = df.set_axis(header,axis=1)
          df['Quantity'] = 0
          
          data = df.to_dict('records'),
          
          return data
      
    
       else:
           raise PreventUpdate
   else:
      raise PreventUpdate

@app.callback(
      [   Output('cartdatatable', 'data'),
          Output('total','value'),
          Output('quantity-msg', 'style'),
          Output('quantity-msg','children')
           ],
      [   Input('add_to_cart', 'n_clicks'),
          
           ],
      [   State('firstdatatable','selected_rows'),     
          State('firstdatatable', 'data'),
          State('cartdatatable','columns'),
          State('cartdatatable', 'data'),
          State('total','value'),

        ])
def addtocart (add_to_cart, selected_rows, data, columns, cartdata, total):
   
    
    dc = data[selected_rows[0]]
    
    if dc['Quantity'] > dc['Stocks']:
        qtymsg = [html.H3('*Stocks not enough. Change quantity.', style={'font-style':'italic','font-size':16, 'color':'red', 'font-weight':'bold', 'float':'right'})]
        return cartdata,total, {'display':'block'},qtymsg
    
    elif dc['Quantity']==0:
        qtymsg = [html.H3('*Quantity is zero. Update quantity', style={'font-style':'italic','font-size':16, 'color':'red', 'font-weight':'bold', 'float':'right'})]
        return cartdata,total, {'display':'block'},qtymsg
    
    else:
        
        subT = dc['Price(Php)']*dc['Quantity']
   
        dc['SubTotal(Php)']= subT
   
        cartdata.append(dc)
    
    
        cd = pd.DataFrame(cartdata)
        cd = cd.dropna()
    
        total = cd['SubTotal(Php)'].sum()
        total ="{0:,.2f}".format(total)
    
        cdata = cd.to_dict('records')
    
        return cdata,total, {'display':'none'},''

@app.callback(
      [   Output('top-style', 'children'),
          Output('top-style', 'style'),
          Output('bottom-style','style'),
          Output('transaction', 'children'),
          Output('banner','children')
          
          
           ],
      [   Input('checkout', 'n_clicks'),
        
           ],
      [   
          State('cartdatatable', 'data'),
          State('total', 'value'),
          State('cust_id','value'),
          State('date','children'),
          State('time','children'),
          State('summary','children')
           ])

def checkout(checkout,cartdata, total, cust_id, date, time, children):
    transtable = pd.DataFrame(cartdata)
    
    if transtable['ISBN 13'][0]==None:
        raise PreventUpdate
    
    else:
        
        transtable['Stocks'] = transtable['Stocks']-transtable["Quantity"]
    
        sqlcheck = "SELECT group_no FROM transactions ORDER BY transaction_id DESC LIMIT 1;"

        group_no = querydatafromdatabase(sqlcheck,[],['group_no'])
           
        if group_no.empty:
            gn = 0;

        else:
            gn = group_no['group_no'][0]
          
        
        g = gn+1
      
        for row in transtable.iterrows():
        
            sqlstock = "UPDATE books SET stocks = " + str(row[1]['Stocks']) + " WHERE isbn13 = " + str(row[1]['ISBN 13'])
            modifydatabase(sqlstock,[row[1]['Stocks'],row[1]['ISBN 13']])
               
            
            sqlinserttrans = "INSERT INTO transactions (group_no,date,time,customer_id,isbn13,quantity,sub_total) VALUES (%s,%s,%s,%s,%s, %s,%s);"
              
            modifydatabase(sqlinserttrans,[str(g),str(date),str(time),str(cust_id), str(row[1]['ISBN 13']),str(row[1]['Quantity']),str(row[1]['SubTotal(Php)'])])
                 
        transid = str(g)
    
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%H:%M:%S') 
        
        banner = (html.H1 ('Order Summary', style = {'margin-left':5}))
    
        return children,{'margin-left':'20%','width':'50%'},{'display':'block', 'margin-left':'20%'},transid,banner
           
      
           
      
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

