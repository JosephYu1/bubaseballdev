from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids, data
import numpy as np

# we call this render function in layout

DEBUG = True

cur_players = data.PLAYERS_ALL

def render(app: Dash) -> html.Div:
    # this callback is to output to the options of the dropdown function, because if we do just id at high level, the app can't see the update.
    # And if we do output as children, it's meaningless and very messy. And if we do value update, it doesn't work because the value is 
    # chosen by the dropdown and feed into heatmap.
    # Therefore, it's a better choice to update the option.
    # See: https://community.plotly.com/t/updating-a-dropdown-menus-contents-dynamically/4920
    @app.callback(
        Output(ids.DROPDOWN_PLAYERS, "options"),
        Input(ids.RADIO_DATA, "value")
    )
    def update_players(radio_option):
        print(radio_option)
        # declare variables first
        if radio_option == "All":
            cur_players = data.PLAYERS_ALL
        elif radio_option == "Private":
            cur_players = data.PLAYERS_PRIVATE
        else:
            cur_players = data.PLAYERS_PUBLIC

        if DEBUG:
            print("-------------")
            print(f'''current players:\n{cur_players}''')
            print("-------------")

        return [{"label" : p, "value": p} for p in cur_players]

    # create callback to capture button click of the button, and use that output to set values in the dropdown menu
    # for adding a button or something to update chart using @app.callback()

    # the input into this function will be the number of clicks, which is an int,
    # and output the list of string of nations, which is the value of the dropdown
    return html.Div(
            children = [
                # dropdown function
                dcc.Dropdown(
                    id = ids.DROPDOWN_PLAYERS, # having the id here works, because it knows when and where to update
                    # to refer to this dropdown to get the values, we need a list of IDs, see ids_test.py
                    # id = ids.DROPDOWN_PLAYERS,
                    options = [{"label" : p, "value": p} for p in cur_players], # list comprehension for selection options
                    value = cur_players[0], # initial value of the dropdown
                    # multi = True # more than one selection
                    # can also make this not clearable
                ),
            ]
        )