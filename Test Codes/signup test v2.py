import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
import pandas as pd
from dash.exceptions import PreventUpdate

df_region = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refregion.csv')
df_province = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refprovince.csv')
df_cities = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refcitymun.csv')
df_brgy = pd.read_csv('https://raw.githubusercontent.com/clavearnel/philippines-region-province-citymun-brgy/master/csv/refbrgy.csv')
dbcustcolumns = ["customer_id","username","password","first_name","last_name",
             "phone_no","email","street", "baranggay", "city","province", "region", "country",
             "zip_code","admin"]

app = dash.Dash()
app.layout = html.Div( children = [
    
    dcc.ConfirmDialog(id='confirm', message = 'Please fill in all fields.'),
    html.Div(children = (html.H1 ('Sign Up', style = {'margin-left':5})), 
             style = {'backgroundColor':'lightgrey'}),
    
    #  user  
    html.Div([
        
    html.Div([
    html.Div(['Username'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='username',value='',required = True,style={'fontSize':14,'padding':7,
                                                     'outline':'none',}),]),],
        style = {'display': 'inline-block', 'width':'33%'}),
    
    html.Div([
    html.Div(['Password'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='password1',type="password", value='',required = True,
              style={'fontSize':14,'padding':7,'outline':'none'}),]),],
        style = {'display': 'inline-block', 'width':'33%'}),
    
    html.Div([
    html.Div(['Confirm Password'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='password-confirm',type="password", value='', required = True,
              style={'fontSize':14,'padding':7, 'outline':'none'}),]),],
        style = {'display': 'inline-block', 'width':'33%'}),
    ], style = {'margin-bottom':20}),
    
    html.Div(id = 'status_msg', children = '', style = {'fontSize':12, 'color':'red', 'font-style':'italic', 'margin-bottom':10}),
    
    #customer data divider
    
    html.Div(
        html.Div('Customer Data', style={'margin-left':5, 'fontSize':20,'font-weight':'bold'}),
                                         style={'backgroundColor':'whitesmoke','margin-bottom':20}),
    
    #customer data name
    
    html.Div([
        
    html.Div([
    html.Div(['First Name'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='firstname',value='',style={'fontSize':14, 'width':'90%','padding':7, 'outline':'none'},required = True),]),],
        style = {'display': 'inline-block', 'width':'50%'}),
    
    html.Div([
    html.Div(['Last Name'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='lastname', value='', required = True,
              style={'fontSize':14, 'width':'90%','padding':7, 'outline':'none'}),]),],
        style = {'display': 'inline-block', 'width':'50%'}),
       
    ], style = {'margin-bottom':10}),
    
    #customer profession
    
    html.Div([
        
    html.Div([
    html.Div(['Profession'], style ={'fontSize':14}),
    html.Div([
    dcc.Dropdown(id='profession',value='',
                 options=[
                     {'label': 'Student', 'value': 'Student'},
                     {'label': 'Faculty', 'value': 'Faculty'},
                     {'label': 'Others', 'value': 'Others'}
                     ],
              style={'fontSize':14,  'width':'100%'}),]),],
        style = {'display': 'inline-block', 'width':'30%', 'verticalAlign':'top'}),
    
    html.Div(id = 'other', children = [
    html.Div(['Other Profession'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='other_prof', value='', style={'fontSize':14, 'width':'90%','padding':7},
              ),]),],
        style = {'display': 'none', 'width':'50%', 'margin-left':'5%'},
        ),
       
    ], style = {'margin-bottom':20}),
    
    
    #customer data phone and email
    
    html.Div([
        
    html.Div([
    html.Div(['Phone Number'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='phonenumber',value='',inputMode = 'numeric',
              style={'fontSize':14, 'width':'90%','padding':7}),]),],
        style = {'display': 'inline-block', 'width':'30%'}),
    
    html.Div([
    html.Div(['Email'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='email', value='', style={'fontSize':14, 'width':'90%','padding':7, 'type':'email'}),]),],
        style = {'display': 'inline-block', 'width':'50%', 'margin-left':'5%'}),
       
    ], style = {'margin-bottom':20}),
    
    html.Div(id = 'passemail_msg', children = '', style = {'fontSize':12, 'color':'red', 'font-style':'italic', 'margin-bottom':10}),

    
    #address divider
    
    html.Div(
        html.Div('Address', style={'margin-left':5, 'fontSize':20,'font-weight':'bold'}),
                                         style={'backgroundColor':'whitesmoke','margin-bottom':20}),
    
    #  customer data region 
    html.Div([
        
    html.Div([
    html.Div(['Country'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='country',value='Philippines',disabled = True, 
              style={'fontSize':14, 'width':'90%','padding':7}),]),],
        style = {'display': 'inline-block', 'width':'10%','verticalAlign':'top'}),
    
    html.Div([
    html.Div(['Region'], style ={'fontSize':14}),
    html.Div(id = 'reg-id', children = [
    dcc.Dropdown(id='region',value='',
                  options=[
          {'label':df_region['regDesc'][ind],'value':df_region['regCode'][ind]} for ind in df_region.index
        ],
              style={'fontSize':14,  'width':'100%'}),]),],
        style = {'display': 'inline-block', 'width':'40%', 'margin-left':'3%','verticalAlign':'top'}),
    
    html.Div([
    html.Div(['Province'], style ={'fontSize':14}),
    html.Div(id ='prov-id', children = [
    dcc.Dropdown(id='province',value='',options = [],
              style={'fontSize':14,  'width':'100%'}),]),],
        style = {'display': 'inline-block', 'width':'30%', 'margin-left':'3%','verticalAlign':'top'}),
    
    html.Div([
    html.Div(['ZipCode'], style ={'fontSize':14,  'width':'50%', }),
    html.Div([
    dcc.Input(id='zipcode',value='',inputMode = 'numeric', 
              style={'fontSize':14, 'width':'100%','padding':7}),]),],
        style = {'display': 'inline-block', 'width':'9%', 'margin-left':'3%','verticalAlign':'top' }),
    
    ], style = {'margin-bottom':10, 'verticalAlign':'top'}),
    
    #customer data address
    
    html.Div([
        
    html.Div([
    html.Div(['City'], style ={'fontSize':14}),
    html.Div([
    dcc.Dropdown(id='city',value='', style={'fontSize':14, 'width':'100%',}),]),],
        style = {'display': 'inline-block', 'width':'40%', 'float':'left'}),
        
    html.Div([
    html.Div(['Baranggay'], style ={'fontSize':14}),
    html.Div([
    dcc.Dropdown(id='baranggay',value='', style={'fontSize':14, 'width':'100%'}),]),],
        style = {'display': 'inline-block', 'width':'40%', 'margin-left':'3%',
                  }),

    ], style = {'margin-bottom':10}),
    
    #street
    html.Div([
        
    html.Div([
    html.Div(['Street'], style ={'fontSize':14}),
    html.Div([
    dcc.Input(id='street',value='', style={'fontSize':14, 'width':'98%','padding':7}),]),],
        style = {'display': 'inline-block', 'width':'100%','float':'right','margin-bottom':20}),
        
    ], style = {'margin-bottom':20}),
    
    
    html.Div([
    
    #add href for cancel, and signup success go back to login page
    html.Button(id='cancel-signup', n_clicks=0,children='Cancel',
                style={'fontSize':20, 'display':'inline-block','float':'center','margin-right':25,'width':100}),
    html.Button(id='signup-button', n_clicks=0,children='Sign Up',style={'fontSize':20, 'margin-left':25,'width':100}),
    ], style = {'float':'middle', 'textAlign':'center'}),
    html.H1(id='number-out')

], style = {'width':'50%','float':'middle','display': 'inline-block', 'margin-left':'25%'})


