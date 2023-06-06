from cgi import print_directory
from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from data_calculations import *

import plotly.graph_objs as go
import plotly.express as px 

import numpy as np
import pandas as pd
import json

import data, ids, layouts

from app import app

DEBUG = False

# --------------------------
# --- Global functions -----
# --------------------------

'''
get_df_convert_dtype_datetime

1. Purpose:
   This function takes a DataFrame as input and converts specific columns to datetime data type. It checks if the DataFrame is not None and has at least one row before performing the conversion.

2. Inputs:
   - df_in: The DataFrame to be processed and have specific columns converted to datetime data type.
     State: The DataFrame should be a valid pandas DataFrame object.

3. Output:
   - df_in: The processed DataFrame with specific columns converted to datetime data type.
     State: It is the same DataFrame object with the specified columns converted to datetime data type.

'''
def get_df_convert_dtype_datetime(df_in):
    if df_in is not None and len(df_in) > 0:
        df_in["Date_datetime"] = pd.to_datetime(df_in["Date_datetime"])
        df_in["Datetime"] = pd.to_datetime(df_in["Datetime"])
    return df_in

'''
get_stored_data_from_vars

1. Purpose:
   This function retrieves data from stored DataFrames based on various input parameters such as match type, team selection, date range, player list, and pitch list. It dynamically filters the data based on the provided inputs and returns the filtered data as a dictionary.

2. Inputs:
   - matchtype_str: A string indicating the type of match (either "Public", "Private", or None).
     State: It should be a valid string value representing the match type.

   - team_select_list: A list of strings representing the selected teams. If "All" is present in the list, all teams are selected.
     State: It should be a valid list object containing team names as strings.

   - startDate: A string representing the start date of the desired date range.
     State: It should be a valid string representing a date.

   - endDate: A string representing the end date of the desired date range.
     State: It should be a valid string representing a date.

   - player_list: A list of strings representing the selected players. If "All" is present in the list, all players are selected.
     State: It should be a valid list object containing player names as strings.

   - pitch_list (optional): A list of strings representing the selected pitches. If "All" is present in the list, all pitches are selected. By default, it is an empty list.
     State: It should be a valid list object containing pitch names as strings.

3. Output:
   - curDF: A dictionary representation of the filtered DataFrame based on the input parameters.
     State: It is a dictionary containing the filtered data from the stored DataFrames.

'''

def get_stored_data_from_vars(matchtype_str, team_select_list, startDate, endDate, player_list, pitch_list = []):
    # handle which type of match
    if matchtype_str is None:
        PreventUpdate
    # change match type
    if matchtype_str == "Public":
        curDF = data.BASEBALL_PUBLIC_DF
    elif matchtype_str == "Private":
        curDF = data.BASEBALL_PRIVATE_DF
    else:
        curDF = data.BASEBALL_ALL_DF
    
    # handle the team selection
    if team_select_list is None:
        raise PreventUpdate
    if len(team_select_list) > 0 and "All" not in team_select_list:
        curDF = curDF.loc[curDF["PitcherTeam"].isin(team_select_list)]

    if startDate is None or endDate is None:
        raise PreventUpdate
    if startDate is not None and endDate is not None: 
        # check ordering, don't assume user will have the correct range order!
        # NOTE: the 'cool" thing is that if the Date_datetime column is an object/string, it'd still work, kinda
        if pd.to_datetime(startDate) <= pd.to_datetime(endDate):
            curDF = curDF.loc[curDF["Date_datetime"].between(
                        startDate,
                        endDate
                        )]
        else:
            curDF = curDF.loc[curDF["Date_datetime"].between(
                        endDate,
                        startDate
                        )]
    
    # this is important to prevent Key Error, since the player list is updated everytime there's a change to the data selection. 
    # Meaning that when we change from one team to another, the selection can be empty.
    if player_list is None: 
        PreventUpdate
    if len(player_list) > 0 and 'All' not in player_list:
        curDF = curDF.loc[curDF["Pitcher"].isin(player_list)]

    if pitch_list is None:
        PreventUpdate
    if len(pitch_list) > 0 and "All" not in pitch_list:
        curDF = curDF.loc[curDF["TaggedPitchType"] .isin(pitch_list)]

    return curDF.to_dict()

