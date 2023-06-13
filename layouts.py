import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
# from src import components 
import ids, data, callback # the "." means relative import


# datetime format
DT_FORMAT = "%Y/%m/%d"

# dynamic data linking
baseball_all = data.BASEBALL_ALL_DF

baylor_all = data.BASEBALL_ALL_DF_BAY

baseball_private = data.BASEBALL_PRIVATE_DF

baseball_public = data.BASEBALL_PUBLIC_DF

pitch_type = data.PITCH_TYPES_NDARR


'''
ELEMENT DEFINITIONS
'''


####################################
#  ATTRIBUTES FOR THE RANGE MENU   #
####################################
# dropdown for choosing you x and y-axis variables
rangeAttrPicker = dbc.Row(
    children = [
        # y-axis feature picker 
        dbc.Col([
                html.H6("Select Y axis feature: "),
                dcc.Dropdown(
                    id = ids.TIMESERIES_Y_DROPDOWN,
                    options = [{"label" : p, "value": p} for p in data.ATTRIBUTES_NDARR], # list comprehension for selection options
                    value = data.TS_Y_STR,
                    searchable=True,
                ),
            ],  
            align = "center",
            md = 2,         
        ),
        # x-axis feature picker
        dbc.Col([
                html.H6("Select X axis feature: "),
                dcc.Dropdown(
                    id = ids.TIMESERIES_X_DROPDOWN,
                    options = [{"label" : p, "value": p} for p in data.ATTRIBUTES_NDARR], # list comprehension for selection options
                    value = data.TS_X_STR,
                    searchable=True,
                ),
            ],
            align = "center",
            md = 2,    
        ),
    ]),
    
# radio buttons element
radioButtons =  dbc.Row(
            children=[
                dbc.Col(
                    dcc.RadioItems(
                        id = ids.MATCH_TYPE_RADIO,
                        options = [
                            {
                                'label' : "All",
                                'value' : "All"
                            },
                            {
                                'label' : "Private", 
                                'value' : "Private"
                            },
                            {
                                'label' : "Public", 
                                'value' : "Public"
                            },
                        ],
                        value = "All",
                        className="radio",
                ),),
            ],
        )

# dropdown filters 
teamDropdown = dbc.Col([
                        # title of dropdown for team
                        html.H6("Select Team:"),
                        # dropdown menu for team
                        dcc.Dropdown(
                            id = ids.TEAM_DROPDOWN,
                            options = data.ALL_TEAMS_DICT_LIST,
                            multi = True,
                            value = [data.TEAM_DEFAULT_STR],
                            searchable=True,
                            clearable=False,
                        ),
                    ],
                    md = 4,
                    align = "center"
            )


playerDropdown = dbc.Col([
                        # title of dropdown for player
                        html.H6("Select Player:"),
                        # dropdown menu for player
                        dcc.Dropdown(
                            id = ids.DROPDOWN_PLAYERS_ALL, # having the id here works, because it knows when and where to update
                            options = data.PLAYERS_ALL_DICT_LIST, # list comprehension for selection options
                            value = ["All"], # initial value of the dropdown,
                            searchable=True,
                            multi = True
                        ),
                    ],
                    md = 4,
                    align = "center"
                )

pitchDropdown = dbc.Col([
                        html.H6("Select Pitch Type:"),
                        dcc.Dropdown(
                            id = ids.PITCHTYPE_DROPDOWN_TEAM,
                            options = data.PITCH_TYPES_DICT_LIST, 
                            value = [data.PITCH_DEFAULT_STR],
                            searchable=True,
                            multi = True,
                        ),
                    ],
                    md = 4,
                    align = "center"
                )

# This doesn't look as nice as the date range picker, but is more useful, because it only show the dates that have matches
# The rational is that there's no point to show the entire calender when the user is just trying to data relevant to the match
dateDropdown = dbc.Row(
                children=[
                    dbc.Col([
                            html.H6("Start Date:"),
                            dcc.Dropdown(
                                # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                                id = ids.STARTDATE_DROPDOWN,
                                options = data.DATE2NUM, # list comprehension for selection options
                                value = data.DATE2NUM[0], # initial value of the dropdown,
                                searchable=True,
                                clearable = False,
                            )
                        ],
                        align = "center",
                        md = 2,
                    ),
                    dbc.Col([
                            html.H6("End Date:"),
                            dcc.Dropdown(
                                # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                                id = ids.ENDDATE_DROPDOWN,
                                options = data.DATE2NUM, # list comprehension for selection options
                                value = data.DATE2NUM[-1], # initial value of the dropdown,
                                searchable=True,
                                clearable = False,
                            )
                        ],
                        align = "center",
                        md = 2,
                    ),
                ])

