import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from src.plots import get_line_plot_data

app = dash.Dash()

app.layout = html.Div([

    html.Div([
        dcc.Graph(id="my-line-plot",
                    figure={
                        "data": get_line_plot_data(),
                        "layout": go.Layout(title="Total Cases", hovermode="closest")
                    })
    ],
    style={"width": "40%", "align": "left"})


])


#### Callback Functions


if __name__=="__main__":
    app.run_server()