'''
get_updated_dict_list Comment:

1. Purpose:
   This function takes a JSON dictionary as input, converts it to a DataFrame, performs data type conversion on specific columns, and generates dictionaries representing unique values from different columns. It returns dictionaries for teams, dates, and players, which can be used for various purposes.

2. Inputs:
   - json_dict_in: A JSON dictionary containing data to be processed.
     State: It should be a valid JSON dictionary.

3. Output:
   - cur_teams_dict_list: A list of dictionaries representing unique teams from the processed DataFrame.
     State: It is a list of dictionaries with "label" and "value" keys, where each dictionary corresponds to a unique team.

   - date_dict_list: A list of dictionaries representing dates converted from the processed DataFrame.
     State: It is a list of dictionaries with "label" and "value" keys, where each dictionary corresponds to a date.

   - cur_players_dict_list: A list of dictionaries representing unique players from the processed DataFrame.
     State: It is a list of dictionaries with "label" and "value" keys, where each dictionary corresponds to a unique player.

'''
def get_updated_dict_list(json_dict_in):
    if json_dict_in is None:
        raise PreventUpdate

    curDF = pd.DataFrame.from_dict(json_dict_in)
    curDF = get_df_convert_dtype_datetime(curDF)
    
    # teams
    cur_teams, cur_teams_dict_list = data.get_uniques_sort_insert_top(curDF, "PitcherTeam", True, "All")

    # dates
    date_dict_list = data.get_date2num_from_df(curDF)
    
    # players
    cur_players, cur_players_dict_list = data.get_uniques_sort_insert_top(curDF, "Pitcher", True, "All")

    # pitch types
    # cur_pitches, cur_pitches_dict_list = data.get_uniques_sort_insert_top(curDF, "TaggedPitchType", True, "All")

    return cur_teams_dict_list, date_dict_list, date_dict_list, cur_players_dict_list

# -------------------
# --- Stored data ---
# -------------------
# handle stored data here, so all functions can just use the stored data instead
# https://dash.plotly.com/dash-core-components/store
# The point is to have callbacks like datepicker and matchtype to change the data directly, so 
# we don't need to repeat calculations/filtering in every callback!
# this is the first callback! 
# Filters data from matchtype
@app.callback(
    Output(ids.STORED_DATA, "data"),
    Input(ids.MATCH_TYPE_RADIO, "value"),
    Input(ids.TEAM_DROPDOWN, "value"),
    Input(ids.STARTDATE_DROPDOWN, "value"),
    Input(ids.ENDDATE_DROPDOWN, "value"),
    Input(ids.DROPDOWN_PLAYERS_ALL, "value")
)
def update_stored_data_base(matchtype_str, team_select_list, startDate, endDate, player_list):
    return get_stored_data_from_vars(matchtype_str, team_select_list, startDate, endDate, player_list)

# update the list options based on the state of the current data
# NOTE: do NOT include pitchtype here, since not all graphs uses the same pitch type due to pitchtype ids... this is from different person working on the code /shrug
@app.callback(
    Output(ids.TEAM_DROPDOWN, "options"),
    Output(ids.STARTDATE_DROPDOWN, "options"),
    Output(ids.ENDDATE_DROPDOWN, "options"),
    Output(ids.DROPDOWN_PLAYERS_ALL, "options"),
    Input(ids.STORED_DATA, "data")
)
def update_team_options(json_dict_in):
    return get_updated_dict_list(json_dict_in)

# perform pitchtype update separately
@app.callback(
    Output(ids.PITCHTYPE_DROPDOWN_TEAM, "options"),
    Input(ids.STORED_DATA, "data")
)
def update_team_options(json_dict_in):
    curDF = pd.DataFrame.from_dict(json_dict_in)
    cur_pitches, cur_pitches_dict_list = data.get_uniques_sort_insert_top(curDF, "TaggedPitchType", True, "All")
    return cur_pitches_dict_list

