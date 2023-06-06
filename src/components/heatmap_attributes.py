# importing dependencies
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px 
from . import ids, data

# documentation on multiple callback:
# https://dash.plotly.com/advanced-callbacks
# https://plotly.com/python/heatmaps/

DEBUG = True

# input
players = data.PLAYERS_ALL # this is to keep the framework dynamic for updates, recall this is a ndarray of str!
player_default = data.BASEBALL_ALL['Pitcher'][0] # pick the first pitcher as default
df_default = data.BASEBALL_ALL[(data.BASEBALL_ALL['Pitcher'] == player_default)] # this is VERY important, as it gives a dataframe for use later

# Make data for merging later
# xvar = data.BASEBALL['TaggedPitchType']
# yvar = data.BASEBALL['PitchCall']

def render(app: Dash) -> html.Div:

  # interactive update to dropdown
  @app.callback(
    Output(ids.HEATMAP_ATTRIBUTES, "children"),
    Input(ids.RADIO_DATA, 'value'),
    Input(ids.DROPDOWN_PLAYERS, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_X, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Y, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Z, 'value')
  )
  # NOTE: the input is from the dropdown selection. It is currently a str, but needs to work with multiple players, which would be list[str]
  def update_heatmap(radio_option, dropdown_pitcher, dropdown_attrX, dropdown_attrY, dropdown_attrZ) -> html.Div:
    if radio_option == "All":
      cur_data = data.BASEBALL_ALL
      cur_players = data.PLAYERS_ALL
    elif radio_option == "Private":
      cur_data = data.BASEBALL_PRIVATE
      cur_players = data.PLAYERS_PRIVATE
    else:
      cur_data = data.BASEBALL_PUBLIC
      cur_players = data.PLAYERS_PUBLIC
    
    if DEBUG:
      print(cur_data.info())
      print(f'''pitcher_dropdown: {dropdown_pitcher}''')

    if dropdown_pitcher in cur_players: # sanitize input for not drawing when there's no players selected
      # this does the filtering
      heatmap_data = cur_data[(cur_data['Pitcher'] == dropdown_pitcher)][[dropdown_attrX, dropdown_attrY, dropdown_attrZ]]

      new_df = heatmap_data.groupby([dropdown_attrX, dropdown_attrY])[dropdown_attrZ].median().reset_index() # using median instead of count()
      new_df = new_df.pivot(index = dropdown_attrX, columns = dropdown_attrY)[dropdown_attrZ].fillna(0)

      # using plotly express to draw heatmap
      fig = px.imshow(new_df,
                labels = dict(x = dropdown_attrX, 
                              y = dropdown_attrY,
                              color = dropdown_attrZ),
                aspect = "auto",
                text_auto = False, # to turn on/off showing text on each cell
                )
      fig.update_layout(
              title=f'Heatmap of Pitcher {dropdown_pitcher.upper()} Based on Median Value of {radio_option.upper()} Data',
          )
      
      return html.Div(
              dcc.Graph(figure=fig)
          )
    else:
        return html.Div(
            [
              html.H4("Please select a player from the correct data."),
              html.H6("You are seeing this message because the player currently selected is not\nin the data group. i.e. John Smith has no Private data."),
            ]
              
          )
        
    
  return html.Div(id=ids.HEATMAP_ATTRIBUTES)