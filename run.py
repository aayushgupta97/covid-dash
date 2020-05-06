import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


from app import app
from layouts import layout_india, layout_world
import callbacks

navbar = dbc.NavbarSimple(id="navbar",
            children=[
                dbc.NavItem(dbc.NavLink("India", href="/india")),
                dbc.NavItem(dbc.NavLink("World", href="/world")),
            ],
            brand= "Covid-Dash",
            brand_href="#",
            color="primary",
            dark="True",
            sticky="top"
            )


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
        return '404'

if __name__ == '__main__':
    app.run_server()