# "larger than" options for x and y-axis 
largerThanOptions = dbc.Row(
        children = [
            # menu for the y-axis
            dbc.Col([
                html.H6("Larger than or equal to: "),
                dcc.Input(
                    id = ids.INPUT_Y_LARGER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                ),
            ],
            align = "center",
            md = 2,   
            ),
            # menu for the x-axis 
            dbc.Col([
                html.H6("Larger than or equal to:"),
                dcc.Input(
                    id = ids.INPUT_X_LARGER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                ),
            ],
            align = 'center',
            md = 2,
            ),
        ],
        style = {'padding':"0.7% 0%"}
    ),

# "smaller than" options for x and y-axis   
smallerThanOptions = dbc.Row(
        children = [
            # menu for the y-axis
            dbc.Col([
                html.H6("Smaller than or equal to: "),
                dcc.Input(
                    id = ids.INPUT_Y_SMALLER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                ),
            ],
            align = "center",
            md = 2,   
            ),
            # menu for the x-axis 
            dbc.Col([
                html.H6("Smaller than or equal to:"),
                dcc.Input(
                    id = ids.INPUT_X_SMALLER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                ),
            ],
            align = 'center',
            md = 2,
            ),
        ],
        style = {'padding':"0.7% 0%"}
),

menuRange = html.Div([
                dbc.Col(
                    children=[ 
                        html.Div(rangeAttrPicker),
                    ]
                ),
                dbc.Col(
                    children = [
                        html.Div(largerThanOptions),
                        html.Div(smallerThanOptions)
                    ]
                )
            ])
'''
MENU DEFINITION
'''
#  menu for radio buttons
radioMenu = html.Div(radioButtons)

# player, pitchen, and team menu for all graphs
headerMenu = html.Div(
    [
        dbc.Col([
            dbc.Row(
                children=[
                    teamDropdown,
                ],
                style = {'padding':"0.7% 0.1%"}
            ),
            dbc.Row(
                children=[
                    playerDropdown,
                ],
                style = {'padding':"0.7% 0.1%"}
            ),
            dbc.Row(
                children=[
                    pitchDropdown,
                ],
                style = {'padding':"0.7% 0.1%"}
            ),
        ]
        ),
    ],
    style = {'padding':"0.7% 0.1%"}
)

# date picker menu (start date, end date)
dateMenu = html.Div(
    [
        dbc.Row(dateDropdown),
    ],
    style = {'padding':"0.7% 0%"}
)

# menu for the team analysis tab
menuCombined = html.Div(
    [
        dbc.Col([
            dateMenu,
            headerMenu, 
        ])
    ]
)

teamMenu = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dateMenu, 
                headerMenu, 
            ],
            align = 'start',
            width="10%",
            ),
            html.Hr(),
            dbc.Col([
                menuRange
            ],
            align = 'center',
            width="10%"
            )
        ],
        className="g-0",
        )
    ]
)

# select the attributes of what to display on heatmap
attrMenu = html.Div(
    [
        dbc.Row(
            children=[
                html.Hr(),
                dbc.Col(
                    [
                        html.H6("Select X axis variable"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.DROPDOWN_ATTRIBUTES_X,
                            options = data.ATTRIBUTES_DICT_LIST, #[{"label" : p, "value": p} for p in data.ATTRIBUTES_NDARR], # list comprehension for selection options
                            value = data.ATTR_X_STR, # initial value of the dropdown,
                            searchable=True,
                            clearable=False,
                            # multi = True # more than one selection
                            # can also make this not clearable
                        ),

                    ],
                    align = "center",
                    md = 2,
                    ),

                dbc.Col(
                    [
                        html.H6("Select Y axis variable"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.DROPDOWN_ATTRIBUTES_Y,
                            options = data.ATTRIBUTES_DICT_LIST, #[{"label" : p, "value": p} for p in data.ATTRIBUTES_NDARR], # list comprehension for selection options
                            value = data.ATTR_Y_STR, # initial value of the dropdown,
                            searchable=True,
                            clearable=False,
                        ),
                    ],
                    align = "center",
                    md = 2,
                ),
                
                dbc.Col(
                    [
                        html.H6("Select Color variable"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.DROPDOWN_ATTRIBUTES_Z,
                            options = data.ATTRIBUTES_DICT_LIST, #[{"label" : p, "value": p} for p in data.ATTRIBUTES_NDARR], # list comprehension for selection options
                            value = data.ATTR_Z_STR, # initial value of the dropdown,
                            searchable=True,
                            clearable=True, # NOTE: this can be cleared as a None option, but can also select None
                        )
                    ],
                    align = "center",
                    md = 2,
                ),

                dbc.Col(
                    [
                        html.H6("Select Color Quantile (0.5 gives Median)"),
                        dbc.Col(dcc.Input(
                            id = ids.INPUT_ATTRIBUTES_Z_QUANTILE,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            max = 1,
                            value = 0.5, # default set to median, which is 0.5
                            debounce=True
                        )),
                    ],
                    align = "center",
                    md = 3,
                ),
                
                # dbc.Col(
                #     dbc.Button(
                #         id = ids.RESET_DEFAULT_DROPDOWN_ATTRIBUTES,
                #         className = "dropdown-button",
                #         children=["Reset"],
                #         n_clicks=0,
                #     ),
                #     align = "end",
                #     md = 2,
                # ),
                dbc.Col(
                    html.H5(
                        id=ids.CTX_MSG, 
                        children = [data.CTX_MSG_STR])
                )
            ]
        ),

    ]
)