# # Reset values of attributes to default in correlation. This is meant to be used in other pages as well... but a quick refresh takes care of most things
# @app.callback(
#     [Output(ids.DROPDOWN_ATTRIBUTES_X, 'value'),
#     Output(ids.DROPDOWN_ATTRIBUTES_Y, 'value'), 
#     Output(ids.DROPDOWN_ATTRIBUTES_Z, 'value'),
#     Output(ids.CTX_MSG, 'children')],
#     [Input(ids.RESET_DEFAULT_DROPDOWN_ATTRIBUTES, 'n_clicks')]
# )
# # the input is a click, in this case it's the number of clicks
# def reset_dropdowns(_: int):
#     # for debugging buttons
#     button_id = ctx.triggered_id if not None else 'No clicks yet'

#     if DEBUG == False:
#         ctx_msg = data.CTX_MSG_STR
#     else:
#         ctx_msg = json.dumps({
#             'states': ctx.states,
#             'triggered': ctx.triggered,
#             'inputs': ctx.inputs
#         }, indent=2)
#         print(ctx_msg)
        
#     return data.ATTR_X_STR, data.ATTR_Y_STR, data.ATTR_Z_STR, ctx_msg # note we are always returning the ctx msg.

# Correlation page
@app.callback(
    Output(ids.CORRELATION_HEATMAP, "figure"),
    Output(ids.CTX_MSG, 'children'),
    Input(ids.STORED_DATA, 'data'),
    Input(ids.DROPDOWN_PLAYERS_ALL, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_X, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Y, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Z, 'value'),
    Input(ids.INPUT_ATTRIBUTES_Z_QUANTILE, 'value')
)
def update_correlation_heatmap(json_dict_in, dropdown_pitcher_list, dropdown_attrX, dropdown_attrY, dropdown_attrZ, input_z):
    cur_data = pd.DataFrame.from_dict(json_dict_in)
    msg = ""

    if DEBUG:
        print(cur_data.info())
        print(f'''pitcher_dropdown: {dropdown_pitcher_list}''')
    
    # cannot have the same axis labels!
    if dropdown_attrX is None or dropdown_attrY is None or dropdown_attrZ is None:
        raise PreventUpdate
    if dropdown_attrX == dropdown_attrY or dropdown_attrX == dropdown_attrZ or dropdown_attrY == dropdown_attrZ:
        msg = "The 3 variables has to be different, so X cannot be the same as Y or Z, or Y same as X or Z, etc."
        return None, msg
    
    heatmap_data = cur_data[[dropdown_attrX, dropdown_attrY, dropdown_attrZ]]

    # safeguard on Z column data so quantile can work - only do qunatile on numbers!
    if cur_data.shape[0] > 0:
        # Do NOT use .loc here, since the loc refers to the absolute index, but after filtering, the starting index is likely NOT 0
        # Since we didn't convert column datatypes before, most columns that are NOT numeric would be objects. Here we know for certain that Pitcher is an object type
        if isinstance(cur_data[dropdown_attrZ][0], type(cur_data["Pitcher"][0])):
            msg = "Color variable has to be number based, such as SpinRate or RelHeight. Doesn't work with words like Pitcher or TaggedHitType."
            return None, msg

    # the the multi groupby to aggregate data on quantile, have to set numeric_only to False to avoid future pandas update error
    new_df = heatmap_data.groupby([dropdown_attrX, dropdown_attrY])[dropdown_attrZ].quantile(input_z, numeric_only=False).reset_index() # using median instead of count()
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
            title=f'Heatmap of Pitcher {dropdown_pitcher_list} Based on Median Value',
        )
    return fig, msg

