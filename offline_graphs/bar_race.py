import plotly.graph_objects as go
import pandas as pd
import numpy as np 
from numpy import random
import plotly.io as pio
def label_to_color(names, r_min=0, r_max=255, g_min=0, g_max=255, b_min=0, b_max=255):
    mapping_colors = dict()
    
    for name in names.unique():
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = 'rgb({}, {}, {})'.format(red, green, blue)
    
        mapping_colors[name] = rgb_string
    
    return mapping_colors


def get_top_10(df, date, col='deceased'):
    tdata = df[df['date'] == date]
    fdata = tdata.sort_values(by=col, ascending=False)[:10]
    return fdata

pio.templates.default = "simple_white"

data = pd.read_csv('../data/COVID_Global_Timeseries.csv')

min_date = data['date'].min()
max_date = data['date'].max()
list_of_dates = data['date'].unique().tolist()

global_code_color = label_to_color(data['countrycode'], 0, 255, 0, 255, 0, 255)
global_with_color = data.copy()
global_with_color['color'] = global_with_color['countrycode'].map(global_code_color)


def make_bar_chart(dataset, col_name, frame_rate = 1):
    list_of_frames = []
    for date in list_of_dates:
        pdata = get_top_10(dataset, date)
        list_of_frames.append(go.Frame(data = [go.Bar(x = pdata["countrycode"], y = pdata[col_name],
                                            marker_color = pdata["color"], text = pdata["countrycode"],
                                            hoverinfo = "none",textposition = "outside",
                                            texttemplate = "%{x}<br>%{y:s}",cliponaxis = False)],
                                layout = go.Layout(
                                    font = {"size":20},
                                    height = 700,
                                    xaxis = {"showline":False,"tickangle":-90, "visible":False},
                                    yaxis = {"showline":False, "visible":False},
                                title = f"{col_name}" + " as on: "+ str(date))))

    fData = get_top_10(dataset, min_date)
    
    fig = go.Figure(
    data = [go.Bar(x = fData["countrycode"], y = fData[col_name],
                   marker_color = fData["color"],text = fData["countrycode"],
                  hoverinfo = "none",textposition = "outside",
                   texttemplate = "%{x}<br>%{y:s}",cliponaxis = False)],
    layout=go.Layout(
        title=f"{col_name}" + " as on: "+str(min_date),
        font = {"size":20},
        height = 700,
        xaxis = {"showline":False,"tickangle":-90, "visible":False},
        yaxis = {"showline":False, "visible":False},
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames=list(list_of_frames)
    )
    fig.show()
make_bar_chart(global_with_color, col_name='confirmed')
