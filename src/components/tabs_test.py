import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px 
from . import ids, data


def tabs(app: Dash):
    @app.callback(
    Output(ids.TABS_EXAMPLE_CONTENT, 'children'),
    Input(ids.TABS_EXAMPLE_1, 'value')
    )

    def render_content(tab):
            if tab == 'tab-1-example-graph':
                return html.Div([
                    html.H3('Tab content 1'),
                    dcc.Graph(
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }]
                        }
                    )
                ])
            elif tab == 'tab-2-example-graph':
                return html.Div([
                    html.H3('Tab content 2'),
                    dcc.Graph(
                        id='graph-2-tabs-dcc',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [5, 10, 6],
                                'type': 'bar'
                            }]
                        }
                    )
                ])
    return html.Div(id=ids.TABS_EXAMPLE_CONTENT)
