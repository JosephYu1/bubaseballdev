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
 
'''
BAYLOR BASEBALL BANNER
'''
banner = html.Div(
            html.Img(
                src=app.get_asset_url('baylor_baseball_banner.png'), 
                style={'height':'100%', 'width': '50%'},
            ),
            style={'text-align':'center'}
        )

'''
DOCUMENTATION FOR RADIO BUTTONS
'''
radio_card = dbc.Collapse(
                dbc.Card([
                    html.H5("Radio Buttons Specifications"),
                    html.P("There are three radio buttons displayed at the top of some tabs,\
                            each of them represent a different selection of Match Type"),
                    html.H6("Private"),
                    html.P("The 'Private' radio button selects the private data from the\
                            Baylor Baseball Team games. These are practice rounds played\
                            amongst team members."),
                    html.H6("Public"),
                    html.P("The 'Public' radio button selects the public data from the\
                            Baylor Baseball Team games. These are games played against\
                            other schools."), 
                    html.H6("All"),
                    html.P("The 'All' radio button will select both private and public data")         
                ]),
                # activation of the collapse button
                id="radio-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )

'''
DOCUMENTATION FOR DROPDOWN LIST
'''
dropdown_card = dbc.Collapse(
                    dbc.Card([
                        # documentation for dropdown list attribute
                        html.H5("Things to Note When Using Dropdown Lists"),
                        html.H6("You can type to search!"),
                        html.P("The list is long, say you just want to get Pitcher, well, just type it in and you'll get it!"),
                        html.H6("What is 'All'?"),
                        html.P("When you see a [x] mark left to an option, it means you can delete it, and often times, there's\
                                an option to select 'All', literally meaning it's all the options available. However, that also\
                                means you'd need to clear it to let the system know you don't want 'All' anymore, instead use\
                                just the players you picked. For example: you start with the 'All' option in Select Players, next,\
                                you pick 'Wayne, John', but you didn't see any update yet. Once you delete the 'All' choice, you\
                                should then see updates. This applies to every dropdown list with the little [x] to the left!"),
                        html.H6("TL;DR: If you don't see update after picking new options, delete 'All'!"),
                        html.H6("Why don't I see option X/Y/Z/etc, aka, why do I only see 'BAY_BEA' and 'All' in Select Team?"),
                        html.P(f'''You may need to reset by clicking on 'All' or other options. Since the data is inter-dependable, it means\
                                that the current data is semi-locked-in. This means that since Baylor's team is selected by default, all\
                                data is now related to Baylor only. You can 'back-out' by selecting 'All' to let the system know you want\
                                to expand your selection.'''), 
                        html.H6("TL;DR: If you don't see what you want, use 'All' to step back out of the current limits!")
                        
                    ]),
                    # activation of the collapse button
                    id="drop-horizontal-collapse",
                    is_open=False,
                    style={"width": "1075px"},
                )
                

'''
DOCUMENTATION FOR input
'''
input_card = dbc.Collapse(
                    dbc.Card([
                        # documentation for input box attribute
                        html.H5("Things to Note When Using Input Boxes"),
                        html.H6("Press enter after you filled in boxes to update!"),
                        html.P("The boxes do NOT auto-update, they only updates after you press the Enter key when you finished typing."),
                        html.H6("I can't input the values I want into the box?"),
                        html.P("Each box expects a certain type of input, or a specific range of input. This means that you can't type\
                                'banana' into a box that expects a number. Or you can't exceed a reasonable range of that field, such as\
                                the input of Color Quantile of Correlation Analysis, you can only enter a number between 0 and 1, if you \
                                try to enter 23, it wouldn't work. In general, the input boxes only accepts numbers!"),
                        html.H6("Why if the variable is not number-based, can I enter non-numbers then?"),
                        html.P("Unfortunately, no. If the variable is based on words, say, Pitch Type, then you cannot filter them."),
                    ]),
                    # activation of the collapse button
                    id="input-horizontal-collapse",
                    is_open=False,
                    style={"width": "1075px"},
                )

'''
DOCUMENTATION FOR Refreshing the page
'''
refresh_card = dbc.Collapse(
                dbc.Card([
                    html.H5("Refreshing"),
                    html.H6("I don't see the data I want - too many subsets"),
                    html.P("If you ever run into the trouble of not seeing the data you expect, such as\
                            you only see data from Feb 17th, chances are you have done too many subsets (filtering)\
                            or the data. The get access to the complete data gain, simply refresh the page."),
                    html.H6("TL;DR: When in doubt, refresh."),
                ]),
                # activation of the collapse button
                id="refresh-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )


# ------------------------------
# ---------- pages -------------
# ------------------------------

                
'''
DOCUMENTATION FOR THE TEAM ATTRIBUTES ANALYSIS
'''
team_card = dbc.Collapse(
                dbc.Card([
                    # documentation for the team attribute analysis tab
                        html.H5("Team Analysis"),
                        html.P("Page for seeing how the team performs. Many of the fields are dynamic\
                                and inter-related - meaning if you update one field, the other fields will reflect the change!\
                                For example, if you started with player 'Wayne, John', then switched over to 'Charles, Ray', \
                                the Start Date and End Date may change because that John played on Feb 17 but Ray didn't."),
                        html.H6("When or why use 'Color' for grouping, aka 'How do I see more than 2D on a flat surface?'"),
                        html.P("Sometimes you want to more data... but there's only 2 axis on a chart. Using Color gives you a whole\
                                new dimension to play around!\
                                For example, if you want to see different Pitchers' SpinRate in a particular match, simply set the X\
                                axis to 'Datetime', set Y to 'SpinRate', and set Color to 'Pitcher', then you got yourself a timeseries\
                                of the Pitcher(s)' SpinRate over the match time! Oh of course, don't forget to set the Start and End Date\
                               to the correct range!")
                ]),
                # activation of the collapse button
                id="team-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )

'''
DOCUMENTATION FOR THE CORRELATION ANALYSIS 
'''
corr_card = dbc.Collapse(
                dbc.Card([
                    # documentation for the team attribute analysis tab
                    html.H5("Correlation Analysis"),
                    html.H6("How do you know if X is correlated to Y?"),
                    html.P("You can plot them against each other based on another value.\
                            For example, you want to see if how much Pitch Type and Pitch Call are related to SpinRate, then the resulting\
                            graph should tell you their relationship."),
                    html.H6("Why can't I select the same variables, aka 'Why is my graph not updating?'"),
                    html.P("Each variable MUST BE DIFFERENT. X cannot be the same as Y or Color, or Y cannot be same as\
                            X or Z... you get the point."),
                ]),
                # activation of the collapse button
                id="corr-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )

'''
DOCUMENTATION FOR THE CUSTOM ANALYSIS
'''
custom_card = dbc.Collapse(
                dbc.Card([
                    # documentation for the team attribute analysis tab
                    html.H5("Custom Analysis"),
                    html.H6("How many graphs can I add?"),
                    html.P("Theoretically, as many as your browser or Baylor's server can handle... so technically, not that many."),
                    html.H6("Why is it so slow?"),
                    html.P("Each graph loads its own data, and each data is about at least 30MB... so, it's going to be slow\
                            if you have a bunch of them. We strongly recommend you to test and play around in the Team Analysis first,\
                            then, once you found some interesting ideas you want to compare, hop over to Custom Analysis for a side-by-side\
                            view."),
                    html.H6("But seriously, why is it so slow?"),
                    html.P("Because we are writing the data into your browser's memory, meaning it sends data from the server to your\
                            browser, then whatever update you do, the server asks your browser for the data, and your browser hands it\
                            to the server. To do this, we need to convert the original data from a dataframe into a JSON file, and then when we need to edit \
                            the data, like doing filtering or selecting players, we need to convert the data back into a dataframe. And finally\
                            we need to plot the results as a graph.\
                            We chose this method to save on bandwidth. When you are, say, over in Montana, and want to\
                            use this app, the internet connection to Baylor will likely be slow. And since EACH of these data package is\
                            at least 30MB, you can imagine everytime you did a change, it'll cost a 30MB transfer if we simply load directly\
                            from the server. Therefore, by writing and saving the data to your browser, instead let your local\
                            system handle some of the data load instead of exploding your internet connection.\
                            To recap, there are 3 bottlenecks: 1. memory storing, 2. converting data, 3.\
                            plotting the graphs. If future endeavor is to be made to increase the performance, we suggest rewriting some code\
                            using Pyspark for faster computing for Issue 2. For Issue 3, we suggest either using different plotting libraries\
                            or to write your own. For issue 1, there are work-arounds but it's going to be a trade-off in some ways."),
                ]),
                # activation of the collapse button
                id="custom-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )

upload_card = dbc.Collapse(
                dbc.Card([
                    html.H5("Upload Data"),
                    html.H6("Rule 1: Make Sure The Date Format is Correct!"),
                    html.P("Since you may get your files from other schools, it's not uncommon for different schools to use different settings.\
                            By default, we assume it's in the format of YYYY\MM\DD, but many schools may use MM/DD/YYYY, and one school even \
                            used DD/MM/YYYY! Which brings us to the question: is 5/3/2023 refers to May 3rd or Mar 5th? Well, it depends on \
                            which school you got the file from and how they set their Trackman. If the date format is wrong,\
                            the system may warn you, but it may also go through (MM/DD vs DD/MM), which is bad because then you'd need to\
                            manually delete the file generated, and recreate a new file."),
                    html.H6("TL;DR: Make sure you pick the correct date format BEFORE you upload the file."),
                ]),
                # activation of the collapse button
                id="upload-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )

edit_card = dbc.Collapse(
                dbc.Card([
                    html.H5("Edit Data"),
                    html.H6("fill in"),
                    html.P("..."),
                ]),
                # activation of the collapse button
                id="edit-horizontal-collapse",
                is_open=False,
                style={"width": "1075px"},
            )


'''
DOCUMENTATION FOR THE GRIDZONE ANALYSIS TAB
'''
strikezone_card = dbc.Collapse(
                    dbc.Card([
                        # documentation on gridzone heatmaps 
                        html.H5("Graphs"),
                        html.H6("Gridzone heatmap"),
                        html.P(
                            "The gridzone heatmap is the left-hand graph in this tab. It is a zone-by-zone representation of the hits in relation to the side and height of the strikezone. \
                            The strikezone is depicted as a white square in the graph the x-axis represents the side distance from the homeplate while the y-axis represents the height distance from the homeplate."
                        ),
                        html.H6("Density heatmap"),
                        html.P(
                            "The density heatmap represents “hot” and “cold” zones in a map depending on the number of points that lay on the zone. Similar to the grizone heamtap, the x-axis represents\
                            the side distance from the homeplate while the y-axis represents the height distance from the homeplate. The strikezone is visualized as a white square on the map. "
                        ),
                        html.H5("Graph toolbar"),
                        # showcasing plotly options
                        html.P("When hovering over the graph, a Plotly-powered toolbar will show up with different options:"),
                        html.Img( 
                            src=app.get_asset_url('plotly_options.png'), 
                            style={'text-align':'center'},
                        ),
                        html.H6("Option 1"),
                        html.P(
                            "Download the image as a png"
                        ),
                        html.H6("Option 2: "),
                        html.P(
                            "Zoom into the image by using your mouse; to do so, place your mouse \
                            on the graph and drag across the area you want to zoom in while right-clicking"
                        ),
                        html.H6("Option 3: "),
                        html.P(
                            "Pan option; allows you to pan through the image by pressing your mousepad and dragging"
                        ),
                        html.H6("Option 4: "),
                        html.P(
                            "Zoom-in using default plotly mechanism; click it and the graph will be zoomed into"
                        ),
                        html.H6("Option 5: "),
                        html.P(
                            "Zoom-out using default plotly mechanism; click it and the graph will be zoomed out of"
                        ), 
                        html.H6("Option 6: "),
                        html.P(
                            "Autoscale; clicking it resets the graph into its original state"
                        ),
                        html.H6("Option 7: "),
                        html.P(
                            "Reset axes option"
                        ),
                        html.H6("Option 8: "),
                        html.P(
                            "Clicking the plotly icon takes you to the plotly documentation page, which displays \
                            information on the underlying mechanism of these graphs"
                        )
                    ]),
                    # activation of the collapse button
                    id="gridzone-horizontal-collapse",
                    is_open=False,
                    style={"width": "1075px"},
                ),

'''
DOCUMENTATION FOR WOBA ANALYSIS TAB
'''
woba_card = dbc.Collapse(
                    dbc.Card([
                        html.H5('Graphs'),
                        html.P("The wOBA distribution can be visualized in two ways, as a histogram and as a scatterplot.\
                                To toggle between this two graphs, utilize the 'Select graph' dropdown"),

                    ]),
                    # activation of the collapse button
                    id="woba-horizontal-collapse",
                    is_open=False,
                    style={"width": "1075px"},
                ),