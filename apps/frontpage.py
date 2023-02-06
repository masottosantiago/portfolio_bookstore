# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc

from app import app

layout = html.Div([
      
             dcc.Link(
                
                 
          html.H1(children = html.Img(src=app.get_asset_url('journey1.png'), style = {'width':'70%','margin':1, 'padding':1}), 
                style = {'backgroundColor':'white', 'textAlign':'center','float':'center', 'margin':1, 'padding':1
                                                      }), 
           href='/login'),
    ])


