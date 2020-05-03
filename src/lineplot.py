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