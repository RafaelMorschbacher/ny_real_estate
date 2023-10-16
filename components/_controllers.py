from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from app import *

locations_dict = {
    0: "All",
    1: "Manhattan",
    2: "Bronx",
    3: "Brooklyn",
    4: "Queens",
    5: "Staten Island ",
}

slider_size = [100, 500, 1000, 10000, 10000000]

controllers = dbc.Row([
    html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), style={'width': '50%'}),
    html.H3("Real Estate Sales - NYC", style={'margin': '30px'}),
    html.P('This dashboard was made for the visualization of property sales in New York City'),
    html.Hr(),
    html.H4("District", style={'margin': '50px auto 25px'}),
    dcc.Dropdown(id='district-dropdown',
                 options=[{'value': i , 'label': j} for i,j in locations_dict.items()], 
                 value=0, clearable=False,
                 placeholder='Select a District'),
    html.H4("Square feet", style={'margin': '30px auto'}),
    dcc.Slider(
        id='square-ft-slider',
        min= 0,max=4, 
        marks= {i: {'label':str(j)} for i,j in enumerate(slider_size) },
        value=4
    ),
    html.H4("Variable for analysis", style={'margin': '30px auto'}),
    dcc.Dropdown(
                    options=[
                        {'label': 'YEAR BUILT', 'value': 'YEAR BUILT'},
                        {'label': 'TOTAL UNITS', 'value': 'TOTAL UNITS'},
                        {'label': 'SALE PRICE', 'value': 'SALE PRICE'},
                    ],
                    value='SALE PRICE',
                    clearable=False,
                    id="variable-dropdown")

], style={'padding': '10%'})
