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
             "zip_code","admin"]  

dbtranscolumns =["transaction_id","group_no","date","time","customer_id","isbn13","quantity","sub_total"]           

sql = "SELECT " + columnsdB + " FROM books"


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


app = dash.Dash()

app.layout = html.Div([
    html.Div(children = [
    
     html.Div([dcc.Store(id = 'user-login',storage_type = 'session', data = "mssantiago7"),]),
     html.Button (id = 'try', style={'display':'none'}),   
        
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
   
    html.Div(id = 'header-msg', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    html.Div(children = (html.H1 ('Order Form', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    
    
    #main body
    html.Div(children = [
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
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
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
             html.Div(id = 'quantity-msg',children = [
                      html.H3('*Stocks not enough. Change quantity.', style={'font-style':'italic','font-size':16, 'color':'red', 'font-weight':'bold', 'float':'right'})],
                      style = {'display':'none'}),
       ], style = {'width':'45%','display': 'inline-block'}),
                                             
         
         html.Div(children = [
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
                                  html.Button(id='checkout',n_clicks = 0,children='Checkout',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%','display': 'inline-block'}),
                                ],
                       style = {'height':25}),
              html.Div(children = [html.Label(children = 'Transaction ID:', style = {'fontSize':12,'fontWeight': 'bold'}), 
                                 html.Div(id ='transaction',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'font-weight': 'bold',
                                                 'margin-left':'5%'}),
                                 dcc.Input(id = 'cust_id', value='',type='number',style={'display':'none'}),
                                 
                                ],
                       style = {'height':25, 'width':'45%'}),
              html.Div(children=[
                  html.Div(id='date',children = datetime.datetime.now().strftime('%Y-%m-%d'),style = {'width':65, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                                 
                  html.Div(id='time',children = datetime.datetime.now().strftime('%H:%M:%S'),style = {'width':100, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                                 ]),
              
            
            ], style = {'width':'50%','display': 'inline-block', 'margin-right':'1%', 'float':'right'}),
                                             
        ]),
        ])
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
              
               ])
               
def return_2(click,username):
    header = 'Hello, ' + username + '!'
    
    
    sqlsearch = "SELECT * FROM customer WHERE username = 'mssantiago7'"
    cust_data = querydatafromdatabase(sqlsearch,['mssantiago7'], dbcustcolumns)
          
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
          sql = "SELECT " + columnsdB + " FROM books"
          df = querydatafromdatabase(sql,[],dbcolumns)
          df = df.set_axis(header,axis=1)
          df['Quantity'] = 0
          data = df.to_dict('records'),
          return data
      
       elif eventid =="search_button":
           
          sqlsearch = "SELECT " + columnsdB + " FROM books WHERE authors ~* '(\m"+ author +"\M)' OR title ~* '(\m" + title + "\M)'" 
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
          Output('quantity-msg', 'style')
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
        return cartdata,total, {'display':'block'}
    
    else:
        subT = dc['Price(Php)']*dc['Quantity']
   
        dc['SubTotal(Php)']= subT
   
        cartdata.append(dc)
    
    
        cd = pd.DataFrame(cartdata)
    
        total = cd['SubTotal(Php)'].sum()
        total ="{0:,.2f}".format(total)
    
        cdata = cd.to_dict('records')
    
        return cdata,total, {'display':'none'}



def querydatafromdatabase(sql, values,dbcolumns):
    db = psycopg2.connect(
        user="postgres",
        password="abc123",
        host="localhost",
        port=5432,
        database="bookstore")
    cur = db.cursor()
    cur.execute(sql, values)
    print(cur.execute(sql,values))
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

#%%
    name = cust_data[0]['first_name']+ ' '+cust_data[0]['last_name']
    address = cust_data[0]['street']+ ' '+cust_data[0]['baranggay']+ ' '+cust_data[0]['city']+ ' '+cust_data[0]['province']+ ' '+cust_data[0]['region']+ ' '+cust_data[0]['country']+ ' '+cust_data[0]['zip_code']
    contact_no = cust_data[0]['phone_no']
    email = cust_data[0]['email']

#%%
for row in df.iterrows():
    print(row[1]['Stocks'])

#%%
cv = df['Author'][0]
print(cv)

#%%
@app.callback(
      [   Output('transaction', 'children'),
          Output('cartdatatable','data'),
          Output('date','children'),
          Output('time','children'),
        
           ],
      [   Input('checkout', 'n_clicks'),
        
           ],
      [   
          State('cartdatatable', 'data'),
          State('total', 'value'),
          State('cust_id-','value'),
          State('date','children'),
          State('time','children'),
          
           ], prevent_initial_call=True)

def checkout(checkout,cartdata, total, cust_id, date, time):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="checkout":
           if not cartdata == 0:
               
               transtable = pd.DataFrame(cartdata)
               transtable['Stocks'] = transtable['Stocks']-transtable["Quantity"]
               
               for row in transtable.iterrows():
                   
                   sqlstock = "UPDATE books SET stocks = " + row[1]['Stocks'] + "WHERE isbn13 = " + row[1]['ISBN 13']
                   modifydatabase(sqlstock,[row[1]['Stocks'],row[1]['ISBN 13']])
               
                   sqlcheck = "SELECT group_no FROM transactions ORDER BY transaction_id DESC LIMIT 1;"
                   group_no = querydatafromdatabase(sqlcheck,[],dbtranscolumns)
                   
                   sqlinserttrans = "INSERT INTO transactions (group_no,date,time,customer_id,isbn13,quantity,sub_total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
          
                   modifydatabase(sqlinserttrans,[group_no + 1,date,time,cust_id, row[1]['ISBN 13'],row[1]['Quantity'],row[1]['SubTotal(Php)']])
               
               transid = str(group_no) 
               date = datetime.datetime.now().strftime('%Y-%m-%d')
               time = datetime.datetime.now().strftime('%H:%M:%S')
               
               return transid,[0],date,time
           else:
                raise PreventUpdate
       else:
           raise PreventUpdate
      
      
   else:
      raise PreventUpdate
