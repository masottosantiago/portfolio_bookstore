import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table

from dash.exceptions import PreventUpdate
import datetime

from app import app, booksHeader, booksColumnsdB, dbbookscolumns, df, dbcustcolumns, bestsellermonth, querydatafromdatabase, modifydatabase


df['Quantity'] = 0
cartdata = {'ISBN 13': None, 'Author': None, 'Title': None, 'Price(Php)': None, 'Quantity': None, 'SubTotal(Php)': None}


layout = html.Div([ #all division
    
     
    html.Div(children = [
    
    html.Button (id = 'try_order1', style={'display':'none'}),   
        
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
    dcc.Link('Order Form', href='/orderform1', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),
    dcc.Link('Past Orders', href='/pastorders', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),
   
    html.Div(id = 'header-msg_order1', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    #banner
    html.Div(id = 'banner_order1',
             children = (html.H1 ('Order Form', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    #top div
    html.Div(id = 'top-style_order1',children=[
    
    #main body
    html.Div(children = [
                                             
          html.H1('BESTSELLERS OF THE MONTH',style={'textAlign':'center','color':'blue'}),                                     
          dash_table.DataTable(
                                id='bestseller_order1',
                                
                                columns = [
                                    {'name': 'Authors', 'id':'Author','editable':False, },
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
    html.Div(id='nothing_order1',children=[
    

        
        
        html.Div(children = [
            html.Label('Search Database:',style={'fontSize':20,'color':'dark grey','font-weight':'bold'}),
            html.Div(style={'height':20}),
            
            html.Div(children = [html.Label(children = 'Author:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='author_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 'margin-right':'10%'}),
                                   ], 
                     style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
            html.Div(children = [html.Label(children = 'Title:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='title_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 'margin-right':'10%'})
                                 ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                             'margin-top':3,'margin-bottom':0,'padding':1,}),
           html.Div(children = [html.Button(id ='search_button_order1',n_clicks = 0,children='Search',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white','display':'block',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%'}),
                                ],style = {'height':25}),                            
          html.Div(children = [html.Button(id='show_all_order1',n_clicks = 0,children='Show All',
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
          html.Div(id = 'quantity-msg_order1',
                      style = {'display':'none'}),  
            dash_table.DataTable(
                                id='firstdatatable_order1',
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
             html.Div(children = [html.Button(id='add_to_cart_order1',n_clicks = 0,children='Add to Cart',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white','display':'block',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'left', 'margin-right':'10%'}),
                                ],style = {'height':25}), 
             
       ], style = {'width':'45%','display': 'inline-block'}),
                                             
         #2nd column start
         html.Div(children = [
             #summary start
             html.Div(id='summary_order1', children = [
             html.H3('Customer Information'),
             html.Div(children = [html.Label(children = 'Name:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='name_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
             html.Div(children = [html.Label(children = 'Adress:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='address_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),                               
             html.Div(children = [html.Label(children = 'Contact:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='contact_no_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 }),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
             html.Div(children = [html.Label(children = 'Email:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='email_order1',value = '',
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
                                id='cartdatatable_order1',
                               
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
                                 dcc.Input(id ='total_order1',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'font-weight': 'bold',
                                                 'margin-left':'5%'}),
                               ],
                       style = {'height':25}),
             
              html.Div(children=[
                  html.Div(id='date_order1',children = datetime.datetime.now().strftime('%Y-%m-%d'),style = {'width':65, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                                 
                  html.Div(id='time_order1',children = datetime.datetime.now().strftime('%H:%M:%S'),style = {'width':100, 'display':'inline-block','fontSize':12,'fontWeight': 'bold'}),
                                
                                 ]),
              ]),#summary end
                                               
                                              
              html.Button(id='checkout_order1',n_clicks = 0,children='Checkout',
                                             style = {'backgroundColor':'blue','width':'20%',
                                                      'borderRadius':5,'color':'white',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%','display': 'block'}),
                                
            
            ], style = {'width':'50%','display': 'inline-block', 'margin-right':'1%', 'float':'right'}),
                                             
        ]),
        ]),
                                   
    ]),
    html.Div(id='bottom-style_order1', children = [
        html.Div([
        html.Label(children = 'Transaction ID:', style = {'fontSize':12,'fontWeight': 'bold'}), 
                                 html.Div(id ='transaction_order1',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'font-weight': 'bold',
                                                 'margin-left':'5%'}),]),
         dcc.Link([html.Button(id='new-order_order1',n_clicks = 0,children='New Order',
                                             style = {'backgroundColor':'blue','width':'20%','height':40,
                                                      'borderRadius':5,'color':'white',
                                                      'font-family':'Arial','font-weight': 'bold','fontSize': 12,
                                                      'float':'right', 'margin-right':'10%','display': 'block'}),
                   ],href='/orderform'),
                                ],
        style={'float':'center', 'display':'none', 'margin-left':'40%'})                                           
    ])


@app.callback([Output('header-msg_order1','children'),
               Output('name_order1','value'),
               Output('address_order1','value'),
               Output('contact_no_order1', 'value'),
               Output('email_order1','value'),
               
              ],
               
              [Input('try_order1','children'),
               
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
    return header, name, address, contact_no, email



@app.callback(
      [   Output('firstdatatable_order1', 'data'),
        
           ],
      [   Input('search_button_order1', 'n_clicks'),
          Input('show_all_order1','n_clicks'),
          
           ],
      [   State('author_order1', 'value'),
          State('title_order1', 'value'),
           ])

def output(search_button,show_all,author, title):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="show_all_order1":
          sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
          df = querydatafromdatabase(sql,[],dbbookscolumns)
          df = df.set_axis(booksHeader,axis=1)
          df['Quantity'] = 0
          data = df.to_dict('records'),
          return data
      
       elif eventid =="search_button_order1":
           
          sqlsearch = "SELECT " + booksColumnsdB + " FROM books WHERE authors ~* '(\m"+ author +"\M)' OR title ~* '(\m" + title + "\M)' order by bookid asc;" 
          df = querydatafromdatabase(sqlsearch,[author, title], dbbookscolumns)
          df = df.set_axis(booksHeader,axis=1)
          df['Quantity'] = 0
          
          data = df.to_dict('records'),
          
          return data
      
    
       else:
           raise PreventUpdate
   else:
      raise PreventUpdate

@app.callback(
      [   Output('cartdatatable_order1', 'data'),
          Output('total_order1','value'),
          Output('quantity-msg_order1', 'style'),
          Output('quantity-msg_order1','children')
           ],
      [   Input('add_to_cart_order1', 'n_clicks'),
          
           ],
      [   State('firstdatatable_order1','selected_rows'),     
          State('firstdatatable_order1', 'data'),
          State('cartdatatable_order1','columns'),
          State('cartdatatable_order1', 'data'),
          State('total_order1','value'),

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
      [   Output('top-style_order1', 'children'),
          Output('top-style_order1', 'style'),
          Output('bottom-style_order1','style'),
          Output('transaction_order1', 'children'),
          Output('banner_order1','children')
          
          
           ],
      [   Input('checkout_order1', 'n_clicks'),
        
           ],
      [   
          State('cartdatatable_order1', 'data'),
          State('total_order1', 'value'),
          State('cust-id','data'),
          State('date_order1','children'),
          State('time_order1','children'),
          State('summary_order1','children')
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
      
        for index,row in transtable.iterrows():
            print(row['ISBN 13'])
            sqlstock = "UPDATE books SET stocks = " + str(row['Stocks']) + " WHERE isbn13 = " + str(row['ISBN 13'])
            modifydatabase(sqlstock,[row['Stocks'],row['ISBN 13']])
            print([g,str(date),str(time),cust_id, row['ISBN 13'],row['Quantity'],row['SubTotal(Php)']])   
            
            sqlinserttrans = "INSERT INTO transactions (group_no,date,time,customer_id,isbn13,quantity,sub_total) VALUES (%s,%s,%s,%s,%s, %s,%s);"
              
            modifydatabase(sqlinserttrans,[str(g),str(date),str(time),str(cust_id), str(row['ISBN 13']),str(row['Quantity']),str(row['SubTotal(Php)'])])
                 
        transid = str(g)
    
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%H:%M:%S') 
        
        banner = (html.H1 ('Order Summary', style = {'margin-left':5}))
    
        return children,{'margin-left':'20%','width':'50%'},{'display':'block', 'margin-left':'20%'},transid,banner