'''
INTEGRATION OF LOCAITON HEATMAP GRIDZONE
'''
@app.callback(
    Output(ids.STRIKEZONE_ATTRIBUTES, "figure"),
    Input(ids.STORED_DATA, 'data'),
    Input(ids.DROPDOWN_PLAYERS_ALL, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Z, 'value'),
    Input(ids.VIEW_IDS, 'value'),
    Input(ids.STRIKE_PITCHCALL, 'value')
)
def grid_heatmap(json_dict_in, dropdown_pitcher_list, dropdown_attrZ, view_type, pitch_call_list) -> html.Div:
    # location data including all of the player

    loc_data = pd.DataFrame.from_dict(json_dict_in)
    # loc_data = zones_calculation(loc_data) # zone calculation now handled in data_processing, no need. This is now faster!

    # this does the filtering for players
    if dropdown_pitcher_list is None:
        PreventUpdate
    elif "All" not in dropdown_pitcher_list:
        loc_data = loc_data.loc[(loc_data['Pitcher'].isin(dropdown_pitcher_list))]

    if pitch_call_list is None:
        PreventUpdate
    if len(pitch_call_list) > 0 and "All" not in pitch_call_list:
        loc_data = loc_data.loc[(loc_data['PitchCall'].isin(pitch_call_list))]
    if dropdown_attrZ == "Tilt":
        return 

    # y is the side data and x is x data
    # drawing location heatmap 
    graph = go.Heatmap(
            x = loc_data['Location_Side'],
            y = loc_data['Location_Height'],
            z = loc_data[dropdown_attrZ],
            name = "heatmap", 
            colorscale = ids.BLUE_RED, 
            xgap = 2,
            ygap = 2,
            hoverongaps = False,
        )

    fig = go.Figure()

    # adding heatmap into figure
    fig.add_trace(graph)

    fig.update_xaxes(type='category')
    fig.update_yaxes(type='category')

    # changing the view type
    if view_type == "Catcher":
        fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        title = f'''Strikezone Heatmap for {dropdown_pitcher_list}''',
        xaxis = {'title': 'Side distance',
                'visible': True,
                'showticklabels': True,
                'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right'],
                'showgrid': False,
                },
        yaxis = {'title': 'Height distance',
                'visible': True,
                'showticklabels': True,
                'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper'],
                'showgrid': False
                },
        coloraxis_colorbar = dict(title = dropdown_attrZ),
        width = 650,
        height = 650
    )


    # adding black square on heatmap
    fig.add_shape(type="rect",
                x0=0.5, y0=0.5, x1=3.5, y1=3.5,
                line=dict(color="white", width = 7),
                ),

    return fig


