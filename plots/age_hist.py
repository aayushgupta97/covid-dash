import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo 

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

data = [trace1, trace2, trace3]
labels = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']

layout = go.Layout(title="total cases", hovermode="closest")
fig = go.Figure(data=data, layout=layout)


pyo.plot(fig)