

from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from src import components

# NOTE: Previous stylesheet
# external_stylesheets=[dbc.themes.MINTY]
# app = Dash(external_stylesheets=[dbc.themes.FLATLY]) #input can be a list
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
        meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'},],)
srv = app.server
app.title = "Baylor Baseball Data Analysis"

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True
# app.layout = create_layout(app) # optional?