@app.callback(
    [Output('province','options'),
    Output('city','options'),
    Output('baranggay','options'),
    Output('province','value'),
    Output('city','value'),
    Output('baranggay','value'),
    Output('status_msg','children'),
    Output('other','style'),
    Output('username','value'),
    Output('confirm', 'displayed'),
    Output('passemail_msg','children'),],
    
    [Input('region','value'),
    Input('province','value'),
    Input ('city','value'),
    Input('username','value'),
    Input('password-confirm','value'),
    Input('profession','value'),
    Input('phonenumber','value'),
    Input('email','value'),
    Input('signup-button', 'n_clicks'),
    
    ],
    
    [State('province','options'),
     State('city','options'),
     State('baranggay','options'),
     State('baranggay','value'),
     State('password1','value'),
     State('other','style'),
     State('other_prof','value'),
     State('firstname','value'),
     State('lastname','value'),
     State('country','value'),
     State('zipcode','value'),
     State('street','value')],)

def data_update (region,province,city, username, confirm_pass,profession,phonenumber, email, 
                 signup_button,province_opt, city_opt,brgy_opt,brgy_val,password1,other,
                 other_prof_val, firstname,lastname, country, zipcode, street):

#output format(province_opt, city_opt, brgy_opt, province, city, brgy_val,msg,other,username, False)    
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
           
       if eventid == 'username':
           sqlsearch = "SELECT True FROM customer WHERE username = %s"
           df = querydatafromdatabase(sqlsearch,[username], ["username"])
           
           if not df.empty:
               msg = 'Username already exist.'
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,msg,other,username, False,''
           else:
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username,False, ''
       
       elif eventid == 'password-confirm':
           if not password1 == confirm_pass:
               msg = 'Password mismatch.'
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,msg,other,username, False,''
           else:
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, False,''
       
       elif eventid == 'profession':
           if profession == 'Others':
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',{'display': 'inline-block', 'width':'50%', 'margin-left':'5%'},username, False, ''
           else:
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',{'display': 'none'},username, False,''
       
       elif eventid == 'phonenumber':
           sqlsearch = "SELECT True FROM customer WHERE phone_no = %s"
           df = querydatafromdatabase(sqlsearch,[phonenumber], ["phone_no"])
           
           if not df.empty:
               msg = 'Phone number already exist.'
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, False, msg
           else:
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, False, ''
       
       elif eventid == 'email':
           sqlsearch = "SELECT True FROM customer WHERE email = %s"
           df = querydatafromdatabase(sqlsearch,[email], ["email"])
           
           if not df.empty:
               msg = 'Email already exist.'
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, False, msg
           else:
               return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, False, ''
        
       
       elif eventid == "region":
           prov = df_province.loc[df_province['regCode']== region]
           province_opt = [{'label':prov['provDesc'][ind],'value':prov['provCode'][ind]} for ind in prov.index]
           return province_opt,[],[],0,0,0,'',other,username, False, ''
    
       elif eventid == 'province':
           city = df_cities.loc[df_cities['provCode']==province]
           city_opt = [{'label':city['citymunDesc'][ind],'value':city['citymunCode'][ind]} for ind in city.index]
           print(city_opt)
           return province_opt,city_opt,[],province,0,0,'',other,username, False,''
       
       elif eventid == 'city':
           brgy = df_brgy.loc[df_brgy['citymunCode']==city]
           brgy_opt = [{'label':brgy['brgyDesc'][ind],'value':brgy['brgyCode'][ind]} for ind in brgy.index]
           return province_opt,city_opt,brgy_opt,province,city,0,'',other,username, False,''
       
       elif eventid =='signup-button':
          if profession == "Others":
              profession = other_prof_val
           
          elements = [username, password1, confirm_pass,firstname, lastname, profession,
                      phonenumber, email, country, region, province, city,
                      brgy_val, zipcode, street, True, profession]
                      
          if '' in elements:
             
              
              return province_opt, city_opt, brgy_opt, province, city, brgy_val,'',other,username, True,''
          
          else:
              sqlinsertnewcust = "INSERT INTO customer (username, password, first_name, last_name, phone_no, email, street, baranggay,city, province, region, country, zip_code,admin,profession) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
              print(sqlinsertnewcust)
              modifydatabase(sqlinsertnewcust,[username, password1, firstname, lastname, phonenumber, email, street, brgy_val,city, province, region, country, zipcode,False, profession])
              raise PreventUpdate    
           
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