'''
INTEGRATION OF LOCATION HEATMAP GRIDZONE
'''
@app.callback(
    Output(ids.DENSITY_ATTRIBUTES, "figure"),
    Input(ids.STORED_DATA, 'data'),
    Input(ids.DROPDOWN_PLAYERS_ALL, 'value'),
    Input(ids.DROPDOWN_ATTRIBUTES_Z, 'value'),
    Input(ids.VIEW_IDS, 'value'),
    Input(ids.STRIKE_PITCHCALL, 'value') 
)
def density_heatmap(json_dict_in, dropdown_pitcher_list, dropdown_attrZ, view_type, pitch_call_list) -> html.Div:
    loc_data = pd.DataFrame.from_dict(json_dict_in)
    # loc_data = zones_calculation(loc_data)

    # this does the filtering for players
    if dropdown_pitcher_list is None:
        PreventUpdate
    elif "All" not in dropdown_pitcher_list:
        loc_data = loc_data.loc[(loc_data['Pitcher'].isin(dropdown_pitcher_list))]

    if pitch_call_list is None:
        PreventUpdate
    if len(pitch_call_list) > 0 and "All" not in pitch_call_list:
        loc_data = loc_data.loc[(loc_data['PitchCall'].isin(pitch_call_list))]

    # this is not really needed since Tilt is cleaned in data processing and shouldn't exist, but JUST IN CASE
    if dropdown_attrZ == "Tilt":
        return

    layout = go.Layout(
                title = f'''Location Density for {dropdown_pitcher_list}''',
                xaxis = {'title': 'Side distance',
                            'visible': True,
                            'showticklabels': False,
                            'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right'],
                        },
                yaxis = {'title': 'Height distance',
                            'visible': True,
                            'showticklabels': False,
                            'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper'],
                        },
    )

    
    # y is the side data and x is x data
    # drawing location heatmap 
    fig = go.Figure(
            go.Heatmap(
                x = loc_data['Location_Side'],
                y = loc_data['Location_Height'],
                z = loc_data[dropdown_attrZ],
                name = "heatmap", 
                colorscale = ids.BLUE_RED, 
                hoverongaps = False,
                zsmooth = 'best'
            ),
    )

    # changing the view type
    if view_type == "Catcher":
        fig.update_yaxes(autorange="reversed")

    fig.update_layout(layout,
                    xaxis = {'title': 'Side distance',
                            'visible': True,
                            'showticklabels': True,
                            'categoryarray': ['Outside left', 'Left', 'Middle', 'Right', 'Outside right'],
                            'showgrid': False,
                            },
                    yaxis = {'title': 'Height distance',
                            'visible': True,
                            'showticklabels': True,
                            'categoryarray': ['Outside lower', 'Lower', 'Middle', 'Upper', 'Outside upper'],
                            'showgrid': False
                            },
                    coloraxis_colorbar = dict(title = dropdown_attrZ),
                    width = 650,
                    height = 650
    )

    fig.update_traces(
        hovertemplate='<br>'.join([
            'PlateLocHeight : %{x}',
            'PlateLocSide : %{y}',
            'Attribute: %{z}',
        ])
    )

    # adding black square on heatmap
    fig.add_shape(type="rect",
                x0=0.5, y0=0.5, x1=3.5, y1=3.5,
                line=dict(color="white", width = 7),
                )

    return fig


@app.callback(
    Output(ids.TIMESERIES_TEAM2, "figure"),
    [Input(ids.STORED_DATA, "data"),
     Input(ids.PITCHTYPE_DROPDOWN_TEAM, "value"),
     Input(ids.TIMESERIES_X_DROPDOWN, "value"),
     Input(ids.INPUT_X_LARGER, "value"),
     Input(ids.INPUT_X_SMALLER, "value"),
     Input(ids.TIMESERIES_Y_DROPDOWN, "value"),
     Input(ids.INPUT_Y_LARGER, "value"),
     Input(ids.INPUT_Y_SMALLER, "value"),
     Input(ids.TIMESERIES_COLOR_DROPDOWN, "value"),
     ]
)
def update_timeseries_team2(json_dict_in, pitch_list, x_val, in_x_larger, in_x_smaller, y_val, in_y_larger, in_y_smaller, c_val):
    # maybe rewrite .loc into .query for future benefits when the dataframe gets larger than 100,000 rows
    # see: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#performance-of-query
    if json_dict_in is None:
        raise PreventUpdate
    
    curDF = pd.DataFrame.from_dict(json_dict_in)
    curDF = get_df_convert_dtype_datetime(curDF)
    
    if pitch_list is None:
        PreventUpdate
    if len(pitch_list) > 0 and "All" not in pitch_list:
        curDF = curDF.loc[curDF["TaggedPitchType"] .isin(pitch_list)]
    
    # important to sort again for multi-column matching
    curDF = curDF.sort_values(by=['Datetime', "Inning"], ascending=True).reset_index(drop=True)

    # filter data using apply and lambda functions
    curDF = curDF.loc[curDF.apply(lambda row: 
                                  (in_x_larger is None or row[x_val] >= in_x_larger) and
                                  (in_x_smaller is None or row[x_val] <= in_x_smaller) and
                                  (in_y_larger is None or row[y_val] >= in_y_larger) and
                                  (in_y_smaller is None or row[y_val] <= in_y_smaller),
                                  axis=1)]

    # handling edge cases
    if c_val is None or c_val == "" or c_val == "None":
        fig = px.scatter(curDF, 
                            x=x_val,
                            y=y_val,
                            # markers = True,
                            )
    else:
        fig = px.scatter(curDF, 
                            x=x_val,
                            y=y_val,
                            color = c_val,
                            # markers = True,
                            # range_x=[min(curDF[x_val]), max(curDF[x_val])], 
                            # range_y=[min(curDF[y_val]), (min(curDF[y_val]) + max(curDF[y_val])) / 2],
                            )
        
    fig.update_layout({"title": f'Timeseries of Team on Pitchtypes',
                    "xaxis": {"title":f"{x_val}"},
                    "yaxis": {"title":f'{y_val}'},
                    "showlegend": True})

    # fig.write_image("by-month.png",format="png", width=1000, height=600, scale=3)
    return fig

