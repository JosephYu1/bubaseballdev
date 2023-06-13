# import dash
from dash import html, dcc
from dash.dependencies import Input, Output


# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, documentation, custom callbacks
from layouts import *
from documentation import *
import callback

# Import app
from app import app
# Import server for deployment
from app import srv as server
from data_modification_layouts import *

# NOTE: Flash required for icon display
import flask
baseball_server = flask.Flask(__name__)
app._favicon = ("./assets/(favicon).ico")


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        dcc.Store(id = ids.STORED_DATA), # needs to be here so all pages has access to stored data
        html.Img(
            src=app.get_asset_url('baylor_baseball_spread.png'), 
            style={'text-align':'center'},
        ),
        dbc.NavLink(html.H2("DOCUMENTATION", className = 'lead'), href = '/'),
        html.Hr(),
        html.H2("HISTORICAL ANALYSIS", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("New Pitcher Analysis", href="/custom", active="exact", id = ids.NEW_PITCHER_TAB, n_clicks = 0),
                dbc.NavLink("Team Analysis", href="/team", active="exact", id = ids.TEAM_TAB, n_clicks = 0),
                dbc.NavLink("Correlation Analysis", href="/correlation", active="exact", id = ids.CORR_TAB, n_clicks = 0),
                dbc.NavLink("Strikezone Analysis", href="/strikezone", active="exact", id = ids.STRIKEZONE_TAB, n_clicks = 0),
                dbc.NavLink("wOBA Analysis", href="/woba", active="exact", id = ids.WOBA_TAB, n_clicks = 0),
                # dbc.NavLink("Custom Analysis", href="/custom", active="exact", id = ids.CUSTOM_TAB, n_clicks = 0),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H2("DATA MODIFICATION", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Upload Data", href="/upload-data", active="exact"),
                dbc.NavLink("Edit Data", href="/edit-data", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="side-bar"
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# Sidebar layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return [collapse_docs]
    elif pathname == '/team':
        return [radioMenu, teamMenu,
                timeseries_color_drop,
                timeseries_team]
    elif pathname == '/correlation':
        return [radioMenu, dateMenu, headerMenu, attrMenu, heatmap]
    # location heatmaps
    elif pathname == '/strikezone':
        return [radioMenu, dateMenu, headerMenu, grid_attrMenu, gridzone_heatmap]
    elif pathname == '/woba':
        return [radioMenu, dateMenu, headerMenu, woba_attrMenu, woba_graph]
    elif pathname == '/custom':
        return graph_container
    elif pathname == '/upload-data':
        return format_selection, upload_layout
    elif pathname == '/edit-data':
        return edit_layout
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ]
        )


# Call app server
if __name__ == '__main__':
    # set debug to false when deploying app
    app.run_server(debug=True)