@app.callback(
    Output('number-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('number-in', 'value')])
def output(n_clicks, number):
    if n_clicks:
        sql = "SELECT * FROM roi_parameters"
             
        df = querydatafromdatabase(sql,["scenario_name","total_hits","conv_rate","rev_per_purchase","no_times_purchase","sampling_cost","percent_potential_rev"])
        sqlinsert = "INSERT INTO roi_parameters(scenario_name,total_hits,conv_rate,rev_per_purchase,no_times_purchase,sampling_cost,percent_potential_rev ) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        modifydatabase(sqlinsert, ['Scenario 3', 10000,1,2,3,4,5])
        
        sql = "SELECT * FROM roi_parameters"
        df = querydatafromdatabase(sql,["scenario_name","total_hits","conv_rate","rev_per_purchase",
                                              "no_times_purchase","sampling_cost","percent_potential_rev"])
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict("rows")      
        return [data,columns,0]
        print(df)
    return number

    print(df)


    sqlinserttrans = "INSERT INTO transactions (customer_id, total, isbn_list, quantity_list, sub_total_list) VALUES (%s,%s,%s,%s,%s);"
          print(sqlinserttrans)
          modifydatabase(sqlinserttrans,[custid, total,isbn_list, quantity_list, sub_total_list])
                  