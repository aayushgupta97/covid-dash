from dash.dependencies import Input, Output
from app import app
from plotly.subplots import make_subplots
from src.plots import *

### Read Data

## India
confirmed_daily = pd.read_csv("data/daily/confirmed.csv")
confirmed_cm = pd.read_csv("data/cumulative/confirmed.csv")
deceased_daily = pd.read_csv("data/daily/deceased.csv")
deceased_cm = pd.read_csv("data/cumulative/deceased.csv")
recovered_daily = pd.read_csv("data/daily/recovered.csv")
recovered_cm = pd.read_csv("data/cumulative/recovered.csv")

## World
global_timeseries = pd.read_csv("data/COVID_Global_Timeseries.csv")

### India Callbacks
@app.callback(Output("statewise_subplot", "figure"),
            [Input("demo-dropdown", "value"),
            Input("type-dropdown", "value")])
def update_subplot(column_name, plot_type):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    if plot_type == "cm":
        confirmed, deceased, recovered = get_cm_subplot(column_name, confirmed_cm, deceased_cm, recovered_cm)
    else:
        confirmed, deceased, recovered = get_daily_subplot(column_name,confirmed_daily, deceased_daily, recovered_daily)
    fig.append_trace(confirmed, row=1, col=1)

    fig.append_trace(deceased, row=2, col=1)

    fig.append_trace(recovered, row=3, col=1)
    fig.update_layout(height=600, title_text="Statewise Statistics")
    # changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # print(changed_id)

    return fig

### World Callback
@app.callback(Output("main_world_plot", "figure"),
[Input("country_drop_down", "value"),
Input("world_plot_time", "value"),
Input("world_plot_scale", "value")])
def update_world_plot(country_list, time_from, scale_type):
    idx = -1 * time_from
    traces = []
    for country in country_list:
        df_plot = global_timeseries[global_timeseries['countrycode'] == country]
        traces.append(dict(x=df_plot['date'][idx:],
                                y=df_plot["confirmed"][idx:],
                                mode='markers+lines',
                                opacity=0.9,
                                name=country
                        )
                )
    
    return {
            'data': traces,
            'layout': dict (
                # width=1280,
                height=800,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                        'rangeslider': {'visible':True},

                      },
                yaxis={
                    "type": scale_type,
                }

        )
    }


import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
### Index Page
ind = requests.get("https://api.thevirustracker.com/free-api?countryTotal=IN").json()

@app.callback(Output("india-card", "children"),
        [Input("interval-component", "n_intervals")])
def update_india_card(n):
    return dbc.CardBody(
            [   dbc.ListGroup([
                dbc.ListGroupItemHeading("India Today"),
                dbc.ListGroupItem(f"Total: {ind['countrydata'][0]['total_cases']}"),
                dbc.ListGroupItem(f"Deceased: {ind['countrydata'][0]['total_deaths']}"),
                dbc.ListGroupItem(f"New Cases Today: {ind['countrydata'][0]['total_new_cases_today']}"),
            ]),html.Hr(),
                dcc.Link(dbc.Button("More India Stats", color="warning"), href="/india")
            ]
    )