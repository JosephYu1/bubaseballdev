# importing dependencies
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff

# app layout design
app = dash.Dash(__name__)
# importing data 
baseball = pd.read_csv("fixed_location.csv")
players = baseball['Pitcher'].unique()
player_default = baseball['Pitcher'][0]

# graph structure 
graph = go.Heatmap(
            x = baseball['Location_Side'],
            y = baseball['Location_Height'],
            z = baseball['RelSpeed'],
            name = "heatmap", 
            colorscale = 'Viridis', 
            xgap = 2,
            ygap = 2
  )

""" graph.add_shape(
  type = 'rect',
  x0 = 'Left', 
  x1 = 'Right',
  y0 = 'Upper',
  y1 = 'Lower',
  line=dict(
    color='Black'
  ),
),
 """
layout = go.Layout(
              xaxis = {'title': 'Side distance',
                        'visible': True,
                        'showticklabels': False,
                        'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right']
                      },
              yaxis = {'title': 'Height distance',
                        'visible': True,
                        'showticklabels': False,
                        'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper']},
              margin={"t": 5, "b": 30, "r": 20},
              width = 1000,
              height = 600
          )

# divider for select player dropdown menu
app.layout = html.Div([
 html.H1("Baseball Analytics"),
  # divider for the heatmap graph
  html.Div([
    html.H4('Heatmap of relative speed per location'),
      dcc.Graph(
        id = 'heatmap', 
        figure = {
        'data': [go.Heatmap(
            x = baseball['Location_Side'],
            y = baseball['Location_Height'],
            z = baseball['RelSpeed'],
            name = "heatmap", 
            colorscale = 'Viridis', 
            xgap = 2,
            ygap = 2
        )],
        'layout': go.Layout(
              xaxis = {'title': 'Side distance',
                        'visible': True,
                        'showticklabels': False,
                        'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right']
                      },
              yaxis = {'title': 'Height distance',
                        'visible': True,
                        'showticklabels': False,
                        'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper']},
              margin={"t": 5, "b": 30, "r": 20},
              width = 1000,
              height = 600
          )
        }
      )
  ]),
])

if __name__ == '__main__':
 app.run_server(debug=True)
