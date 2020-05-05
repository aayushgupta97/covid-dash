import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from src.plots import get_line_plot_data, get_bar_plot, get_gender_plot, get_age_hist, get_subplot
from src.utils import *
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Reading Data
national_timeseries = pd.read_csv("./data/covid_national_timeseries.csv")
gender_age_data = pd.read_csv("data/covid_raw_gender_age_full.csv")
statewise_total_cases = pd.read_csv("data/covid_statewise_total_cases.csv")
confirmed_daily = pd.read_csv("data/daily/confirmed.csv")
deceased_daily = pd.read_csv("data/daily/deceased.csv")
recovered_daily = pd.read_csv("data/daily/recovered.csv")

# Defining Plots
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
    dbc.Col(dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Maharashtra', 'value': 'mh'},
            {'label': 'Delhi', 'value': 'dl'},
            {'label': 'Rajasthan', 'value': 'rj'}
        ],
        value='dl'
    )),
    dcc.Graph(id = "statewise_subplot", figure=fig)
])



app.layout = dbc.Container([
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

#### Callback Functions
@app.callback(Output("statewise_subplot", "figure"),
            [Input("demo-dropdown", "value")])
def update_subplot(column_name):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

    confirmed, deceased, recovered = get_subplot(column_name,confirmed_daily, deceased_daily, recovered_daily)
    fig.append_trace(confirmed, row=1, col=1)

    fig.append_trace(deceased, row=2, col=1)

    fig.append_trace(recovered, row=3, col=1)
    fig.update_layout(height=600, title_text="Statewise Statistics")

    return fig

if __name__=="__main__":
    app.run_server()