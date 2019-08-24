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

        # flex row to hold the plot and filtering sliders
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
                    ],
                    
                    style = {"width": "900px", "height": "900px"}
                ),
                
                # a flex column to hold the input sliders
                html.Div(
                    className = "sliderColumn",
                    children = [
                        
                        # pad this column down in line with the plot
                        html.Div(
                            children = [
                                html.H2(
                                    children = "1) Use the sliders to filter.",
                                ),
                            ],
                            
                            style = {"padding-top": "80px"}
                        ),
                        
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
                            ],
                            
                            style = {"width" : "300px", "height": "100px", "padding-top": "20px"}
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
                            ],
                            
                            style = {"width" : "300px", "height": "100px"}
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
                                        0: {"label": "Unrated"},
                                        1: {"label": "1"},
                                        2: {"label": "2"},
                                        3: {"label": "3"},
                                        4: {"label": "4"},
                                        5: {"label": "5"}
                                    }
                                )
                            ],
                            
                            style = {"width" : "300px", "height": "100px"}
                        ),
                        
                        html.H2(
                            children = "2) Select trails on the map."
                        ),
                        
                        html.H2(
                            children = "3) Add to the chart below."
                        ),
                        
                        # a button to add selected trails to the table
                        html.Button(
                            "Add Selected Trails", 
                            id = "add_selection",
                            style = {"width": "175px"}
                        ),
                        
                        html.H2(
                            children = "4) To remove trails, select them in the table."
                        ),
                        
                        # a button to remove trails from the table
                        html.Button(
                            "Remove Selected Trails",
                            id = "remove_selection",
                            style = {"width": "175px"}
                        )

                    ]
                )
                
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
                    page_size = 500,
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
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_table = {
                        "minWidth'": "900px",
                        "width": "900px",
                        "maxWidth": "900px",
                        "maxHeight": "500px",
                        "overflowY": "scroll"
                    }
                )
            ]
        )
    ],
    
    # define total width of app
    style = {"width": "1200px"}
)


## import the callback functions from callbacks.py
register_callbacks(app)

# run the app on local server
app.run_server(debug = False)
