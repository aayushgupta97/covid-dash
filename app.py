import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Caching with FileSystem instead of Redis.
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})
app.config.suppress_callback_exceptions = True