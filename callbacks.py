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


@app.callback(Output("main_world_plot", "figure"),
[Input("country_drop_down", "value")])
def update_world_plot(country_list):
    traces = []
    for country in country_list:
        df_plot = global_timeseries[global_timeseries['countrycode'] == country]
        traces.append(dict(x=df_plot['date'],
                                y=df_plot["confirmed"],
                                mode='markers+lines',
                                opacity=0.9,
                                name=country
                        )
                )
    
    return {
            'data': traces,
            'layout': dict (
                # width=1280,
                height=600,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

        )
    }