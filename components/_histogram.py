from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor= 'rgba(0, 0, 0, 0)'
)

row_style = {'height': '20vh'}

histogram = dbc.Row( 
    dcc.Graph(id='map-histogram', figure=fig),
    style= row_style
)