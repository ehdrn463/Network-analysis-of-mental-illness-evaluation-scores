import dash
import dash_bootstrap_components as dbc

# Sharing Callback Output doesn't work
# https://community.plotly.com/t/multiple-callbacks-for-an-output/51247
# from dash_extensions.enrich import DashProxy, MultiplexerTransform

# app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
