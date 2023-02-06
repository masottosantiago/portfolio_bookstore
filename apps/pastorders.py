import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
import dash_table

from app import app, booksColumnsdB, dbbookscolumns,dbtranscolumns, querydatafromdatabase, modifydatabase



layout = html.Div([ #all division
     
    html.Div(children = [
    
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
    Output('loading','children'),
    Output('nothing1', 'style'),
    Input('try1','n_clicks'),
    State('cust-id','data'),
    )

def group(click, custid):
    sqltrans = "SELECT group_no FROM transactions WHERE customer_id = " + str(custid)+" GROUP BY group_no;"
    dt = querydatafromdatabase(sqltrans,[],['group_no'])      
    if dt.empty:
        df = {'Order Details':None, 
                'ISBN 13':None,'Authors':None,'Title':None,'Publication Date':None,
                      'Price(Php)':None,'Quantity':None,'Subtotal(Php)':None}
        return [df], {'display':'block','textAlign':'center'},'No Past Orders', {'display':'inline-block','width':'55%','float':'center', 'margin-left':'23%'}
    
    
    setlist = []
   
    for row in dt.iterrows():
    
        sqlgroup = "SELECT * FROM transactions WHERE customer_id = " + str(custid)+" and group_no = "+str(row[1]['group_no'])
        group = querydatafromdatabase(sqlgroup,[],dbtranscolumns)
        
        tabledata = []
        total = 0
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
                    {'Order Details':'Total: ', 
                      'ISBN 13':'','Authors':'','Title':'','Publication Date':'',
                      'Price(Php)':'','Quantity':'','Subtotal(Php)':total}
                    ]
        
        headercol = pd.DataFrame.from_dict(head)
        tabledata.insert(0,headercol)
        gh = pd.concat(tabledata)
        setlist.append(gh)
    df = pd.concat(setlist)
    
    
    return df.to_dict('records'), {'display':'none'},'', {'display':'inline-block','width':'55%','float':'center', 'margin-left':'23%'}
        
