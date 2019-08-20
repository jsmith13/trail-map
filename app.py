### Dash dashboard for visualizing the data.
## This is the "parent" file that lays out the dashboard, calls the data update functions, and contains the calls to run the dashboard.
## Dependent directly on config.py and callbacks.py.

# import subscripts
import config
from callbacks import register_callbacks

# import required packages
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import math

# initiate the dashboard
app = dash.Dash()


## define the layout of the dashboard
app.layout = html.Div(
    className = "pageContainer",
    children = [
        # page title
        html.H1(
            children = "Trails of Western Washington",
            style = {
                "textAlign": "center",
                "color": "black"
            }
        ),

        # flex row to hold the plot and table
        html.Div(
            className = "plotRow",
            children = [
                # plot of trailhead locations
                html.Div(
                    className = "plotTrailheads",
                    children = [
                        dcc.Graph(
                            id = "trailheads_plot"
                        )
                    ]
                ),
                
                # flex column to hold the table and its buttons
                html.Div(
                    className = "tableColumn",
                    children = [
                        # flex row to hold the buttons
                        html.Div(
                            className = "tableButtonsRow",
                            children = [
                                html.Button("Add Selected Trails", id = "add_selection"),
                                html.Button("Remove Selected Trails", id = "remove_selection")
                            ]
                        ),
                        
                        # table of selected trails
                        html.Div(
                            className = "trailTable",
                            children = [
                                dash_table.DataTable(
                                    id = "selected_trail_table",
                                    columns = [
                                        {"name": "Trail", "id": "name"},
                                        {"name": "Location", "id": "location"},
                                        {"name": "Miles", "id": "length"},
                                        {"name": "Climb", "id": "ascent"},
                                        {"name": "Rating", "id": "stars"}
                                    ],
                                    export_format = "csv",
                                    export_headers = "names",
                                    page_size = 20,
                                    row_selectable = "multi",
                                    sort_action = "native",
                                    sort_mode = "multi",
                                    
                                    # style table
                                    style_as_list_view = True,
                                    style_cell = {"textAlign": "left"},
                                    style_data_conditional = [
                                        {"if": {"row_index": "odd"}, 
                                         "backgroundColor" : "rgb(248, 248, 248)"}
                                    ],
                                    style_header = {
                                        "backgroundColor": "rgb(230, 230, 230)",
                                        "fontWeight": "bold"
                                    },
                                    style_table = {"width": "800px", "height": "800px"}
                                )
                            ]
                        )
                    ]
                )
            ]    
        ),
        
        # a flex row to hold the difficulty and length sliders
        html.Div(
            className = "sliderRow",
            children = [
                # a slider to select hike difficulty
                html.Div(
                    className = "inputDifficultySlider",
                    children = [
                        html.Label("Difficulty"),
                        dcc.RangeSlider(
                            id = "difficulty_slider",
                            min = 0,
                            max = 5,
                            step = 1,
                            value = [0, 5],
                            marks = {
                                0: {"label": "Green"},
                                1: {"label": "Green/Blue"},
                                2: {"label": "Blue"},
                                3: {"label": "Blue/Black"},
                                4: {"label": "Black"},
                                5: {"label": "Double Black"}
                            }
                        )
                    ]
                ),

                # a slider to select trail length
                html.Div(
                    className = "inputLengthSlider",
                    children = [
                        html.Label("Length"),
                        dcc.RangeSlider(
                            id = "length_slider",
                            min = 0,
                            max = 2,
                            step = 0.05,
                            value = [0, 2],
                            marks = {
                                0: {"label": "1"},
                                0.30103: {"label": "2"},
                                0.4771213: {"label": "3"},
                                0.60206: {"label": "4"},
                                0.69897: {"label": "5"},
                                1: {"label": "10"},
                                1.176091: {"label": "15"},
                                1.30103: {"label": "20"},
                                1.69897: {"label": "50"},
                                2: {"label": "100"}
                            }
                        )
                    ]
                ),
                
                # a slider to select trail rating
                html.Div(
                    className = "inputRatingSlider",
                    children = [
                        html.Label("Rating"),
                        dcc.RangeSlider(
                            id = "rating_slider",
                            min = 0,
                            max = 5,
                            step = 1,
                            value = [0, 5],
                            marks = {
                                0: {"label": "0"},
                                1: {"label": "1"},
                                2: {"label": "2"},
                                3: {"label": "3"},
                                4: {"label": "4"},
                                5: {"label": "5"}
                            }
                        )
                    ]
                )
            ]
        )
    ]
)


## import the callback functions from callbacks.py
register_callbacks(app)

# run the app on local server
app.run_server(debug = True)
