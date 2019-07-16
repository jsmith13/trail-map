### Dash dashboard for visualizing the data.

# import subscripts
import config
import data_retrieval_functions
import plotting

# import required packages
import dash
import dash_core_components as dcc
import dash_html_components as html


# initiate the dashboard
app = dash.Dash()

# define the layout of the dashboard
app.layout = html.Div(
    className = "container",
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
                            id = "trailheads",
                            figure = plotting.trailhead_map()
                        ),
                    ]
                ),

                # plot of trail metrics
                html.Div(
                    className = "plotRight",
                    children = [
                        dcc.Graph(
                            id = "metrics",
                            figure = plotting.trail_metrics()
                        )
                    ]
                )
            ]    
        ),
        
        # flex row to hold the inputs
        html.Div(
            className = "inputRow",
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
                            marks = [
                                {"label": "Green", "value": 0},
                                {"label": "Green/Blue", "value": 1},
                                {"label": "Blue", "value": 2},
                                {"label": "Blue/Black", "value": 3},
                                {"label": "Black", "value": 4},
                                {"label": "Double Black", "value": 5}
                            ]
                        )
                    ]
                ),
                
                # a slider to select trail length
                html.Div(
                    className = "inputLengthSlider",
                    children = [
                        html.Label("Length"),
                        dcc.Slider(
                            id = "length_slider",
                            min = 0,
                            max = 100,
                            step = 0.5,
                            value = [0, 100],
                            marks = [
                                {"label": 0, "value": 0},
                                {"label": 100, "value": 100}
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# run the app on local server
app.run_server()

