import requests
import pandas as pd
import plotly.graph_objects as go

### Getting data for api.covid API and making dataframe
def get_line_plot_data():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])
    trace1 = go.Scatter(x=df['date'][31:],
                    y=df['totalconfirmed'][31:],
                    mode="lines",
                    name="Confirmed")
    trace2 = go.Scatter(x=df['date'][31:],
                    y=df['totaldeceased'][31:],
                    mode="lines",
                    name="Deceased")

    trace3 = go.Scatter(x=df['date'][31:],
                    y=df['totalrecovered'][31:],
                    mode="lines",
                    name="Recovered")

    line_plot_data = [trace1, trace2, trace3]
    return line_plot_data


def get_gender_plot():
    r = requests.get("https://api.covid19india.org/raw_data1.json").json()
    gender = pd.DataFrame(r['raw_data'])['gender']
    values = [gender.value_counts()['M'], gender.value_counts()['F']]
    data = [go.Pie(labels=["Male", "Female"] , values=values)]
    return data


def get_age_hist():
    pass

def quick_plot():
    pass


def get_bar_plot():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])    
    data = [go.Bar(x=df['date'][31:],y=df['dailyconfirmed'][31:])]
    return data





