import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


from app import app, querydatafromdatabase

layout = html.Div(children =[
    html.Div(id='main_login', children =[
    
    html.Div(
        dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
                  style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
                         'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
                         }),
        ),
    html.Div(
        dcc.Input(id="passw", type="password", placeholder="Enter Password",className="inputbox2",
                  style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
                         'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
                         }),
        ),
    html.Div(children = [
        html.Div(
            html.Button('Verify', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
            style={'display': 'inline-block','width':'49.5%','padding-top':'30px', 'float': 'left', 'textAlign':'right'},
            ),
        html.Div(
            dcc.Link(html.Button('Cancel', id='cancel', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
                     style={'display': 'inline-block','width':'49.5%','padding-top':'30px', 'float': 'right'},href='/' )),
        ]),
    html.Div(dcc.Link('No account yet?', href='/signup'), style = {'textAlign': 'right', 'margin-right':'35%'}),
    
    ]),
    html.Div(id='output1', children='',style={'padding-left':'550px','padding-top':'10px', 'color':'red'}),
    
    ])

@app.callback(
    [Output('main_login','children'),
     Output('output1', 'children'),
     Output('user-login','data'),
     Output('cust-id','data')
     
    ],
   [Input('verify', 'n_clicks')],
    [State('user', 'value'),
     State('passw', 'value'),
     State('main_login','children')
     ])
def update_output(n_clicks, uname, passw, login_div):
    
    sqlsearch = "SELECT customer_id, password, admin FROM customer WHERE username = '" + uname + "'"
    df = querydatafromdatabase(sqlsearch,[], ['customer_id','password','admin'])
    
    if uname =='' or uname == None or passw =='' or passw == None:
        return login_div,"","",""
    elif df.empty:
        return login_div,'Incorrect Username',"",""
    elif not df.iloc[0]['password']== passw:
        return login_div,'Incorrect Password',"",""
    else:
        custid = df['customer_id'][0]
        if df.iloc[0]['admin']:
            nextdiv = [  html.Div(children = [
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
   
    html.Div('Hello, Admin!', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    
    html.Div(style={'height':100}),
    html.Div(dcc.Link(html.Button(id='but_rep',children="REPORTS", 
                                  style={'fontSize':30, 'font-weight':'bold','width':500,'height':100,}),
             href='/reports' ),style={'textAlign':'center', 'margin-bottom':20}),
    html.Div(style={'height':5}),
    html.Div(dcc.Link(html.Button("INVENTORY", style={'fontSize':30, 'font-weight':'bold','width':500,'height':100}),
             href='/inventory' ),style={'textAlign':'center'}),
    
    ]
            return nextdiv,'',"Admin",custid
        else:
            
            nextdiv = nextdiv = [  html.Div(children = [
    dcc.Link('Signout', href='/', 
                                  style = {'display':'inline-block','float':'right',
                                          'margin-right':10}),
   
     
    html.Div('Hello, '+ str(uname)+'!', style = {'width':'20%', 'display':'inline-block','float':'left',
                                         'font-weight':'bold','font-size':16, 'margin-left':6}),
    ]),
    
    
    html.Br(),
    html.Div(style={'height':100}),
    html.Div(dcc.Link(html.Button("ORDER FORM", style={'fontSize':30, 'font-weight':'bold','width':500,'height':100}),
             href='/orderform' ),style={'textAlign':'center','margin-bottom':20}),
    html.Div(style={'height':5}),
    html.Div(dcc.Link(html.Button("PAST ORDERS", style={'fontSize':30, 'font-weight':'bold','width':500,'height':100}),
             href='/pastorders' ),style={'textAlign':'center'})
    
    ]
            return nextdiv,'',uname, custid
