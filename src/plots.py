import requests
import pandas as pd
import plotly.graph_objects as go

INDEX_MARCH_1 = 31
"""
Each Function returns a data list, containing the traces used in plots.
"""

class QuickPlot:
    def __init__(self, starting_index=0):
        self.starting_index = starting_index
    
    def bar(self, df, x_col, y_col):
        data = [go.Bar(x=df[x_col][self.starting_index:], y=df[y_col][self.starting_index:])]
        return data
    

class QuickTrace:
    def __init__(self, starting_index=0):
        self.starting_index = starting_index 
    
    def bar_trace(self, df, x_col, y_col):
        return go.Bar(x=df[x_col][self.starting_index:], y=df[y_col][self.starting_index:])

    def scatter_trace(self, df, x_col, y_col, name=None):
        return go.Scatter(x=df[x_col][self.starting_index:],
                    y=df[y_col][self.starting_index:],
                    mode="lines",
                    name=name)
    

### Getting data for api.covid API and making dataframe
def get_line_plot_data(df):
    trace1 = go.Scatter(x=df['date'][INDEX_MARCH_1:],
                    y=df['totalconfirmed'][INDEX_MARCH_1:],
                    mode="lines",
                    name="Confirmed")
    trace2 = go.Scatter(x=df['date'][INDEX_MARCH_1:],
                    y=df['totaldeceased'][INDEX_MARCH_1:],
                    mode="lines",
                    name="Deceased")

    trace3 = go.Scatter(x=df['date'][INDEX_MARCH_1:],
                    y=df['totalrecovered'][INDEX_MARCH_1:],
                    mode="lines",
                    name="Recovered")

    line_plot_data = [trace1, trace2, trace3]
    return line_plot_data


def get_gender_plot(df):
    gender = df['gender']
    value_count = gender.value_counts()['M'] + gender.value_counts()['F']
    values = [gender.value_counts()['M'], gender.value_counts()['F']]
    data = [go.Pie(labels=["Male", "Female"] , values=values, textinfo="label+value+percent")]
    return data, value_count




def get_age_hist(df):
    age = df['age'].apply(lambda x: x if bool(x) else np.nan)
    age.dropna(inplace=True)
    data = [go.Histogram(x=age, nbinsx=20)]
    
    return data, len(age)


def quick_plot():
    pass


def get_bar_plot(df):    
    data = [go.Bar(x=df['date'][INDEX_MARCH_1:],y=df['dailyconfirmed'][INDEX_MARCH_1:])]
    return data


def get_daily_subplot(column_name, confirmed, deceased, recovered):
    trace1 = go.Bar(x=confirmed['date'], y=confirmed[column_name], name="confirmed")
    trace2 = go.Bar(x=deceased['date'], y=deceased[column_name], name="deceased")
    trace3 = go.Bar(x=recovered['date'], y=recovered[column_name], name="recovered")

    return trace1, trace2, trace3


def get_cm_subplot(column_name, confirmed, deceased, recovered):
    trace1 = go.Scatter(x=confirmed['date'], y=confirmed[column_name], mode="markers+lines", name="confirmed") 
    trace2 = go.Scatter(x=deceased['date'], y=deceased[column_name], mode="markers+lines", name="deceased") 
    trace3 = go.Scatter(x=recovered['date'], y=recovered[column_name], mode="markers+lines", name="recovered") 

    return trace1, trace2, trace3




def frames_animation(df, title):

    list_of_frames = []
    initial_date = df['date'].min()
    final_date = df['date'].max()
    list_of_dates = df['date'].unique().tolist()
    for date in list_of_dates:
            tdata = df[df['date'] == date]
            fdata = tdata.sort_values(by='confirmed', ascending=False)[:10]
            list_of_frames.append(go.Frame(data=[go.Bar(x=fdata['countrycode'], y=fdata['confirmed'],
                                                        marker_color=fdata['color'], hoverinfo='none',
                                                        textposition='outside', texttemplate='%{x}<br>%{y}',
                                                        cliponaxis=False)],
                                           layout=go.Layout(font={'size': 14},
                                                            plot_bgcolor = '#FFFFFF',
                                                            xaxis={'showline': False, 'visible': False},
                                                            yaxis={'showline': False, 'visible': False},
                                                            bargap=0.15,
                                                            title=title + str(date))))
    return list_of_frames 


def bar_race_plot (df, title, list_of_frames):

    
    # initial year - names (categorical variable), number of babies (numerical variable), and color
    initial_date = df['date'].min()
    tmp = df[df['date'] == initial_date]
    df = tmp.sort_values(by='confirmed', ascending=False)[:10]
    initial_names = df[df['date'] == initial_date].countrycode
    initial_numbers = df[df['date'] == initial_date].confirmed
    initial_color = df[df['date'] == initial_date].color
    range_max = df['confirmed'].max()
    
    fig = go.Figure(
        data=[go.Bar(x=initial_names, y=initial_numbers,
                       marker_color=initial_color, hoverinfo='none',
                       textposition='outside', texttemplate='%{x}<br>%{y}',
                       cliponaxis=False)],
        layout=go.Layout(font={'size': 14}, plot_bgcolor = '#FFFFFF',
                         xaxis={'showline': False, 'visible': False},
                         yaxis={'showline': False, 'visible': False, 'range': (0, range_max)},
                         bargap=0.15, title=title + str(initial_date),
                         updatemenus=[dict(type="buttons",
                                           buttons=[dict(label="Play",
                                                         method="animate",
                                                         args=[None,{"frame": {"duration": 2000, "redraw": True}, "fromcurrent": True}]),
                                                    dict(label="Stop",
                                                         method="animate",
                                                         args=[[None],{"frame": {"duration": 0, "redraw": False}, "mode": "immediate","transition": {"duration": 0}}])])]),
        frames=list(list_of_frames))
    
    return fig