# dynamically update the hand type list, this is also important!
@app.callback(
    Output(ids.PITCH_HAND_ID, "option"),
    Input(ids.STORED_DATA, "data"),
)
def update_handtype(json_dict_in):
    df = pd.DataFrame.from_dict(json_dict_in)
    df = df.dropna(subset=["BatterSide"]) # defensive programming to avoid all possible NaN in selection
    hand_ndarr = df["BatterSide"].unique()
    hand_ndarr = np.append(hand_ndarr, "All")
    return hand_ndarr

# update woba factors default based on year
@app.callback(
    [Output(ids.INPUT_UBBFACT, 'value'),
     Output(ids.INPUT_HBPFACT, 'value'),
     Output(ids.INPUT_1BFACT, 'value'),
     Output(ids.INPUT_2BFACT, 'value'),
     Output(ids.INPUT_3BFACT, 'value'),
     Output(ids.INPUT_HRFACT, 'value')],
     [Input(ids.DROPDOWN_WOBA_YEAR, "value")]
)
def update_woba_factors(year_str):
    if year_str.upper() != "CUSTOM":
        return wobaYearWeightList(year_str)
    else:
        return []

'''
WOBA GRAPHS 
'''
@app.callback(
    Output(ids.WOBA_FIGURE2, "figure"),
    Input(ids.STORED_DATA, "data"),
    Input(ids.PITCHTYPE_DROPDOWN_TEAM, 'value'),
    Input(ids.PITCH_HAND_ID, "value"),
    Input(ids.WOBA_PITCHCALL, "value"),
    Input(ids.WOBA_GRAPH_IDS, "value"),
    Input(ids.DROPDOWN_WOBA_SORT, "value"),
    Input(ids.INPUT_UBBFACT, 'value'),
    Input(ids.INPUT_HBPFACT, 'value'),
    Input(ids.INPUT_1BFACT, 'value'),
    Input(ids.INPUT_2BFACT, 'value'),
    Input(ids.INPUT_3BFACT, 'value'),
    Input(ids.INPUT_HRFACT, 'value')
)
def woba_graphs_fast(json_dict_in, pitch_type_list, hand_type, pitch_call_list, graph_type, sort_str, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num) -> html.Div:
    # NOTE: this is IMPORTANT! If there's no hand type for whatever reason, either the list or selection is off, then the entire thing breaks!
    # The defensive programming from 
    if hand_type is None:
        raise PreventUpdate
    woba_data = pd.DataFrame.from_dict(json_dict_in)

    '''
    applying filtering for each attribute
    '''
    if hand_type != "All":
        woba_data = woba_data.loc[(woba_data['BatterSide'] == hand_type)]
    
    if pitch_type_list is None:
        raise PreventUpdate
    if len(pitch_type_list) > 0 and "All" not in pitch_type_list:
        woba_data = woba_data.loc[woba_data["TaggedPitchType"] .isin(pitch_type_list)]
    
    if pitch_call_list is None:
        raise PreventUpdate
    if len(pitch_call_list) > 0 and "All" not in pitch_call_list:
        woba_data = woba_data.loc[(woba_data['PitchCall'].isin(pitch_call_list))]
    
    # Now start doing calculation. This should start AFTER the filtering is done.
    woba_data = addWOBACustomFast_v3(woba_data, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num)
    woba_data = woba_data.loc[(woba_data['wOBA'] != "UNDEFINED - DIVIDED BY ZERO")]

    if sort_str == "wOBA": # the groupby function in addWOBACustomFast_v3 automatically sort by last name, so only need to cover wOBA
        woba_data = woba_data.sort_values(by=["wOBA"])

    # change color scale here if needed
    # color_scale = px.colors.qualitative.Pastel

    if graph_type == ids.WOBA_GRAPH[0]:
        '''
        first graph: histogram of the woba
                    - consider, do we want the attribute_z also, for color?
        '''
        layout = go.Layout(
                    title = f'''wOBA Histogram for {hand_type} hands and {pitch_call_list} pitch types''',
        )
        # create a color scale
        hist = go.Figure(
                    px.bar(woba_data, x="Name", y="wOBA", color = "Name", 
                        #    color_discrete_sequence=color_scale,
                           hover_data = {'Name': True,
                                         'wOBA': True})
                )

        hist.update_layout(layout,
                            width = 1200,
                            height = 580,
                            yaxis = {
                                'tickformat' : '.2f'
                            }
        )
        return hist
            
    else:
        '''
        second graph: scatterplot of woba per player 
                        - filter to only show per hand or all
                        - filter to show by pitch type
        '''
        layout = go.Layout(
                    title = f'''wOBA Scatterplot for {hand_type} pitching hands and {pitch_call_list} pitch types''',
        )
        woba_data['Marker_Size'] = 0.5

        scatter = go.Figure(
                    px.scatter(
                        woba_data,
                        x="Name",
                        y="wOBA",
                        color="Name",
                        size="Marker_Size"
                    )
                 )

        scatter.update_layout(layout,
                                width = 1300,
                                height = 750,
                                yaxis = {
                                    'tickformat' : '.2f'
                                }
                             )
        return scatter


