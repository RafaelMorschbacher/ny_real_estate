from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
import math
import numpy as np
import dotenv
import os
from app import app

#===================
from components._histogram import histogram
from components._map import map
from components._controllers import controllers, slider_size
#===================
dotenv.load_dotenv()
mapbox_key = os.getenv('MAPBOX_KEY')
server = app.server
#============================================#
# DATA
#============================================#

#=================== read csv
df = pd.read_csv('dataset/cleaned_data.csv')

#=================== data treatment
df['SIZE M2'] = df['GROSS SQUARE FEET']/10.764

df = df[df['YEAR BUILT'] != 0]

df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])

df.loc[df['SIZE M2'] > 10000, 'SIZE M2'] = 10000
df.loc[df['SALE PRICE'] > 50000000, 'SALE PRICE'] = 50000000
df.loc[df['SALE PRICE'] < 10000, 'SALE PRICE'] = 10000

#=================== aux variables


#=================== aux functions

def get_sqr_feet_size(square_size_index):
       decimal_part = square_size_index % 1
       if decimal_part == 0:
              return slider_size[square_size_index]
       else:
              index_floor = slider_size[math.floor(square_size_index)]
              index_ceil = slider_size[math.ceil(square_size_index)]
        
              return index_floor + (decimal_part)*(index_ceil - index_floor)

# ============================================#
#  LAYOUT
# ============================================#

app.layout = dbc.Container(
        children=[
                dbc.Row(
                    [
                        dbc.Col([controllers], md=4),
                        dbc.Col([
                            map, histogram
                        ], md=8)
                        ]
                )
        ], fluid=True, )

# ============================================#
#  CALLBACKS
# ============================================#

#=================== map and histogram
@app.callback(
        Output('map-histogram', 'figure'),
        Output('map-graph', 'figure'),
        Input('district-dropdown', 'value'),
        Input('variable-dropdown', 'value'),
        Input('square-ft-slider', 'value'),
)

def update__hist_map(location, variable, square_size_index):
    
        #=================== dataframe filters
        if(location): 
                df_filtered = df[df['BOROUGH'] == location]
        else: 
                df_filtered = df.copy()

     
        square_size = get_sqr_feet_size(square_size_index)

        df_filtered = df_filtered[df_filtered['SIZE M2'] <= square_size]

        #=================== histogram

        fig_histogram = px.histogram(
        data_frame=df_filtered,
        x= variable,
        log_y= variable in ['SALE PRICE', 'TOTAL UNITS']
                )
        
        fig_histogram.update_layout(
                margin=go.layout.Margin(l=10, r=0, t=0, b=50),
                showlegend=False, 
                template="plotly_dark", 
                paper_bgcolor="rgba(0, 0, 0, 0)"
        )

        #=================== map

        px.set_mapbox_access_token(mapbox_key)

        fig_map = px.scatter_mapbox(
               data_frame= df_filtered,
               lat="LATITUDE", lon="LONGITUDE",
               color= variable,
               size="SIZE M2", size_max=20, zoom=10, opacity=0.4
        )
        avg_lat = df_filtered['LATITUDE'].mean()
        avg_lon = df_filtered['LONGITUDE'].mean()

        color_scale = px.colors.sequential.GnBu
        df_quantiles = df_filtered[variable].quantile(np.linspace(0, 1, len(color_scale))).to_frame()
        df_quantiles = round((df_quantiles - df_quantiles.min()) / (df_quantiles.max() - df_quantiles.min()) * 10000) / 10000
        df_quantiles.iloc[-1] = 1
        df_quantiles["colors"] = color_scale
        df_quantiles.set_index(variable, inplace=True)
        color_scale = [[i, j] for i, j in df_quantiles["colors"].items()]


        fig_map.update_coloraxes(colorscale=color_scale)


        fig_map.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=avg_lat, lon=avg_lon)), 
                template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)", 
                margin=go.layout.Margin(l=10, r=10, t=10, b=10))

        #=================== return outputs
        return [fig_histogram, fig_map]



if __name__ == '__main__':
    app.run_server(debug=False)