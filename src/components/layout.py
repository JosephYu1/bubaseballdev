from dash import Dash, html
from dash import Dash, dcc, html
from . import dropdown_players, dropdown_attributes, heatmap_attributes # the "." means relative import
from . import ids, data

# helpful documentation on layout
# https://dash.plotly.com/layout

# call to the render file with the IDs, see *.py files in components

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className = "app-div",
        children=[
            html.H1(app.title),
             # TABS FOR GRAPHS 
             # Each graph has different dropdown requirements
                # - Attributes heatmap needs the x, y, and z 
                # - Strikezone location only needs z to be updated
            html.Div([
                dcc.Tabs(
                    # id and value designation for graph segment
                    id = 'graph-tabs', value = 'location-tab',
                    children = [
                        # tab for strikezone location heatmap
                        dcc.Tab(
                            label = 'Strikezone Location Heatmap', 
                            value = 'location-tab',
                            children = [
                                html.Div(
                                    className = 'dropdown-locations',
                                    children = [
                                        dropdown_players.render(app) # same name as the .py file
                                    ],
                                    style = {'background-color': 'rgb(120, 120, 120)'}    
                                ),                     
                            ]
                        ),

                        # tab for attributes heatmap 
                        dcc.Tab(
                            label = 'Attributes Heatmap',
                            value = 'attributes-tab',
                            children= [
                                # FIXME: THIS CODE CHUNK PRODUCES REDUNDANCY
                                #        THE GRAPHS ARE NOT LOADING DUE TO 
                                #        HAVING MORE THAN ONE DROPDOWN
                                # dropdown + graph need to be children of 
                                # tab                    
                                # using render() here
                                html.Div(
                                    className = "dropdown-container",
                                    children = [
                                        dropdown_players.render(app) # same name as the .py file
                                    ],
                                    style = {'background-color': 'rgb(120, 120, 120)',
                                            }
                                ),

                                html.Div(
                                    className = "dropdown-container-attr",
                                    children = [
                                        dropdown_attributes.render(app)
                                    ],
                                    style = {'background-color': 'rgb(120, 120, 120)',
                                            #  'color': 'rgb(250, 250, 250)'
                                            },
                                ),

            # select data source
            html.H4("Select data type: "),
            html.Div(
                className= "radiobuttons-data",
                children = [
                    dcc.RadioItems(
                        id = ids.RADIO_DATA,
                        options = [
                            {
                                'label' : "All",
                                'value' : "All"
                            },
                            {
                                'label' : "Private Only", 
                                'value' : "Private"
                            },
                            {
                                'label' : "Public Only", 
                                'value' : "Public"
                            },
                        ],
                        value = "All",
                        inline = True,
                        # For padding: https://community.plotly.com/t/styling-radio-buttons-and-checklists-spacing-between-button-checkbox-and-label/15224/2
                        # NOTE: style={} changes other things, margin options works differently there
                        inputStyle={"margin-right": "5px", 
                                    "margin-left": "5px"}
                    )
                ]
            ),
            html.Hr(),

            # using render() here
            html.Div(
                className = "dropdown-container",
                children = [
                    html.H4("Select Player:"),
                    dropdown_players.render(app) # same name as the .py file
                ],
                style = {'background-color': 'rgb(120, 120, 120)',
                        #  'color': 'rgb(250, 250, 250)'
                         }
            ),

            html.Div(
                className = "dropdown-container-attr",
                children = [
                    dropdown_attributes.render(app)
                ],
                style = {'background-color': 'rgb(120, 120, 120)',
                        #  'color': 'rgb(250, 250, 250)'
                         },
            ),

                            ]
                        )
                    ]

                ),
            ]),
            html.Hr(),

            # add heatmap here
            heatmap_attributes.render(app)
            
        ]
    )