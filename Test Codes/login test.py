import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
from dash.exceptions import PreventUpdate


app = dash.Dash()
app.layout = html.Div(children = [
    html.Div(id = 'main', children = [
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
html.Div(id='output1', children='',style={'padding-left':'550px','padding-top':'10px', 'color':'red','display':'block'}),

])

@app.callback(
    [Output('output1', 'children'),
    Output('main', 'children')],
   [Input('verify', 'n_clicks')],
    [State('user', 'value'),
     State('passw', 'value'),
     State('main','children')],prevent_initial_call=True )
def update_output(n_clicks, uname, passw, maindiv):
    
    sqlsearch = "SELECT username,password FROM customer WHERE username = '" + uname +"'"
    df = querydatafromdatabase(sqlsearch,[], ['username','password'])
    
    if uname =='' or uname == None or passw =='' or passw == None:
        return '', maindiv
    elif df.empty:
        return ['Incorrect Username'], maindiv
    elif not df.iloc[0]['password']== passw:
        return ['Incorrect Password'], maindiv
    else:
        if df.iloc[0]['admin']:
            nextdiv = [  html.Div(html.H3('Hello, Admin!', style = {'width':'20%', 'display':'inline-block'})),
                         html.Div(children = [dcc.Link('Inventory', href='/admin/inventory', 
                                                       style = {'margin-right':50}),
                                              dcc.Link('Signout', href='/login')],
                                  style ={'display':'inline-block','float':'right'}) ]
            return '',nextdiv
        else:
            nextdiv = [  html.Div(html.H3('Hello, '+str(uname)+'!', style = {'width':'20%', 'display':'inline-block'})),
                         html.Div(children = [dcc.Link('Inventory', href='/admin/inventory', 
                                                       style = {'margin-right':50}),
                                              dcc.Link('Signout', href='/login')],
                                  style ={'display':'inline-block','float':'right'}) ]
            return '', nextdiv
    
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
print(df['password'])
print(df[['password']])
print(df.iloc[0]['password'])

#%%
if df.iloc[0]['password']==12345:
    print('yes')
else:
    print('no')