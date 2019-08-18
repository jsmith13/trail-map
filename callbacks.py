### Generate plots to embed in Dash dashboard
## This file provides app.py with "callback" functions that take user inputs and return data and layouts formatted to generate the appropriate plots.
## This file depends on config.py to supply API keys and data_retrieval_functions.py to provide data.

# import local dependencies
import config
import data_retrieval_functions as drf

# import required libraries
import plotly.graph_objs as plgo
from dash.dependencies import Input, Output, State


## this function is a wrapper to allow the callbacks to be imported into app.py
def register_callbacks(app):

    ### update functions
    ## updates the trailheads plot
    @app.callback(
        Output("trailheads_plot", "figure"),
        [Input("length_slider", "value"),
        Input("difficulty_slider", "value")]
    )
    
    def callback_update_trailheads_plot(length, difficulty):
        # convert length out of logrithmic scale
        length = [10 ** i for i in length]
        
        # collect updated data from data_retrieval_functions.py
        updates = drf.trailheads_map_update(length, difficulty)

        # define data assignments
        data_trailheads_plot = [dict(
            type = "scattermapbox",
            mode = "markers",
            lon = updates[0], 
            lat = updates [1], 
            text = updates[2]
        )]

        # define plot layout
        layout_trailheads_plot = plgo.Layout(
            title = "It's a Map",
            autosize = False,
            width = 800,
            height = 800,

            # map location and orientation
            mapbox = plgo.layout.Mapbox(
                accesstoken = config.mapbox_api_key,
                bearing = 0,
                center = plgo.layout.mapbox.Center(
                    lon = updates[3],
                    lat = updates[4]
                ),

                # map perspective
                pitch = 0,
                zoom = 6
            )
        )
        
        # return data and layout for the trailhead plots in a dictionary
        return(
            {"data": data_trailheads_plot, "layout": layout_trailheads_plot}
        )
        
    
    ## updates the trail metrics plot
    @app.callback(
        Output("metrics_plot", "figure"),
        [Input("length_slider", "value"),
        Input("difficulty_slider", "value"),
        Input("trailheads_plot", "selectedData")]
    )
    
    def callback_widgets_update_metrics(length, difficulty, trailheads_selection):
        # convert length out of logrithmic scale
        length = [10 ** i for i in length]
        
        # collect updated data from data_retrieval_functions.py
        updates = drf.trail_metrics_update(length, difficulty, trailheads_selection)

        # define data assignments
        data_metrics_plot = [dict(
            type = "scatter",
            mode = "markers",
            x = updates[0],
            y = updates[1],
            text = updates[2],

            # color markers by hike difficulty
            marker = dict(
                color = updates[3],
                colorscale = [[0.0, "green"], [0.5, "blue"], [1.0, "black"]]
            )
        )]

        # define plot layout
        layout_metrics_plot = plgo.Layout(
            title = "It's a Scatterplot",
            autosize = False,
            width = 800,
            height = 800,

            # define axis parameters
            xaxis = dict(
                type = "log",
                title = "distance (miles)"
            ),

            yaxis = dict(
                type = "log",
                title = "elevation gain (feet)"
            )
        )

        # return data and layout for the metrics plot in a dictionary
        return(
            {"data": data_metrics_plot, "layout": layout_metrics_plot}
        )
        
    