# importing dependencies
import pandas as pd
import dash
from dash import Dash, dcc, html
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from . import ids, data
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# importing data 
baseball = pd.read_csv("fixed_location.csv")
players = baseball['Pitcher'].unique()
player_default = baseball['Pitcher'][0]

DEBUG = True 

# the locations map already has a defined x, and y
# z and players can be chosen from
def locations_map(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.HEATMAP_LOCATIONS, "children"),
        Input(ids.DROPDOWN_PLAYERS, 'value'),
        Input(ids.DROPDOWN_ATTRIBUTES_Z, 'value')
    )
    def update_locations_heatmap(dropdown_pitcher, dropdown_attrZ) -> html.Div:
        if dropdown_pitcher:
            # value filtering
            heatmap_data = data.BASEBALL_LOCATIONS[(data.BASEBALL_LOCATIONS['Pitcher'] == dropdown_pitcher)][dropdown_attrZ]

            graph = go.Heatmap(
                    x = baseball['Location_Side'],
                    y = baseball['Location_Height'],
                    z = dropdown_attrZ,
                    name = "heatmap", 
                    colorscale = 'teal', 
                    xgap = 2,
                    ygap = 2
                )

            # add the headmap structure
            fig = go.Figure()

            # adding heatmap into figure
            fig.add_trace(graph)

            fig.update_xaxes(type='category')
            fig.update_yaxes(type='category')

            fig.update_layout(
                xaxis = {'title': 'Side distance',
                            'visible': True,
                            'showticklabels': False,
                            'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right']
                        },
                yaxis = {'title': 'Height distance',
                            'visible': True,
                            'showticklabels': False,
                            'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper']
                        },
                title=f'Heatmap of Pitcher {dropdown_pitcher.upper()}',
                # margin={"t": 5, "b": 30, "r": 20},
                width = 800,
                height = 800
            )

            # adding black square on heatmap
            fig.add_shape(type="rect",
                        x0=0.5, y0=0.5, x1=3.5, y1=3.5,
                        line=dict(color="orange", width = 7),
                        ),


