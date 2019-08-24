### Generate plots to embed in Dash dashboard
## This file provides app.py with "callback" functions that take user inputs and return data and layouts formatted to generate the appropriate plots.
## This file depends on config.py to supply API keys and data_retrieval_functions.py to provide data.

# import local dependencies
import config
import data_retrieval_functions as drf

# import required libraries
import json
import plotly.graph_objs as plgo
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# initiate a list of row indices for the data currently in the table of selected trails
hike_indices = []

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
            ids = updates[6],
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
        [Output("selected_trail_table", "data"),
        Output("selected_trail_table", "selected_rows")],
        [Input("add_selection", "n_clicks"),
        Input("remove_selection", "n_clicks")],
        [State("trailheads_plot", "selectedData"),
        State("selected_trail_table", "selected_rows")]
    )
    
    def callback_update_table(add_selection, remove_selection, trailheads_plot_selection, table_selection):
        # identify hike_indices as a global variable
        global hike_indices
        
        # initialize the table with empty data on load
        if trailheads_plot_selection is None and table_selection is None:             
            return([{}], [])
            
        # determine which button triggered this callback
        triggering_button = callback_context
        # pull the name out of the larger callback object
        triggering_button = triggering_button.triggered[0]["prop_id"].split(".")[0]
                
        # add selected trails
        if triggering_button == "add_selection":          
            # pull data on trails selected in the trailheads plot
            # update the list of indices
            updates, hike_indices = drf.add_selected_trails(trailheads_plot_selection, hike_indices)
            
            # return the data to be added and clear selection
            return(updates, [])
        
        # or remove selected trails
        if triggering_button == "remove_selection":
            # update the list of indices
            updates, hike_indices = drf.remove_selected_trails(table_selection, hike_indices)
            
            # return the data to be added and clear selection
            return(updates, [])
        
