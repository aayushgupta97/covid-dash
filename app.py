import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import pandas as pd
import plotly.graph_objects as go

### Getting data for api.covid API and making dataframe
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

app = dash.Dash()

app.layout = html.Div([

    html.Div([
        dcc.Graph(id="my-line-plot",
                    figure={
                        "data": data,
                        "layout": go.Layout(title="Total Cases", hovermode="closest")
                    })
    ],
    style={"width": "40%", "align": "left"})


])

if __name__=="__main__":
    app.run_server()