# importing dependencies
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import os

# app layout design
print(os.getcwd()) # TODO: delete this
app = dash.Dash(__name__)
# importing data 
baseball = pd.read_csv("./heatmap/fixed_location.csv") # <--- change to your correct data folder path!
players = baseball['Pitcher'].unique()
player_default = baseball['Pitcher'][0]


'''
HEATMAP STRUCTURE
'''
graph = go.Heatmap(
            x = baseball['Location_Side'],
            y = baseball['Location_Height'],
            z = baseball['RelSpeed'],
            name = "heatmap", 
            colorscale = 'icefire', 
            xgap = 2,
            ygap = 2
          )

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
      # margin={"t": 5, "b": 30, "r": 20},
      width = 800,
      height = 800
)

# adding black square on heatmap
fig.add_shape(type="rect",
              x0=0.5, y0=0.5, x1=3.5, y1=3.5,
              line=dict(color="purple", width = 7),
              ),


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
        figure = fig,
      )
  ]),
])

if __name__ == '__main__':
 
 app.run_server(debug=True)