heatmap = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id = ids.CORRELATION_HEATMAP)),
                # dbc.Col(dcc.Graph(id = ids.CORRELATION_HEATMAP2)),
            ]
            
        )
    ]
)

# ============================
# ---- Location Heatmaps -----
# ============================
'''
LOCATION HEATMAP OPTIONS AND ATTRIBUTES
'''
grid_attrMenu = html.Div(
    [
        dbc.Row(
            children=[
                html.Hr(),
                dbc.Col([
                        html.H6("Select Coachable (Color) variable"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.DROPDOWN_ATTRIBUTES_Z,
                            options = data.COACHABLE_DICT_LIST, # list comprehension for selection options
                            value = data.ATTR_Z_STR, # initial value of the dropdown,
                            searchable=True,
                            # multi = True # more than one selection
                            # can also make this not clearable
                        )
                    ],
                    align = "center",
                    md = 3,
                ),
                dbc.Col([
                        html.H6("Select View"),
                        dcc.Dropdown(
                            id = ids.VIEW_IDS,
                            options  = [{"label": p, "value": p} for p in ids.VIEW_TYPES],
                            value = ids.VIEW_TYPES[0],
                            searchable=True,
                        )
                    ],
                    align = "center",
                    md = 3,
                ),
                dbc.Col([
                    html.H6("Select PitchCall"),
                    dcc.Dropdown(
                        id = ids.STRIKE_PITCHCALL,
                        options  = data.PITCH_CALL_DICT_LIST,
                        value = [data.PITCH_TYPE[0]],
                        searchable=True,
                        multi=True,
                        clearable=False
                    )
                ],
                align = "center",
                md = 3,
                ),
            ],  
            style={'flex': 1},
        ),

    ]
)

density_attrMenu = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col([
                        html.H6("Select Coachable (Color) variable"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.DROPDOWN_ATTRIBUTES_Z,
                            options = data.COACHABLE_DICT_LIST, # list comprehension for selection options
                            value = data.ATTR_Z_STR, # initial value of the dropdown,
                            searchable=True,
                            # multi = True # more than one selection
                            # can also make this not clearable
                        )
                    ],
                    align = "center",
                    md = 3,
                ),
                dbc.Col([
                    html.H6("Select View"),
                    dcc.Dropdown(
                        id = ids.VIEW_IDS,
                        options  = [{"label": p, "value": p} for p in ids.VIEW_TYPES],
                        value = ids.VIEW_TYPES[0],
                        searchable=True,
                    )
                ],
                align = "center",
                md = 3,
                ),
                dbc.Col([
                    html.H6("Select PitchCall"),
                    dcc.Dropdown(
                        id = ids.STRIKE_PITCHCALL,
                        options  = data.PITCH_CALL_DICT_LIST,
                        value = [data.PITCH_TYPE[0]],
                        searchable=True,
                        multi=True,
                        clearable=False

                    )
                ],
                align = "center",
                md = 3,
                ),

            ],
            style={'flex': 1},
        ),

    ]
)


''' 
EACH TYPE OF HEATMAP
'''
gridzone_heatmap = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(dcc.Graph(id = ids.STRIKEZONE_ATTRIBUTES), ),
                dbc.Col(dcc.Graph(id = ids.DENSITY_ATTRIBUTES), )
            ]
        )
    ],
)

