from dash.dependencies import Input, Output
from app import app, cache
from plotly.subplots import make_subplots
from src.plots import *
from src.constant_data import country_code_to_name, india_state_code_mapping
from src.utils import *
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

FIRST_RUN = True
### Read Data
## India
# confirmed_daily = pd.read_csv("data/daily/confirmed.csv")
# confirmed_cm = pd.read_csv("data/cumulative/confirmed.csv")
# deceased_daily = pd.read_csv("data/daily/deceased.csv")
# deceased_cm = pd.read_csv("data/cumulative/deceased.csv")
# recovered_daily = pd.read_csv("data/daily/recovered.csv")
# recovered_cm = pd.read_csv("data/cumulative/recovered.csv")

# state_subplot_title = tuple(state['label'] for state in india_state_code_mapping)
# state_column_codes = [state['value'] for state in india_state_code_mapping]

# ## World
# global_timeseries = pd.read_csv("data/COVID_Global_Timeseries.csv")
# countrywise_total = pd.read_csv("data/COVID_countrywise_total_data.csv")
# # top_6 = countrywise_total.sort_values('confirmed', ascending=False).iloc[:6]
# country_1 = pd.read_csv("data/top_6_timeseries/country_1.csv")
# country_2 = pd.read_csv("data/top_6_timeseries/country_2.csv")
# country_3 = pd.read_csv("data/top_6_timeseries/country_3.csv")
# country_4 = pd.read_csv("data/top_6_timeseries/country_4.csv")
# country_5 = pd.read_csv("data/top_6_timeseries/country_5.csv")
# country_6 = pd.read_csv("data/top_6_timeseries/country_6.csv")

# top_6_list = [country_1, country_2, country_3, country_4, country_5, country_6]

# global_code_color = label_to_color(global_timeseries['countrycode'], 0, 255, 0, 255, 0, 255)
# global_with_color = global_timeseries.copy()
# global_with_color['color'] = global_with_color['countrycode'].map(global_code_color)
from get_data import execute_all

state_subplot_title = tuple(state['label'] for state in india_state_code_mapping)
state_column_codes = [state['value'] for state in india_state_code_mapping]
def get_new_data():
    """
    updates the global_timeseries data.
    """
    global FIRST_RUN ,global_timeseries, countrywise_total, confirmed_daily, confirmed_cm,\
    deceased_daily, deceased_cm, recovered_daily, recovered_cm, country_1,\
    country_2, country_3, country_4, country_5, country_6, top_6_list,\
    global_code_color, global_with_color, df_index_small_plot
    
    ## Will not collect data on initial app run
    if not FIRST_RUN:
        execute_all()

    confirmed_daily = pd.read_csv("data/daily/confirmed.csv")
    confirmed_cm = pd.read_csv("data/cumulative/confirmed.csv")
    deceased_daily = pd.read_csv("data/daily/deceased.csv")
    deceased_cm = pd.read_csv("data/cumulative/deceased.csv")
    recovered_daily = pd.read_csv("data/daily/recovered.csv")
    recovered_cm = pd.read_csv("data/cumulative/recovered.csv")

    ## World
    global_timeseries = pd.read_csv("data/COVID_Global_Timeseries.csv")
    countrywise_total = pd.read_csv("data/COVID_countrywise_total_data.csv")
    # top_6 = countrywise_total.sort_values('confirmed', ascending=False).iloc[:6]
    country_1 = pd.read_csv("data/top_6_timeseries/country_1.csv")
    country_2 = pd.read_csv("data/top_6_timeseries/country_2.csv")
    country_3 = pd.read_csv("data/top_6_timeseries/country_3.csv")
    country_4 = pd.read_csv("data/top_6_timeseries/country_4.csv")
    country_5 = pd.read_csv("data/top_6_timeseries/country_5.csv")
    country_6 = pd.read_csv("data/top_6_timeseries/country_6.csv")

    top_6_list = [country_1, country_2, country_3, country_4, country_5, country_6]

    global_code_color = label_to_color(global_timeseries['countrycode'], 0, 255, 0, 255, 0, 255)
    global_with_color = global_timeseries.copy()
    global_with_color['color'] = global_with_color['countrycode'].map(global_code_color)
    df_index_small_plot = global_timeseries.groupby(['date']).sum().reset_index()
    FIRST_RUN = False
    

