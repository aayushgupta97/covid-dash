import callbacks
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os

from app import app
from layouts import layout_india, layout_world, navbar, index

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/india':
         return layout_india
    elif pathname == '/world':
         return layout_world
    else:
        return index

if __name__ == '__main__':
    # app.run_server(debug=False, port=8080)
    os.makedirs('cache', exist_ok=True)
    server.run(port=8080)