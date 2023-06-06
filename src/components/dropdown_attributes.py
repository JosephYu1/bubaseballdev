from dash import Dash, html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from . import ids, data
import json

DEBUG = False

# TODO: add color picker!
# https://dash.plotly.com/dash-daq/colorpicker

# data testing
all_attr = data.ATTRIBUTES_NDARR
all_coachable = data.COACHABLE_LIST
setAttr = set(all_attr)
bad_attr = [x for x in all_coachable if x not in setAttr]
if bad_attr:
    print(bad_attr)
    # handles bad data by preventing update
    raise Dash.exceptions.PreventUpdate

# defaults
default_attrX = 'TaggedPitchType' 
default_attrY = 'PitchCall'
default_attrZ = 'SpinRate'
ctx_msg = ""

# useful documentation on layout:
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/


def render(app: Dash) -> html.Div:

    # for resetting to default values
    @app.callback(
        [Output(ids.DROPDOWN_ATTRIBUTES_X, 'value'),
        Output(ids.DROPDOWN_ATTRIBUTES_Y, 'value'), 
        Output(ids.DROPDOWN_ATTRIBUTES_Z, 'value'),
        Output(ids.CTX_MSG, 'children')],
        [Input(ids.RESET_DEFAULT_DROPDOWN_ATTRIBUTES, 'n_clicks')]
    )
    # the input is a click, in this case it's the number of clicks
    def reset_dropdowns(_: int):
        # for debugging buttons
        button_id = ctx.triggered_id if not None else 'No clicks yet'

        if DEBUG: 
            ctx_msg = json.dumps({
                'states': ctx.states,
                'triggered': ctx.triggered,
                'inputs': ctx.inputs
            }, indent=2)
            print(ctx_msg)
        else:
            ctx_msg = ""
            
        return default_attrX, default_attrY, default_attrZ, ctx_msg

    # the following we make 
    return html.Div(
        children = [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6("Select X axis variable"),
                            dcc.Dropdown(
                                # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                                id = ids.DROPDOWN_ATTRIBUTES_X,
                                options = [{"label" : p, "value": p} for p in all_attr], # list comprehension for selection options
                                value = default_attrX, # initial value of the dropdown
                                # multi = True # more than one selection
                                # can also make this not clearable
                            ),

                        ],
                        align = "center",
                        md = 3,
                    ),

                    dbc.Col(
                        [
                            html.H6("Select Y axis variable"),
                            dcc.Dropdown(
                                # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                                id = ids.DROPDOWN_ATTRIBUTES_Y,
                                options = [{"label" : p, "value": p} for p in all_attr], # list comprehension for selection options
                                value = default_attrY, # initial value of the dropdown
                                # multi = True # more than one selection
                                # can also make this not clearable
                            ),
                        ],
                        align = "center",
                        md = 3,
                    ),
                    
                    dbc.Col(
                        [
                            html.H6("Select Coachable (Color) variable"),
                            dcc.Dropdown(
                                # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                                id = ids.DROPDOWN_ATTRIBUTES_Z,
                                options = [{"label" : p, "value": p} for p in all_coachable], # list comprehension for selection options
                                value = default_attrZ, # initial value of the dropdown
                                # multi = True # more than one selection
                                # can also make this not clearable
                            )
                        ],
                        align = "center",
                        md = 3,
                    ),
                    
                    dbc.Col(
                        html.Button(
                        id = ids.RESET_DEFAULT_DROPDOWN_ATTRIBUTES,
                        className = "dropdown-button",
                        children=["Reset"],
                        n_clicks=0,
                        ),
                        align = "end",
                        md = 3,
                    ),
                    
                ]
            ),
            

            dbc.Row(
                html.Pre(
                    id=ids.CTX_MSG, 
                    children = [ctx_msg])
            )
        ]
    )