def get_new_data_every(period=3600):
    """
    update the data every 'period' seconds
    """
    while True:
        get_new_data()
        print("data has been updated")
        time.sleep(period)
executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_data_every)

### Modify data for index plots


###### ***************************************************************** ######

### India Callbacks
@app.callback(Output("statewise_subplot", "figure"),
            [Input("demo-dropdown", "value"),
            Input("type-dropdown", "value")])
@cache.memoize(timeout=1200)
def update_subplot(column_name, plot_type):
    # fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    if plot_type == "cm":
        confirmed, deceased, recovered = get_cm_subplot(column_name, confirmed_cm, deceased_cm, recovered_cm)
    else:
        confirmed, deceased, recovered = get_daily_subplot(column_name,confirmed_daily, deceased_daily, recovered_daily)
    # fig.append_trace(confirmed, row=1, col=1)

    # fig.append_trace(deceased, row=2, col=1)

    # fig.append_trace(recovered, row=3, col=1)
    # fig.update_layout(height=600, title_text="Statewise Statistics")

    return {
        "data": [confirmed, deceased, recovered],
        "layout" : {"title": "Statewise Statistics", "barmode": "stack",
                    "xaxis": {"title": "Timeline", "tickangle":"-45", "nticks": "30"}, "yaxis": {"title": "Count"}}
    }

@app.callback(Output("all_state_subplot", "figure"),
        [Input("all_state_subplot_scale", "value")])
@cache.memoize(timeout=1200)
def update_state_subplot(graph_scale):
    state_columns = state_column_codes
    fig = make_subplots(rows=10, cols=4, 
            subplot_titles=state_subplot_title, shared_xaxes=False)

    row = 1
    col= 1
    for code in state_columns:
        fig.append_trace(go.Scatter(x=confirmed_cm['date'], y=confirmed_cm[code], mode="lines", showlegend=False), row=row, col=col)
        fig.update_yaxes(showgrid=False, row=row, col=col, type=graph_scale, tickvals=[1,20,400,8000, 80000])
        fig.update_xaxes(showticklabels=False)

        col = col + 1
        if col > 4:
            row = row + 1
            col = 1

    fig.update_layout(height=1500, title_text= "State wise plots to see the growth and if the curve flattens",
       paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    return fig

###### ***************************************************************** ######
### World Callback
@app.callback(Output("main_world_plot", "figure"),
[Input("country_drop_down", "value"),
Input("world_plot_time", "value"),
Input("world_plot_scale", "value")])
@cache.memoize(timeout=1200)
def update_world_plot(country_list, time_from, scale_type):
    idx = -1 * time_from
    traces = []
    for country in country_list:
        df_plot = global_timeseries[global_timeseries['countrycode'] == country]
        traces.append(dict(x=df_plot['date'][idx:],
                                y=df_plot["confirmed"][idx:],
                                mode='markers+lines',
                                opacity=0.9,
                                name=country_code_to_name[country]
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
                    "title": "Confirmed"
                }

        )
    }


@app.callback(Output("top_6_subplot", "figure"),
            [Input("top_6_tab", "value")])
@lru_cache(maxsize=32)
@cache.memoize(timeout=1200)
def update_top_6_subplot(plot_type):
    fig = make_subplots(rows=2, cols=3, 
                subplot_titles=(country_1['country'][0],
                country_2['country'][0],
                country_3['country'][0],
                country_4['country'][0],
                country_5['country'][0],
                country_6['country'][0]), shared_xaxes=True)

    row = 1
    col = 1
    for df in top_6_list:
        if plot_type == 'cm':
            fig.append_trace(go.Scatter(x=df['date'], y=df['total_cases'], mode="lines", name=f"Total: {df['total_cases'][df.index[-1]]:,d}"), row=row, col=col)
        else:
            fig.append_trace(go.Bar(x=df['date'], y=df['new_daily_cases'], name=f"Weekly Avg: {round(df['new_daily_cases'][-7:].sum()/7):,.2f}"), row=row, col=col)
        col = col + 1
        if col > 3:
            row = row + 1
            col = 1

    initial_range = [country_1['date'][country_1.index[-14]], country_1['date'][country_1.index[-1]]]
    print(initial_range)
    fig.update_layout(height=600, title_text="Countries with most Confirmed cases", xaxis4={"rangeslider":{"visible" :True},
                                                                                                 "range": initial_range},xaxis5={"rangeslider":{"visible" :True},
                                                                                                 "range": initial_range},xaxis6={"rangeslider":{"visible" :True},
                                                                                                 "range": initial_range})


    return fig

