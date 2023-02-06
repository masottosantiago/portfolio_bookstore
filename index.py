import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import frontpage, login, signup, inventory, orderform, orderform1, pastorders, reports

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    html.Div([dcc.Store(id = 'user-login',storage_type = 'session')],style={'display':'none'}),
    html.Div([dcc.Store(id = 'cust-id',storage_type = 'session'),]),
     
    html.H1(children = html.Img(src=app.get_asset_url('banner.png'), style = {'width':'20%'}), 
                style = {'backgroundColor':'black', 'textAlign':'center','float':'center',
                                                    'margin':0, 'padding':0 }), 
    # content will be rendered in this element
 
    html.Div(id='page-content', children =[])
], style = {'margin':0})

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    
    if pathname == '/login':
        return login.layout
    elif pathname == '/signup':
        return signup.layout
    elif pathname == '/inventory':
        return inventory.layout
    elif pathname == '/orderform':
        return orderform.layout
    elif pathname == '/orderform1':
        return orderform1.layout
    elif pathname == '/pastorders':
        return pastorders.layout
    elif pathname == '/reports':
        return reports.layout
    else:
        return  frontpage.layout

if __name__ == '__main__':
    app.run_server()