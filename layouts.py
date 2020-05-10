import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from src.plots import *
from src.utils import *
from src.constant_data import currently_present_in_api_country, india_state_code_mapping
import dash_table
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

## India
national_timeseries = pd.read_csv("./data/covid_national_timeseries.csv")
gender_age_data = pd.read_csv("data/covid_raw_gender_age_full.csv")
statewise_total_cases = pd.read_csv("data/covid_statewise_total_cases.csv")

## World
countrywise_total = pd.read_csv("data/COVID_countrywise_total_data.csv")

globalstats = pd.read_csv("data/globalstats.csv")

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

age_data, age_count = get_age_hist(gender_age_data)
histogram_age_distribution = html.Div([
        dcc.Graph(id="my-histogram",
            figure={
                "data": age_data,
                "layout": {"title": f"Age Distribution<br>Sample Size: {age_count}",
                
                "xaxis":{'title':'Age',
                        # 'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                },
                "yaxis": {"title": "Count"}
            }})
    ])

gender_data, gender_count = get_gender_plot(gender_age_data)
pie_gender = html.Div([
        dcc.Graph("my-pie-graph",
            figure={
                "data": gender_data,
                "layout":{"title": f"Gender Distribution<br>Sample Size: {gender_count}"}
            })
            ])


# statewise_total_table = html.Div(dbc.Table.from_dataframe(sort_dataframe_desc_on_int_column("confirmed", get_dataframe_with_columns(["active", "confirmed", "deaths", "state"], statewise_total_cases)), striped=True, bordered=True, hover=True))
country_processed_table_data = sort_dataframe_desc_on_int_column("confirmed", get_dataframe_with_columns(["active", "confirmed", "deaths", "state"], statewise_total_cases))

tb = dash_table.DataTable(data=country_processed_table_data.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in country_processed_table_data.columns],
                            # page_action='none',
    style_table={'height': '600px', 'overflowY': 'auto'},
    style_cell={
        # 'whiteSpace': 'normal',
        'height': 'auto',
        'textAlign': 'left'
    },
    css=[{'selector': '.row', 'rule': 'margin: 0'}])



# fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

statewise_subplots = html.Div([
    dbc.Col([dcc.Dropdown(
        id='demo-dropdown',
        options=india_state_code_mapping,
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
    ], width={"size": 4, "offset":4}
    ),
    dcc.Graph(id = "statewise_subplot")
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
html.Hr(),
dbc.Row([
    dbc.Col(tb, width={"size":6, "offset":3}),
]),
html.Hr(),
html.Br(),
dbc.Row(
    dbc.Col(statewise_subplots)
), html.Hr(),
dbc.Row(
    html.Div([dcc.RadioItems(
    id="all_state_subplot_scale",
    options=[
        {'label': 'Logarithmic', 'value': 'log'},
        {'label': 'Linear Scale', 'value': 'linear'},
    ],
    value='log'
),], style={"display": "none"})
),
dbc.Row(
    dbc.Col(dcc.Graph(id="all_state_subplot"), width=12)
)

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
        value=['IN','IT', 'RU', 'DE'], # which are pre-selected
        multi=True
    )
world_plot = dcc.Graph(figure=go.Figure(), id='main_world_plot')

top_6_subplot = html.Div([
    
    dcc.Tabs(id='top_6_tab', value='daily', children=[
        dcc.Tab(label='Daily', value='daily'),
        dcc.Tab(label='Cumulative', value='cm'),
    ]),
    dcc.Graph(id = "top_6_subplot")
])


layout_world = dbc.Container([
    html.Br(),
    dbc.Row([dbc.Col(country_selection_dropdown, width=9),
             dbc.Col(world_plot_time, width=3)]),

    dbc.Row([
        dbc.Col(world_plot, width = 10),
        dbc.Col(html.Div(world_plot_scale, style={"margin-top": "40px"}), width=2),        
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(top_6_subplot)
    ])
])


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
countrywise_total_table = html.Div(dbc.Table.from_dataframe(
    get_dataframe_with_columns(
        ["Country, Other", "Total Cases","New Cases", "Total Deaths", "New Deaths","Total Recovered","Active Cases", "Serious, Critical"],rename_columns_df({
        "confirmed": "Total Cases",
        "active": "Active Cases",
        "recovered": "Total Recovered",
        "deaths": "Total Deaths",
        "cases_today": "New Cases",
        "deaths_today": "New Deaths",
        "serious": "Serious, Critical",
        "country": "Country, Other"
    }, sort_dataframe_desc_on_int_column("confirmed", countrywise_total))),
      striped=True, bordered=True, hover=True), style={     
          "overflow": "scroll", 
          "height": "500px"
      })


global_first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(f"{globalstats['total_cases'][0]:,d} total cases", className="card-title"),
            html.P(f"of which {globalstats['total_active_cases'][0]:,d} are currently active and \
                {globalstats['total_recovered'][0]:,d} have recovered and {globalstats['total_deaths'][0]:,d} have died."),
            dcc.Link(dbc.Button("Go somewhere", color="primary"), href="/world"),
        ]
    )
)

