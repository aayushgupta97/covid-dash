import requests
import pandas as pd
import plotly.graph_objects as go

INDEX_MARCH_1 = 31
"""
Each Function returns a data list, containing the traces used in plots.
"""


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
    values = [gender.value_counts()['M'], gender.value_counts()['F']]
    data = [go.Pie(labels=["Male", "Female"] , values=values)]
    return data


def get_age_hist(df):
    age = df['age'].apply(lambda x: x if bool(x) else np.nan)
    age.dropna(inplace=True)
    data = [go.Histogram(x=age, nbinsx=20)]
    return data


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