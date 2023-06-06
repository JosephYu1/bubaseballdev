from pydoc import classname
import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from src import components 
from documentation_text import * 
import ids, data, callback # the "." means relative import


# Import app
from app import app
# Import server for deployment
from app import srv as server
from data_modification_layouts import *

title = html.Div(
    [
        html.H1("Welcome to the Baylor Baseball Analytics Site"),
    ],
    style={"text-align": "center"},
)

docs_title = html.Div(
    [
        html.H3("Documentation"),
    ],
    style={"text-align": "left", 'margin-top': '3%','margin-bottom': '2%'},
)

# REFERENCE: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
collapse_radio = html.Div(
    [
        dbc.Button(
            "Radio Buttons",
            id="radio-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            radio_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_team = html.Div(
    [
        dbc.Button(
            "Team Analysis",
            id="team-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            team_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_corr = html.Div(
    [
        dbc.Button(
            "Correlation Analysis",
            id="corr-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,           
        ),
        html.Div(
            corr_card,
            style={"minHeight": "3%"},
        )
    ]
)

collapse_input = html.Div(
    [
        dbc.Button(
            "Input Box",
            id="input-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,           
        ),
        html.Div(
            input_card,
            style={"minHeight": "3%"},
        )
    ]
)

collapse_drop = html.Div(
    [
        dbc.Button(
            "Dropdown List",
            id="drop-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,           
        ),
        html.Div(
            dropdown_card,
            style={"minHeight": "3%"},
        )
    ]
)

collapse_strikezone = html.Div(
    [
        dbc.Button(
            "Strikezone Analysis",
            id="gridzone-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            strikezone_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_woba = html.Div(
    [
        dbc.Button(
            "wOBA Analysis",
            id="woba-gridzone-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            woba_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_custom = html.Div(
    [
        dbc.Button(
            "Custom Analysis",
            id="custom-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            custom_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_upload = html.Div(
    [
        dbc.Button(
            "Upload Data",
            id="upload-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            upload_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_edit = html.Div(
    [
        dbc.Button(
            "Edit Data",
            id="edit-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            edit_card,
            style={"minHeight": "3%"},
        ),
    ]
)

collapse_refresh = html.Div(
    [
        dbc.Button(
            "Refreshing",
            id="refresh-horizontal-collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
            size = 5,
        ),
        html.Div(
            refresh_card,
            style={"minHeight": "3%"},
        ),
    ]
)

'''
MENU WITH ALL DOCUMENTATION
'''
collapse_docs = html.Div([
    dbc.Row(
        [
            title,
            banner,
            docs_title,
        ],
    ),
    dbc.Row(
    [
        dbc.Col([
            html.H4("Elements"),
            collapse_radio,
            collapse_drop,
            collapse_input,
            collapse_refresh,
            html.Hr(),
            html.H4("Pages"),
            collapse_team,
            collapse_corr,
            collapse_strikezone,
            collapse_woba,
            collapse_custom,
            html.Hr(),
            html.H4("Add/Edit Data"),
            collapse_upload,
            collapse_edit,
        ])
    ]
    )

]
)


'''
BUTTON OPENINGS CALLBACKS FOR EACH TAB AND FUNCTIONALITY
'''
@app.callback(
    Output("radio-horizontal-collapse", "is_open"),
    [Input("radio-horizontal-collapse-button", "n_clicks")],
    [State("radio-horizontal-collapse", "is_open")],
)
def radio_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("gridzone-horizontal-collapse", "is_open"),
    [Input("gridzone-horizontal-collapse-button", "n_clicks")],
    [State("gridzone-horizontal-collapse", "is_open")],
)
def gridzone_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("woba-horizontal-collapse", "is_open"),
    [Input("woba-gridzone-horizontal-collapse-button", "n_clicks")],
    [State("woba-horizontal-collapse", "is_open")],
)
def woba_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("team-horizontal-collapse", "is_open"),
    [Input("team-horizontal-collapse-button", "n_clicks")],
    [State("team-horizontal-collapse", "is_open")],
)
def team_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("corr-horizontal-collapse", "is_open"),
    [Input("corr-horizontal-collapse-button", "n_clicks")],
    [State("corr-horizontal-collapse", "is_open")],
)
def corr_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("custom-horizontal-collapse", "is_open"),
    [Input("custom-horizontal-collapse-button", "n_clicks")],
    [State("custom-horizontal-collapse", "is_open")],
)
def custom_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("input-horizontal-collapse", "is_open"),
    [Input("input-horizontal-collapse-button", "n_clicks")],
    [State("input-horizontal-collapse", "is_open")],
)
def input_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("drop-horizontal-collapse", "is_open"),
    [Input("drop-horizontal-collapse-button", "n_clicks")],
    [State("drop-horizontal-collapse", "is_open")],
)
def drop_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("upload-horizontal-collapse", "is_open"),
    [Input("upload-horizontal-collapse-button", "n_clicks")],
    [State("upload-horizontal-collapse", "is_open")],
)
def drop_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("edit-horizontal-collapse", "is_open"),
    [Input("edit-horizontal-collapse-button", "n_clicks")],
    [State("edit-horizontal-collapse", "is_open")],
)
def drop_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("refresh-horizontal-collapse", "is_open"),
    [Input("refresh-horizontal-collapse-button", "n_clicks")],
    [State("refresh-horizontal-collapse", "is_open")],
)
def drop_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