index_tab_card1 = html.Div(
        dbc.Card([
        dbc.CardBody([  
             dbc.ListGroup([

                dbc.ListGroupItemHeading("Total"),
                dbc.ListGroupItem(f"Total: ", id="lg_item1_card1"),
                dbc.ListGroupItem(f"Deceased", id="lg_item2_card1"),
                dbc.ListGroupItem(f"New Cases Today: ", id="lg_item3_card1"),
            

             ], id="index_tab_card1")
            ])
        ])
)

index_tab_card2 = html.Div(dbc.Card([
        dbc.CardBody([  
             dbc.ListGroup([
                
                dbc.ListGroupItemHeading("Today"),
                dbc.ListGroupItem(f"Total: ", id="lg_item1_card2"),
                dbc.ListGroupItem(f"Deceased:", id="lg_item2_card2"),
                dbc.ListGroupItem(f"New Cases Today: ", id="lg_item3_card2"),
            
             ], id="index_tab_card2")
            ]),
    ])
)
index_tabs = html.Div([
    
    dcc.Tabs(id='index_tabs', value='W', children=[
        dcc.Tab(label='USA', value='US'),
        dcc.Tab(label='World', value='W'),
        dcc.Tab(label='INDIA', value='IN'),
    ]),

])



index = dbc.Container([
html.Br(), html.Hr(),
dbc.Row(
    [
        dbc.Col(index_tabs)
    ]), html.Br(),
dbc.Row([
    dbc.Col(index_tab_card1, width={"size":3, "offset": 3}),
    dbc.Col(index_tab_card2, width=3),

]), html.Hr(),
dbc.Row([
    dbc.Col(card1, width=6),
    dbc.Col(card2, width=6)

]),
html.Br(), html.Hr(), html.Br(),
    dbc.Row(
        dbc.Col(countrywise_total_table)
    ),


#     html.Div(html.A("Link to GitHub", href="https://github.com/aayushgupta97/covid-dash", style={"color": "white"}),
#    style={
#   "position": "fixed",
#   "left": 0,
#   "bottom": 0,
#   "width": "100%",
#   "background-color": "#007bff",
#   "color": "white",
#   "text-align": "center",
# })
])



# bar_chart_race =     dbc.Row([
#         dbc.Col(html.Div(
#         dcc.Dropdown(
#             id="race-chart-dropdown",
#         options=[
#             {"label": "Confirmed", "value":"confirmed"},
#             {"label": "Deceased", "value": "deceased"}
#         ],
#         value='confirmed'
#     ),), width=3),

#     dbc.Col(
#             dcc.Graph(id="race-chart-figure")
#     )       
#      ] )