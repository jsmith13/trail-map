### Generate plots to embed in Dash dashboard
## This file provides app.py with "callback" functions that take user inputs and return data and layouts formatted to generate the appropriate plots.
## This file depends on config.py to supply API keys and data_retrieval_functions.py to provide data.

# import local dependencies
import config
import data_retrieval_functions as drf

# import required libraries
import plotly.graph_objs as plgo
from dash.dependencies import Input, Output, State

# initiate a tracker for the number of clicks on each button in the interface
n_clicks_tracker = {"add": 0, "remove": 0}

# initiate a list of hike_IDs for the data currently in the table of selected trails
hike_IDs = []

## this function is a wrapper to allow the callbacks to be imported into app.py
def register_callbacks(app):

    ### update functions
    ## updates the trailheads plot
    @app.callback(
        Output("trailheads_plot", "figure"),
        [Input("length_slider", "value"),
        Input("difficulty_slider", "value"),
        Input("rating_slider", "value")]
    )
    
    def callback_update_trailheads_plot(length, difficulty, rating):
        # convert length out of logrithmic scale
        length = [10 ** i for i in length]
        
        # collect updated data from data_retrieval_functions.py
        updates = drf.trailheads_map_update(length, difficulty, rating)

        # define data assignments
        data_trailheads_plot = [dict(
            type = "scattermapbox",
            mode = "markers",
            lon = updates[0], 
            lat = updates [1], 
            text = updates[2],
            
            # color markers by maximum altitude
            marker = dict(
                color = updates[3],
                colorscale = [[0.0, "violet"], [1.0, "blue"]]
            )
        )]

        # define plot layout
        layout_trailheads_plot = plgo.Layout(
            #title = "It's a Map",
            autosize = False,
            width = 800,
            height = 800,
            
            # map location and orientation
            mapbox = plgo.layout.Mapbox(
                accesstoken = config.mapbox_api_key,
                bearing = 0,
                center = plgo.layout.mapbox.Center(
                    lon = updates[4],
                    lat = updates[5]
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
        
    
    ## updates the table of selected trails
    @app.callback(
        Output("selected_trail_table", "data"),
        [Input("add_selection", "n_clicks"),
        Input("remove_selection", "n_clicks")],
        [State("trailheads_plot", "selectedData")]
    )
    
    def callback_update_table(add_selection, remove_selection, selection):
        # identify hike_IDs as a global variable
        global hike_IDs
        
        # check to see if selection is empty
        if selection is not None:
            # pull data on trails selected in the trailheads plot
            # update the list of indices
            updates, hike_IDs = drf.add_selected_trails(selection, hike_IDs)
                        
            # return the data to be added
            return(updates)
        
        # if selection is empty, return empty data
        else:
            return([{}])
    
    