# @Deprecated
density_heatmap = html.Div(
    [
        dbc.Row(
            id = ids.DENSITY_ATTRIBUTES,
        )
    ]
)

# ============================
# ------ Time Series ---------
# ============================
timeseries_player = html.Div(
    [
        dbc.Row(
            dcc.Graph(id = ids.TIMESERIES_PLAYER)
        )
    ]
)

timeseries_team = html.Div(
    [
        dbc.Row(
            [
                # dbc.Col(dcc.Graph(id = ids.TIMESERIES_TEAM)),
                dbc.Col(dcc.Graph(id = ids.TIMESERIES_TEAM2)),
            ]
            
        )
    ]
)


# @Deprecated
# picker for date range
# https://dash.plotly.com/dash-core-components/datepickerrange
# to use its values in callback, they are 2 separate Inputs/Outputs, like:
#   Output(ids.DATEPICKER, 'start_date'),
#   Output(ids.DATEPICKER, "end_date"),
dateSlider = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.DatePickerRange(
                    id=ids.DATEPICKER,
                    min_date_allowed= data.DATE2NUM[0],
                    max_date_allowed= data.DATE2NUM[-1],
                    initial_visible_month=data.DATE2NUM[0],
                    start_date= data.DATE2NUM[0],
                    end_date=data.DATE2NUM[-1],
                    with_portal = True, # what exactly is a portal?
                    clearable=True, # need to handle None in callback
                    # tooltip={'always_visible': False, 'placement': 'bottom'}
                )),
                dbc.Col(html.P(style={'font-size': '16px', 'opacity': '100%'},
                               children='Pick Date Range. You may also click and drag a box on the graph below to do quick zoom.'))
            ]
        )      
    ],
    style = {'width': 'auto', 'display':'inline-block',}
)

# select pitch type
pitchtype_drop_player = html.Div(
    [
        dbc.Row(
            [
                html.H6("Select Pitch Type:"),
                dbc.Col(dcc.Dropdown(
                    id = ids.PITCHTYPE_DROPDOWN_PLAYER,
                    options = data.PITCH_TYPES_DICT_LIST, #[{"label" : p, "value": p} for p in pitch_type], # list comprehension for selection options
                    value = data.PITCH_DEFAULT_STR,
                    searchable=True,
                    clearable = False
                )),
            ]
            
        )
    ]
)

pitchtype_drop_team = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id = ids.PITCHTYPE_DROPDOWN_TEAM,
                    options = data.PITCH_TYPES_DICT_LIST, #[{"label" : p, "value": p} for p in pitch_type], # list comprehension for selection options
                    multi = True,
                    value = [data.PITCH_DEFAULT_STR],
                    searchable=True,
                    clearable=False
                )),
                dbc.Col(html.Div(children='Select Pitch Type. Use "All" to show different types at the same time'
                        )),
            ]
            
        )
    ]
)

# timeseries x axis
timeseries_x_drop = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(children='Select X axis feature.'
                        )),
                dbc.Col(dcc.Dropdown(
                    id = ids.TIMESERIES_X_DROPDOWN,
                    options = data.ATTRIBUTES_DICT_LIST, # list comprehension for selection options
                    value = data.TS_X_STR,
                    searchable=True,
                )),
                dbc.Col(html.Div(children="Larger than or equal to value (press enter to refresh)"
                        )),
                dbc.Col(dcc.Input(
                    id = ids.INPUT_X_LARGER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                )),
                dbc.Col(html.Div(children="Smaller than or equal to value (press enter to refresh)"
                        )),
                dbc.Col(dcc.Input(
                    id = ids.INPUT_X_SMALLER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                )),
                
            ]
        )
    ]
)

# timeseries y axis
timeseries_y_drop = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(children='Select Y axis feature.'
                        )),
                dbc.Col(dcc.Dropdown(
                    id = ids.TIMESERIES_Y_DROPDOWN,
                    options = data.ATTRIBUTES_DICT_LIST, # list comprehension for selection options
                    value = data.TS_Y_STR,
                    searchable=True,
                )),
                dbc.Col(html.Div(children="Larger than or equal to value (press enter to refresh)"
                        )),
                dbc.Col(dcc.Input(
                    id = ids.INPUT_Y_LARGER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                )),
                dbc.Col(html.Div(children="Smaller than or equal to value (press enter to refresh)"
                        )),
                dbc.Col(dcc.Input(
                    id = ids.INPUT_Y_SMALLER,
                    type = 'number',
                    placeholder="Input a number",
                    min = 0,
                    debounce=True
                )),
            ]
        )
    ]
)