@app.callback(Output("race-chart-figure", "figure"),
            [Input("race-chart-dropdown", "value")])
def update_Race_chart(dd_value):
    title = f'Number of {dd_value} on '
    list_of_frames = frames_animation(global_with_color, title)
    fig = bar_race_plot(global_with_color, title, list_of_frames)
    return fig


###### ***************************************************************** ######
### Index Callback
@app.callback(Output("total_small_confirmed_plot", "figure"),
[Input("radio_small_confirmed_plot", "value")])
def update_total_small_plot(graph_scale):
    df_plot = df_index_small_plot.groupby(['date']).sum().reset_index()
    trace = [go.Scatter(x=df_plot['date'],
                        y=df_plot['confirmed'],
                        mode="lines",
                        name="Confirmed")]

    return {
        "data": trace,
        "layout": dict(
            title=f"Last updated on {df_plot['date'][df_plot.index[-1]]}",
            yaxis={"type": graph_scale}
        )
    }


@app.callback(Output("total_small_deceased_plot", "figure"),
[Input("radio_small_deceased_plot", "value")])
def update_total_small_plot(graph_scale):
    df_plot = df_index_small_plot.groupby(['date']).sum().reset_index()
    trace = [go.Scatter(x=df_plot['date'],
                        y=df_plot['deceased'],
                        mode="lines",
                        name="Deaths")]

    return {
        "data": trace,
        "layout": dict(
            title=f"Last updated on {df_plot['date'][df_plot.index[-1]]}",
            yaxis={"type": graph_scale}
        )
    }




@app.callback([Output("lg_item1_card1", "children"),
Output("lg_item2_card1", "children"),
Output("lg_item3_card1", "children"),
Output("lg_item1_card2", "children"),
Output("lg_item2_card2", "children"),
Output("lg_item3_card2", "children")],
[Input("index_tabs", "value")])
def update_lg_item1_card1(col_code):
    return (f"Confirmed: {countrywise_total['confirmed'][countrywise_total['code'] == col_code].iloc[0]:,d}",
    f"Recovered: {countrywise_total['recovered'][countrywise_total['code'] == col_code].iloc[0]:,d}",
    f"Deaths: {countrywise_total['deaths'][countrywise_total['code'] == col_code].iloc[0]:,d}",
    f"Active: {countrywise_total['active'][countrywise_total['code'] == col_code].iloc[0]:,d}",
    f"Cases Today: {countrywise_total['cases_today'][countrywise_total['code'] == col_code].iloc[0]:,d}",
    f"Deaths Today: {countrywise_total['deaths_today'][countrywise_total['code'] == col_code].iloc[0]:,d}")


# @app.callback(Output("lg_item1_card1", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Confirmed: {countrywise_total['confirmed'][countrywise_total['code'] == col_code].iloc[0]:,d}"

# @app.callback(Output("lg_item2_card1", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Recovered: {countrywise_total['recovered'][countrywise_total['code'] == col_code].iloc[0]:,d}"

# @app.callback(Output("lg_item3_card1", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Deaths: {countrywise_total['deaths'][countrywise_total['code'] == col_code].iloc[0]:,d}"

# @app.callback(Output("lg_item1_card2", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Active: {countrywise_total['active'][countrywise_total['code'] == col_code].iloc[0]:,d}"

# @app.callback(Output("lg_item2_card2", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Cases Today: {countrywise_total['cases_today'][countrywise_total['code'] == col_code].iloc[0]:,d}"

# @app.callback(Output("lg_item3_card2", "children"),
#             [Input("index_tabs", "value")])
# def update_lg_item1_card1(col_code):
#     return f"Deaths Today: {countrywise_total['deaths_today'][countrywise_total['code'] == col_code].iloc[0]:,d}"

