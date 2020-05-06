import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from src.plots import *
from src.utils import *


national_timeseries = pd.read_csv("./data/covid_national_timeseries.csv")
gender_age_data = pd.read_csv("data/covid_raw_gender_age_full.csv")
statewise_total_cases = pd.read_csv("data/covid_statewise_total_cases.csv")

line_plot_total_cases = html.Div([
        dcc.Graph(id="my-line-plot",
                    figure={
                        "data": get_line_plot_data(national_timeseries),
                        "layout": {"title": "Total Cases"}
                    })
    ])

bar_every_day_case = html.Div([
        dcc.Graph(id="my-bar-plot",
                    figure={
                        "data": get_bar_plot(national_timeseries),
                        "layout": {"title": "Bar - Daily new cases"}
                    })
    ])

histogram_age_distribution = html.Div([
        dcc.Graph(id="my-histogram",
            figure={
                "data": get_age_hist(gender_age_data),
                "layout": {"title": "Age"}
            })
    ])

pie_gender = html.Div([
        dcc.Graph("my-pie-graph",
            figure={
                "data": get_gender_plot(gender_age_data),
                "layout":{"title":"Gender"}
            })
            ])


statewise_total_table = html.Div(dbc.Table.from_dataframe(sort_dataframe_desc_on_int_column("confirmed", get_dataframe_with_columns(["active", "confirmed", "deaths", "state"], statewise_total_cases)), striped=True, bordered=True, hover=True))

fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

statewise_subplots = html.Div([
    dbc.Col([dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Maharashtra', 'value': 'mh'},
            {'label': 'Delhi', 'value': 'dl'},
            {'label': 'Rajasthan', 'value': 'rj'}
        ],
        value='dl'
    ),     
    dcc.Dropdown(
        id="type-dropdown",
        options=[
            {"label": "Daily", "value":"daily"},
            {"label": "Cumulative", "value": "cm"}
        ],
        value='daily'
    )
    ], 
    ),
    dcc.Graph(id = "statewise_subplot", figure=fig)
])



layout_india = dbc.Container([
dbc.Row([
    dbc.Col(line_plot_total_cases),
    dbc.Col(bar_every_day_case)
]),
dbc.Row([
    dbc.Col(histogram_age_distribution),
    dbc.Col(pie_gender)
]),
dbc.Row([
    dbc.Col(statewise_total_table, width=4),
    dbc.Col(statewise_subplots)
])
])   



layout_world = dbc.Container([])
index = html.Div([])