#------------------------------
#-this part adds custom graphs-
#------------------------------
# the code is like this because we are generating the layout AND the callback to each graph with the add...
# there are better ways to do this but this is what we got
@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '47%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Store(
                id={
                    'type' : "dynamic-stored-data",
                    'index' : n_clicks
                }
            ),
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            # 1st row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Match Type"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-matchtype-dpn',
                                    'index': n_clicks
                                },
                                options = data.MATCH_TYPES_DICT_LIST,
                                value = "All",
                                clearable = False
                            ),
                        ]
                        
                    ),
                    dbc.Col(
                        [
                            html.Div("Team"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-team-dpn',
                                    'index': n_clicks
                                },
                                options=data.ALL_TEAMS_DICT_LIST,
                                multi=True,
                                value=[data.TEAM_DEFAULT_STR], # use a list whenever multi is set to true
                                searchable=True,
                                clearable=False,
                            ),
                        ]
                        
                    ),
                    dbc.Col(
                        [
                            html.Div("Start Date"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-startdate-dpn',
                                    'index': n_clicks
                                },
                                options = data.DATE2NUM, 
                                value = data.DATE2NUM[0],
                                searchable=True,
                                clearable = False,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Div("End Date"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-enddate-dpn',
                                    'index': n_clicks
                                },
                                options = data.DATE2NUM, 
                                value = data.DATE2NUM[-1],
                                searchable=True,
                                clearable = False,
                            ),
                        ]
                    ),
                    
                ]
            ),
            # 2nd row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Player"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-player-dpn',
                                    'index': n_clicks
                                },
                                options=data.PLAYERS_ALL_DICT_LIST,
                                multi=True,
                                value=["All"],
                                searchable=True,
                                clearable=False
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Div("Pitch"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-pitchtype-dpn',
                                    'index': n_clicks
                                },
                                options = data.PITCH_TYPES_DICT_LIST, # list comprehension for selection options
                                multi = True,
                                value = [data.PITCH_DEFAULT_STR],
                                searchable=True,
                                clearable = False
                            ),
                        ]
                        
                    ),
                ]
            ),
            # 3rd row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("X variable"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-x-dpn',
                                    'index': n_clicks
                                },
                                options=data.ATTRIBUTES_DICT_LIST,
                                value=data.TS_X_STR,
                                clearable=False,
                                searchable=True,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Div("Y variable"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-y-dpn',
                                    'index': n_clicks
                                },
                                options=data.ATTRIBUTES_DICT_LIST,
                                value=data.TS_Y_STR,
                                clearable=False,
                                searchable=True,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.Div("Color variable"),
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-color-dpn',
                                    'index': n_clicks
                                },
                                options=data.ATTRIBUTES_DICT_LIST,
                                value = "",
                                clearable=True,
                                searchable=True,
                            )
                        ]
                    ),
                ]
            ),
        ]
    )
    div_children.append(new_child)
    return div_children

