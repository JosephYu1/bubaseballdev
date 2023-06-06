# TODO: fix graph not updating after selection!

# importing dependencies
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px 
from . import ids, data

# input
# BASEBALL = pd.read_csv(r"./data_combined/20230208-combined-running-index.csv") # NOTE: assume directory start at /capstone. rstring for literal input
# PLAYERS = BASEBALL['Pitcher'].unique()
players = data.PLAYERS_ALL # this is to keep the framework dynamic for updates, recall this is a ndarray of str!
player_default = data.BASEBALL_ALL['Pitcher'][0] # pick the first pitcher as default
df_default = data.BASEBALL_ALL[(data.BASEBALL_ALL['Pitcher'] == player_default)] # this is VERY important, as it gives a dataframe for use later
# NOTE: using a dataframe above is key. <players> are from the pd.unique() function gives a ndarray, which cannot be queried nor use with structure later.
# The subset of BASEBALL df gives also a dataframe that retains all the column names as well, instead of having to make new ones.

# Make data for merging later

print(data.BASEBALL_ALL.head(3).to_dict())

pitch_types = data.BASEBALL_ALL['TaggedPitchType']
pitch_calls = data.BASEBALL_ALL['PitchCall']

# working_data = []
# for i in pitch_types.unique():
#     for j in pitch_calls.unique():
#         working_data.append([i,j])
# working_data = pd.DataFrame(working_data, columns=['TaggedPitchType','PitchCall'])

def render(app: Dash) -> html.Div:
  # interactive update to dropdown
  @app.callback(
    Output(ids.HEATMAP_UPDATE, "children"),
    Input(ids.PLAYER_DROPDOWN, 'value')
  )

  # NOTE: the input is from the dropdown selection. It is currently a str, but needs to work with multiple players, which would be list[str]
  def update_heatmap(pitcher_dropdown): # -> html.Div
    heatmap_data = data.BASEBALL_ALL[(data.BASEBALL_ALL['Pitcher'] == pitcher_dropdown)][['TaggedPitchType','PitchCall','SpinRate']]
    # TODO: debug
    print(f'''pitcher_dropdown: {pitcher_dropdown}''')
    print(f'''\nheatmap_data before merge:\n{heatmap_data}''')

    # see: https://stackoverflow.com/questions/71549352/plotly-express-heatmap-using-pandas-dataframe
    new_df = heatmap_data.groupby(["TaggedPitchType","PitchCall"])["SpinRate"].median().reset_index() # using median instead of count()
    print(f'''\nnew_df after groupby:\n{new_df}''')
    new_df = new_df.pivot(index='TaggedPitchType', columns='PitchCall')['SpinRate'].fillna(0)
    print(f'''\nnew_df after restructure:\n{new_df}''')

    # ver 1
    # heatmap_data = pd.merge(working_data, heatmap_data, on=['TaggedPitchType', 'PitchCall'],how='outer').fillna(0)
    # print(f'''heatmap_data after:\n{heatmap_data}''')
    # maxsale = heatmap_data[heatmap_data['SpinRate']==heatmap_data['SpinRate'].max()]
    # maxsale = maxsale.reset_index()
    # print(maxsale)

    # ver 2
    # heatmap_data = pd.merge(working_data, heatmap_data, on=['TaggedPitchType', 'PitchCall'], how='left').fillna(0)
    # maxsale = heatmap_data.loc[heatmap_data['SpinRate'].idxmax()]

    # output figure using go.Figure library
    # fig = go.Figure(
    #   data = [go.Heatmap(
    #             x=heatmap_data['TaggedPitchType'],
    #             y=heatmap_data['PitchCall'],
    #             z=heatmap_data['SpinRate'],
    #             xgap = 2,
  	# 			      ygap = 2,
    #             colorscale='Viridis'
    #             )],
    #     layout = go.Layout(
    #          	title = f'HEATMAP OF PITCHER {pitcher_dropdown.upper()}'
    #         ),
    # )
    
    # If want to update on graph?
    # fig.add_trace(go.Heatmap(
    #             x=heatmap_data['TaggedPitchType'],
    #             y=heatmap_data['PitchCall'],
    #             z=heatmap_data['SpinRate'],
    #             colorscale='Viridis'
    #             ))
                
    # if just want to return the data directly
    # return {
    #     'data' : [go.Heatmap(
    #             x=heatmap_data['TaggedPitchType'],
    #             y=heatmap_data['PitchCall'],
    #             z=heatmap_data['SpinRate'],
    #             xgap = 2,
  	# 			      ygap = 2,
    #             colorscale='Viridis'
    #             )],
    #     'layout' : go.Layout(
    #          	title = f'HEATMAP OF PITCHER {pitcher_dropdown.upper()}'
    #         ),
    #       }

    # using px and return correctly
    fig = px.imshow(new_df)
    fig.update_layout(
            title=f'Heatmap of Pitcher {pitcher_dropdown.upper()}',
        )
    
    # Do NOT use this, tested for not working, even though the tutorial has id in the return.
    # return html.Div(
    #         dcc.Graph(figure=fig, id=ids.HEATMAP_UPDATE) 
    #     )

    # can be in html.Div or not, doesn't matter. But return html.Div is more compliant to coding standard.
    return dcc.Graph(figure=fig) # NOTE: for some reason, if also return the id here, the website will NOT auto update!
        
    
  return html.Div(id=ids.HEATMAP_UPDATE)