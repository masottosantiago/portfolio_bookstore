import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
from dash.exceptions import PreventUpdate
import dash_table
from datetime import date


booksHeader = ['ISBN 13', 'Author', 'Title','Publication Date', 'Stocks', 'Price(Php)', 'Publisher ID']
booksColumnsdB = 'isbn13, authors, title, publication_date, stocks, price, publisher_id'

dbbookscolumns = ["isbn13","authors","title","publication_date","stocks","price","publisher_id"]
PAGE_SIZE = 12

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

df = querydatafromdatabase(sql,[],dbbookscolumns)
df = df.set_axis(booksHeader,axis=1)  
da =['','','','','','']
sqlpub= "select publisher_name, publisher_id from publisher"
publist = querydatafromdatabase(sqlpub,[],["Publisher Name", "Publisher ID"])


app = dash.Dash()
app.layout = html.Div([
    html.Div([dcc.Store(id = 'user-login',storage_type = 'session', data = "Admin"),]),
    
    
    
    html.Div(children = [
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
    dcc.Link('Inventory', href='/inventory', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),
    dcc.Link('Reports', href='/reports', 
                                  style = {'margin-right':30, 'display':'inline-block', 
                                           'float':'right'}),        
     
    html.Div(id = 'header-msg', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    html.Div(children = (html.H1 ('Inventory', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    
    html.Br(),
    #main body
    html.Div(children = [
    #1stcolumn
    html.Div(id='nothing',children=[
        html.Label('Search Database:',style={'fontSize':20,'color':'dark grey','font-weight':'bold'}),
        html.Div(style={'height':20}),
    html.Div(children = [html.Label(children = 'ISBN:', style = {'fontSize':12,}), 
                                 dcc.Input(id ='isbn',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':12,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'right',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'vertical-align': 'top','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   
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
    html.Div(style={'height':15}),
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
    html.Label("Add Books or Update Books Database:", style={'fontSize':20, 'color':'dark grey','font-weight':'bold'}),
    html.Div(style = {'height':30}),
    html.Div(id = 'pubdropparent',children = [
        html.Div(id='pubdrop', children=[
        html.Label(children = 'Publisher:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Dropdown(id ='input_publisher',value = '',
                                               options=[
                                                   {'label':publist['Publisher Name'][ind],'value':publist['Publisher ID'][ind]} for ind in publist.index],
                                        style = {'fontSize':14,  'width':'70%'}),]),
                                html.Div(id ='addpubcheck', n_clicks= 0, children = [
                                 dcc.Checklist(id='add-publisher',
                                             options=[
                                                 {'label': 'Add New Publisher', 'value': 'AddPub'}],
                                             value=[], style={'display':'inline-block', 'float':'right','fontSize':14})]),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   html.Div(id = 'newpublisher',children=[
      html.Div(children = [html.Label(children = 'Publisher Name:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_publishername',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                              'margin-top':3,'margin-bottom':0,'padding':1,}),
       html.Div(children = [html.Label(children = 'Publisher Adress:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_publisheradd',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '70%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
       html.Div(children = [html.Label(children = 'Publisher Contact No:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_publishercontact',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
       html.Div(children = [html.Label(children = 'Publisher Email:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_publisheremail',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
                                          
        html.Div(style={'height':5,'backgroundColor':'lightgrey','margin-top':10, 'margin-bottom':10})                               
       
       ], style={'display':'none'}),
   
                                               
    html.Div(children = [html.Label(children = 'ISBN:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_isbn',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '40%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   
    html.Div(children = [html.Label(children = 'Publishing Date:', style = {'fontSize':14,'display':'inline-block','float':'left','margin-right':5}), 
                                 dcc.DatePickerSingle(id='publishing_date',
                                                      display_format='YYYY-MM-DD',
                                                      placeholder = 'YYYY-MM-DD',
                                                      style={'display':'inline-block', 'width':500}),
        
                                   ], style = {'display': 'inline-block', 'horizontalAlign': 'center','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,'font-size':14}),
                                              
    html.Div(children = [html.Label(children = 'Author:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_author',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   
    html.Div(children = [html.Label(children = 'Title:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':10}), 
                                 dcc.Textarea(id ='input_title',value = '',
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '80%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   html.Div(children = [html.Label(children = 'Stocks:', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_stocks',value = '0', type = 'number',min=0,  
                                        style = {'display': 'inline-block', 'horizontal-align': 'middle','fontSize':14,
                                                 'width': '20%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   html.Div(children = [html.Label(children = 'Price (Php):', style = {'fontSize':14,'display':'inline-block','float':'left', 'margin-right':5}), 
                                 dcc.Input(id ='input_price',value = '0.00', type = 'number',min=0.00,step=0.01,
                                        style = {'display': 'inline-block', 'vertical-align': 'middle','fontSize':14,
                                                 'width': '20%','padding-top':1,'padding-bottom':1,'float':'left',
                                                 'margin-right':'10%'}),
                                   ], style = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}),
   
    html.Button(id='add',children =["Add/Update"],style = {'float':'right','verticalAlign':'top'},),
            
    
         
     html.Div(style={'height':15}),
   ],style = {'width':'45%', 'display':'inline-block', 'float':'left','margin-left':'3%'}),
#2ndcolumn
    html.Div(children = [
        
        dash_table.DataTable(
                                id='firstdatatable',
                                
                                columns = [
                                    {'name': 'ISBN 13', 'id':'ISBN 13','editable':False,},
                                    {'name': 'Author', 'id':'Author','editable':False, },
                                    {'name': 'Title', 'id':'Title','editable':False, },
                                    {'name': 'Publication Date', 'id':'Publication Date','editable':False, },
                                    {'name': 'Stocks', 'id':'Stocks','editable':True, },
                                    {'name': 'Price(Php)', 'id':'Price(Php)','editable':True,'type':'numeric',
                                     'format':{'specifier':'.2f'}, },
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
                                page_size=12,
                                style_data_conditional =[
                                    
                                    {'if':{'column_id':'Stocks'},
                                     'backgroundColor':'lightblue','font-weight':'bold','textAlign':'center', 'width':50},
                                    {'if':{'column_id':'Price(Php)'},
                                     'backgroundColor':'lightblue','textAlign':'right',
                                     'width':60},
                                    {'if':{'column_id':'Author'},
                                     'width':60,},
                                    {'if':{'column_id':'ISBN 13'},
                                     'width':50,},
                                    {'if':{'column_id':'Title'},
                                     'width':180,},
                                    {'if':{'column_id':'Publication Date'},
                                     'width':70,},
                                    ],
                                
                                editable=True,
                                row_selectable="single",
                              
        ),
        html.Br(),
        html.Label("(Delete selected from Database)",
                   style={'margin-left':3,'font-style':'italic','font-size':10}),
        html.Button(id='delete',children =["Delete"],
                    style = {'float':'left','verticalAlign':'top'},),
        
        ], style = {'width':'45%', 'display':'inline-block', 'float':'right','margin-right':'3%'})                                         
])
 
])
                    

                                               
@app.callback([Output('header-msg','children'),
              Output('input_isbn','value'),
              Output('publishing_date','date'),
              Output('input_author','value'),
              Output('input_title','value'),
              Output('input_stocks','value'),
              Output('input_price','value'),
              Output('input_publisher','value'),],
              [Input('nothing','children'),
               Input('firstdatatable', 'derived_virtual_selected_rows')
               ],
              [State('user-login','data'),
               State('firstdatatable', 'data')
               ])
def return_2(click,rd,value,tdata):
    header = 'Hello, ' + value + '!'
    d = rd[0]
    
    return header,tdata[d]['ISBN 13'],tdata[d]['Publication Date'],tdata[d]['Author'],tdata[d]['Title'],tdata[d]['Stocks'],tdata[d]['Price(Php)'],tdata[d]['Publisher ID']
    



@app.callback(
      [   Output('firstdatatable', 'data'),
           Output('pubdrop', 'style'),
           Output('newpublisher','style'),
           Output('input_publisher','options'),
          
           ],
      [   Input('search_button', 'n_clicks'),
          Input('show_all','n_clicks'),
          Input('add','n_clicks'),
          Input('delete','n_clicks'),
          Input('addpubcheck','n_clicks'),
          
          
           ],
      [   State('firstdatatable', 'derived_virtual_selected_rows'),
          State('author', 'value'),
          State('title', 'value'),
          State('isbn', 'value'),
          State('firstdatatable', 'data'),
          State('input_isbn','value'),
          State('publishing_date','date'),
          State('input_author','value'),
          State('input_title','value'),
          State('input_stocks','value'),
          State('input_price','value'),
          State('add-publisher','value'),
          State('input_publisher','value'),
          State('input_publishername','value'),
          State('input_publisheradd','value'),
          State('input_publishercontact','value'),
          State('input_publisheremail','value'),
          State('pubdrop', 'style'),
          State('newpublisher','style'),
          State('input_publisher','options'),
          
           ])

def output(search_button,show_all,update,delete,newpubclick,rowid,author, title, isbn,table,
           input_isbn,publishing_date,input_author,input_title,input_stocks,input_price,addnewpub,
           input_publisher,input_publishername,input_publisheradd,input_publishercontact,
           input_publisheremail, pubdropstyle,newpubstyle,options):
    
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="show_all":
          sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
          df = querydatafromdatabase(sql,[],dbbookscolumns)
          df = df.set_axis(booksHeader,axis=1)
          data = df.to_dict('records'),
          
          return data,pubdropstyle,newpubstyle,options
      
       elif eventid =="search_button":
          
          if len(isbn)==0:
              sqlsearch = "SELECT " + booksColumnsdB + " FROM books WHERE authors ~* '(\m"+ author +"\M)' OR title ~* '(\m" + title + "\M)' OR isbn13 = NULL"
              df = querydatafromdatabase(sqlsearch,[author, title, isbn], dbbookscolumns)
              df = df.set_axis(booksHeader,axis=1)
              data = df.to_dict('records'),
              return data,pubdropstyle,newpubstyle,options
          else:
              sqlsearch = "SELECT " + booksColumnsdB + " FROM books WHERE authors ~* '(\m"+ author +"\M)' OR title ~* '(\m" + title + "\M)' OR isbn13 = " + isbn 
              df = querydatafromdatabase(sqlsearch,[author, title, isbn], dbbookscolumns)
              df = df.set_axis(booksHeader,axis=1)
              data = df.to_dict('records'),
              return data,pubdropstyle,newpubstyle,options
          
          
       elif eventid == "add":
           
           pubstyle = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}
                   
           
           if addnewpub == ['AddPub']:
               sqlpub = "INSERT INTO publisher publisher_name, publisher_address, publisher_contact, publisher_email VALUES (%s,%s,%s,%s)"
               modifydatabase(sqlpub,[input_publishername,input_publisheradd,input_publishercontact,input_publisheremail])
               sqlpub= "select publisher_name, publisher_id from publisher"
               publist = querydatafromdatabase(sqlpub,[],["Publisher Name", "Publisher ID"])
               options=[{'label':publist['Publisher Name'][ind],'value':publist['Publisher ID'][ind]} for ind in publist.index]
               sqlnewpubid = "select publisher_id from publisher where publsiher_name = '"+ input_publishername + "'"
               input_publisher=querydatafromdatabase(sqlnewpubid,[],["publisher_id"]).iloc[0]                        
           
           indata = [input_isbn,input_author,input_title,publishing_date,input_stocks,input_price,input_publisher]
               
           sqlsearch = "SELECT True FROM books WHERE isbn13 = %s"
           df = querydatafromdatabase(sqlsearch,[input_isbn], ["isbn13"])
           
           if not df.empty:
               sqlupdate = "UPDATE books SET isbn13 = "+ str(input_isbn) + ", authors='" + input_author + "',title='"+input_title+"',publication_date='"+publishing_date+"',stocks="+str(input_stocks)+",price="+str(input_price)+",publisher_id="+str(input_publisher)+" WHERE isbn13="+str(input_isbn)+" order by bookid asc;"
 
              
               modifydatabase(sqlupdate,indata.append(input_isbn))
               sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
               df = querydatafromdatabase(sql,[],dbbookscolumns)
               df = df.set_axis(booksHeader,axis=1)
               data = df.to_dict('records'),
               return data, pubstyle,{'display':'none'},options
               
           else:
               
               sqlinsert = "INSERT INTO books " + booksColumnsdB + " VALUES(%s, %s, %s, %s, %s, %s)"
                     
               modifydatabase(sqlinsert,indata)
               sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
               df = querydatafromdatabase(sql,[],dbbookscolumns)
               df = df.set_axis(booksHeader,axis=1)
               data = df.to_dict('records'),
               return data, pubstyle,{'display':'none'},options
               
          
          
       elif eventid == "delete":
           
           z = table[rowid[0]]['ISBN 13']
           sqldelete = "DELETE FROM books WHERE isbn13 = %s"
           modifydatabase(sqldelete,[z])
           sql = "SELECT " + booksColumnsdB + " FROM books order by bookid asc;"
           df = querydatafromdatabase(sql,[],dbbookscolumns)
           df = df.set_axis(booksHeader,axis=1)
           data = df.to_dict('records'),
           return data, pubdropstyle,newpubstyle,options
       
       elif eventid == "addpubcheck":
           if addnewpub == ['AddPub']:
               return table, {'display':'none'},{'display':'block'},options
           
           else:
               pubstyle = {'display': 'inline-block', 'horizontal-align': 'middle','width':'100%',
                                               'margin-top':3,'margin-bottom':0,'padding':1,}
               
               return table, pubstyle, {'display':'none'},options
       
       else:
           raise PreventUpdate
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

#%%
html.Div(children = [
        html.H1 ('Inventory', style = {'margin-left':5, 'width':'50%', 'display':'inline-block'}),
        dcc.Link('Inventory', href='/inventory', 
                                  style = {'margin-right':50, 'display':'inline-block', 
                                           'float':'right','width':'10%'}),
        dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                           'width':'10%'}),
        ], style = {'backgroundColor':'lightgrey'}),

#%%

v = df['ISBN 13']

vf = df.iloc[0]['ISBN 13']
print(df.iloc[0])

"UPDATE books SET isbn13 = "+ input_isbn + ", authors=" + input_author + ",title="+input_title+",publication_date="+publishing_date+",stocks="+input_stocks+",price="+input_price+" WHERE isbn13="+input_isbn
               