@app.callback(
    Output({'type': 'dynamic-stored-data', 'index': MATCH}, 'data'),
    Input({'type': 'dynamic-matchtype-dpn', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-team-dpn', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-startdate-dpn', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-enddate-dpn', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-player-dpn', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-pitchtype-dpn', 'index': MATCH}, 'value'),
)
def update_stored_data_base(matchtype_str, team_select_list, startDate, endDate, player_list, pitch_list):
    return get_stored_data_from_vars(matchtype_str, team_select_list, startDate, endDate, player_list, pitch_list)

# for team data select and player select
@app.callback(
    Output({'type': 'dynamic-team-dpn', 'index': MATCH}, 'options'),
    Output({'type': 'dynamic-startdate-dpn', 'index': MATCH}, 'options'),
    Output({'type': 'dynamic-enddate-dpn', 'index': MATCH}, 'options'),
    Output({'type': 'dynamic-player-dpn', 'index': MATCH}, 'options'),
    Input({'type': 'dynamic-stored-data', 'index': MATCH}, 'data')
)
def update_vars(json_dict_in):
    return get_updated_dict_list(json_dict_in)

@app.callback(
    Output({'type': 'dynamic-pitchtype-dpn', 'index': MATCH}, 'options'),
    Input({'type': 'dynamic-stored-data', 'index': MATCH}, 'data')
)
def update_team_options(json_dict_in):
    curDF = pd.DataFrame.from_dict(json_dict_in)
    cur_pitches, cur_pitches_dict_list = data.get_uniques_sort_insert_top(curDF, "TaggedPitchType", True, "All")
    return cur_pitches_dict_list

@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input({'type': 'dynamic-stored-data', 'index': MATCH}, 'data'),
     Input({'type': 'dynamic-player-dpn', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-pitchtype-dpn', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-x-dpn', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-y-dpn', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-color-dpn', 'index': MATCH}, 'value'),
     ]
)
def update_graph_v2(json_dict_in, player_list, pitch_list, x_val, y_val, c_val):
    curDF = pd.DataFrame.from_dict(json_dict_in)
    curDF = get_df_convert_dtype_datetime(curDF)
    
    # important to sort again for multi-column matching
    curDF = curDF.sort_values(by=['Datetime', "Inning"], ascending=True).reset_index(drop=True)

    # handling edge cases
    if c_val is None or c_val == "" or c_val == "None":
        fig = px.scatter(curDF, 
                            x=x_val,
                            y=y_val,
                        )
    else:
        fig = px.scatter(curDF, 
                            x=x_val,
                            y=y_val,
                            color = c_val,
                        )
        
    fig.update_layout(
                        {
                            "title": f'Timeseries of Team on Pitchtypes',
                            "xaxis": {"title":f"{x_val}"},
                            "yaxis": {"title":f'{y_val}'},
                            "showlegend": True,
                            "autosize": True,
                            "margin" : dict(
                                t=30,
                                b=30,
                                )
                        },
                    )

    # fig.write_image(f'''graph.png''',format="png", width=1000, height=600, scale=3)
    return fig