# timeseries color for teams
timeseries_color_drop = html.Div(
    [
        dbc.Row(
            [
                html.H6("Select color grouping feature:"),
                dbc.Col(dcc.Dropdown(
                    id = ids.TIMESERIES_COLOR_DROPDOWN,
                    options = data.ATTRIBUTES_DICT_LIST, # list comprehension for selection options
                    value = "", # this assumes the callback handles "None" or "" as a str!
                    searchable=True,
                )),
            ],
            style= {"width" : "18.5%"}
    
        )
    ]
)

# ============================
# ---- WOBA Graphs -----
# ============================
woba_attrMenu = html.Div(
    [
        dbc.Row(
            children=[
                html.Hr(),
                dbc.Col([
                        html.H6("Select batter hand"),
                        dcc.Dropdown(
                            # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                            id = ids.PITCH_HAND_ID,
                            options = [{"label" : p, "value": p} for p in data.HAND_LIST], # list comprehension for selection options
                            value = data.HAND_LIST[0], # initial value of the dropdown
                            # multi = True # more than one selection
                            # can also make this not clearable
                        )
                    ],
                    align = "center",
                    md = 2,
                ),
                dbc.Col([
                    html.H6("Select PitchCall"),
                    dcc.Dropdown(
                        id = ids.WOBA_PITCHCALL,
                        options  = data.PITCH_CALL_DICT_LIST,
                        value = [data.PITCH_TYPE[0]],
                        multi=True,
                        searchable=True,
                        clearable = False,
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6("Select graph"),
                    dcc.Dropdown(
                        id = ids.WOBA_GRAPH_IDS,
                        options  = [{"label": p, "value": p} for p in ids.WOBA_GRAPH],
                        value = ids.WOBA_GRAPH[0],
                        clearable = False
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6(f'''Select Sorting By'''),
                    dcc.Dropdown(
                            id = ids.DROPDOWN_WOBA_SORT,
                            options=data.WOBA_SORT_OPTION,
                            value = data.WOBA_SORT_OPTION[0],
                            clearable = False,
                        )
                ],
                align = "center",
                md = 2,
                ),

                dbc.Col([
                    html.H6(f'''wOBA Default or Use Custom'''),
                    dcc.Dropdown(
                            id = ids.DROPDOWN_WOBA_YEAR,
                            # type = 'text',
                            # placeholder=f'''Input a year, like "2022"''',
                            options=data.WOBA_YEARS_DICT_LIST,
                            value = "2022",
                            clearable=False,
                        )
                ],
                align = "center",
                md = 2,
                ),

            ],
            style={'margin-bottom' : 20, 'flex': 1},
        ),
        dbc.Row(
            children=[
                dbc.Col([
                        html.H6("Set UBB"),
                        dcc.Input(
                            id = ids.INPUT_UBBFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                        )
                    ],
                    align = "center",
                    md = 2,
                ),
                dbc.Col([
                    html.H6("Set HBP"),
                    dcc.Input(
                        id = ids.INPUT_HBPFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6("Set 1B"),
                    dcc.Input(
                        id = ids.INPUT_1BFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6("Set 2B"),
                    dcc.Input(
                        id = ids.INPUT_2BFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6("Set 3B"),
                    dcc.Input(
                        id = ids.INPUT_3BFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                    )
                ],
                align = "center",
                md = 2,
                ),
                dbc.Col([
                    html.H6("Set HR"),
                    dcc.Input(
                        id = ids.INPUT_HRFACT,
                            type = 'number',
                            placeholder="Input a number",
                            min = 0,
                            debounce=True
                    )
                ],
                align = "center",
                md = 2,
                ),

            ],
            style={'flex': 1},
        ),


    ]
)

woba_graph = html.Div(
    [
        dbc.Row(
            [
                # dbc.Col(dcc.Graph(id = ids.WOBA_FIGURE)),
                dbc.Col(dcc.Graph(id = ids.WOBA_FIGURE2))
             ]
        ),
    ],
    style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
)

# container for adding graphs

graph_container = html.Div(
    [
        # dbc.Button("Add Graph", 
        #            id='add-chart', 
        #            n_clicks=0,
        #            size = "lg",
        #            outline = False,
        #            color="secondary",
        #            ),
        html.Div(id='container', children=[]),
    ]
)
