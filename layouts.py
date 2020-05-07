import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from src.plots import *
from src.utils import *
from src.constant_data import currently_present_in_api_country

navbar = dbc.NavbarSimple(id="navbar",
            children=[
                dbc.NavItem(dbc.NavLink("India", href="/india")),
                dbc.NavItem(dbc.NavLink("World", href="/world")),
            ],
            brand= "Covid-Dash",
            brand_href="/",
            color="primary",
            dark="True",
            sticky="top"
            )


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

world_plot_scale = dcc.RadioItems(
    id="world_plot_scale",
    options=[
        {'label': 'Logarithmic', 'value': 'log'},
        {'label': 'Linear Scale', 'value': 'lin'},
    ],
    value='lin'
)  

world_plot_time = dcc.Dropdown(
    id="world_plot_time",
    options=[{"label": "All", "value": 0},
            {"label": "2 Months", "value": 60},
            {"label": "1 Month", "value": 30},
            {"label": "2 Weeks", "value": 14}
    ],
    value=60
)


country_selection_dropdown = dcc.Dropdown(
        id='country_drop_down',
        options=currently_present_in_api_country,
        value=['IN','IT'], # which are pre-selected
        multi=True
    )
world_plot = dcc.Graph(figure=go.Figure(), id='main_world_plot')

layout_world = dbc.Container([
    html.Br(),
    dbc.Row([dbc.Col(country_selection_dropdown, width=9),
             dbc.Col(world_plot_time, width=3)]),

    dbc.Row([
        dbc.Col(world_plot, width = 10),
        dbc.Col(html.Div(world_plot_scale, style={"margin-top": "40px"}), width=2),        
    ])
])

# import requests
# r = requests.get('https://api.thevirustracker.com/free-api?global=stats').json()

# homepage_card = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 dbc.ListGroup(
#     [
#         dbc.ListGroupItemHeading("Today's Update: "),
#         dbc.ListGroupItem(f"New Cases Today: {r['results'][0]['total_new_cases_today']}"),
#         dbc.ListGroupItem(f"Deaths Today: {r['results'][0]['total_new_deaths_today']}"),
#         dbc.ListGroupItem(f"Current Active Cases: {r['results'][0]['total_active_cases']}"),
#     ]
# ),html.Hr(),

#                 dcc.Link(dbc.Button("More World Stats", color="danger"), href="/world")
#             ]
#         ),
#     ],
#     # style={"width": "18rem"},
# )

# homepage_card_2 = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 dbc.ListGroup(
#     [
#         dbc.ListGroupItemHeading("World Totals: "),
#         dbc.ListGroupItem(f"Total: {r['results'][0]['total_cases']}"),
#         dbc.ListGroupItem(f"Deceased: {r['results'][0]['total_deaths']}"),
#         dbc.ListGroupItem(f"Recovered: {r['results'][0]['total_recovered']}")
#     ]
# ), html.Hr(),

#                 dcc.Link(dbc.Button("More World Stats", color="danger"), href="/world")
#             ]
#         ),
#     ],
#     # style={"width": "18rem"},
# )



# ind = requests.get("https://api.thevirustracker.com/free-api?countryTotal=IN").json()
# india_card = dbc.Card(
#     [
#         dbc.CardBody(
#             [   dbc.ListGroup([
#                 dbc.ListGroupItemHeading("India Today"),
#                 dbc.ListGroupItem(f"Total: {ind['countrydata'][0]['total_cases']}"),
#                 dbc.ListGroupItem(f"Deceased: {ind['countrydata'][0]['total_deaths']}"),
#                 dbc.ListGroupItem(f"New Cases Today: {ind['countrydata'][0]['total_new_cases_today']}"),
#             ]),html.Hr(),
#                 dcc.Link(dbc.Button("More India Stats", color="warning"), href="/india")
#             ]
#         ),
#     ],
#     # style={"width": "18rem"},
# )

# india_card = dbc.Card(
#     [
#         dbc.CardBody(id="india-card"),
#         dcc.Interval(
#             id='interval-component',
#             interval=1000*1000, # in milliseconds
#             n_intervals=0
#         )

 
#     ]
# )

card1 = dbc.Card(
    [
        dbc.CardHeader(html.H3("Confirmed")),
        dbc.CardBody([dcc.RadioItems(id="radio_small_confirmed_plot",
    options=[
        {'label': 'Logarithmic', 'value': 'log'},
        {'label': 'Linear Scale', 'value': 'lin'},
    ],
    value='lin'),
        dcc.Graph(id="total_small_confirmed_plot")])
    ]
)


card2 = dbc.Card(
    [
        dbc.CardHeader(html.H3("Deceased")),
        dbc.CardBody([dcc.RadioItems(id="radio_small_deceased_plot",
    options=[
        {'label': 'Logarithmic', 'value': 'log'},
        {'label': 'Linear Scale', 'value': 'lin'},
    ],
    value='lin'),
        dcc.Graph(id="total_small_deceased_plot")])
    ]
)

index = dbc.Container([
html.Br(), html.Hr(),
dbc.Row([
    dbc.Col(card1, width=6),
    dbc.Col(card2, width=6)
    # dbc.Col(homepage_card_2, width=4),
    # dbc.Col(india_card, width=4)
]),

    html.Div(html.A("Link to GitHub", href="https://github.com/aayushgupta97/covid-dash", style={"color": "white"}),
   style={
  "position": "fixed",
  "left": 0,
  "bottom": 0,
  "width": "100%",
  "background-color": "#007bff",
  "color": "white",
  "text-align": "center",
})
])