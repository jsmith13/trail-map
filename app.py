### Dash dashboard for visualizing the data.
## This is the "parent" file that lays out the dashboard, calls the data update functions, and contains the calls to run the dashboard.
## Dependent directly on config.py and callbacks.py.

# import subscripts
import config
from callbacks import register_callbacks

# import required packages
import dash
import dash_core_components as dcc
import dash_html_components as html

# initiate the dashboard
app = dash.Dash()


## define the layout of the dashboard
app.layout = html.Div(
    className = "pageContainer",
    children = [
        # page title
        html.H1(
            children = "Trail Maps",
            style = {
                "textAlign": "center",
                "color": "black"
            }
        ),

        # flex row to hold the two plots
        html.Div(
            className = "plotRow",
            children = [
                # plot of trailhead locations
                html.Div(
                    className = "plotLeft",
                    children = [
                        dcc.Graph(
                            id = "trailheads_plot",
                        ),
                    ]
                ),

                # plot of trail metrics
                html.Div(
                    className = "plotRight",
                    children = [
                        dcc.Graph(
                            id = "metrics_plot",
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
                            #step = 0.1,
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
                )
            ]
        )
    ]
)


## import the callback functions from callbacks.py
register_callbacks(app)

# run the app on local server
app.run_server(debug = True)
