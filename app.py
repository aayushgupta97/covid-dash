import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from src.plots import get_line_plot_data, get_bar_plot, get_gender_plot
import pandas as pd
app = dash.Dash()

# Reading Data
national_timeseries = pd.read_csv("./data/covid_national_timeseries.csv")




app.layout = html.Div([

    html.Div([
        dcc.Graph(id="my-line-plot",
                    figure={
                        "data": get_line_plot_data(national_timeseries),
                        "layout": go.Layout(title="Total Cases", hovermode="closest")
                    })
    ],
    style={"width": "40%", "align": "left"}),

    html.Div([
        dcc.Graph(id="my-bar-plot",
                    figure={
                        "data": get_bar_plot(national_timeseries),
                        "layout": {"title": "Histogram"}
                    })
    ],
    style={"width": "40%", "float": "left"}),

    html.Div([
        dcc.Graph("my-pie-graph",
            figure={
                "data": get_gender_plot(),
                "layout":{"title":"Gender"}
            }
            )
            ],
            style={"width": "30%", "float": "right"})




])


#### Callback Functions


if __name__=="__main__":
    app.run_server()