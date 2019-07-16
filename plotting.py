### Generate plots to embed in Dash dashboard
## This file provides app.py with data and layouts formatted to generate the appropriate plots.
## This file depends on config.py to supply API keys and data_retrieval_functions.py to provide data.

# import local dependencies
import config
import data_retrieval_functions as drf

# import required libraries
import plotly.graph_objs as plgo


## plotting functions

# function trailhead_map
# takes no arguments
# returns parameters for generating the trailhead plot
def trailhead_map():
    # collect updated data from data_retrieval_functions.py
    updates = drf.trailhead_map_update()
    
    # define data assignments
    data = [dict(
        type = "scattermapbox",
        mode = "markers",
        lon = updates[0], 
        lat = updates [1], 
        text = updates[2]
    )]

    # define plot layout
    layout = plgo.Layout(
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
    
    # return data and layout in a dictionary
    return(
        {"data": data, 
         "layout": layout}
    )


# function trail_metrics
# takes no arguments
# returns parameters for generating the trail metric plot
def trail_metrics():
    # collect updated data from data_retrieval_functions.py
    updates = drf.trail_metrics_update()
    
    # define data assignments
    data = [dict(
        type = "scatter",
        mode = "markers",
        x = updates[0],
        y = updates[1],

        # color markers by hike difficulty
        marker = dict(
            color = updates[2],
            colorscale = [[0.0, "green"], [0.5, "blue"], [1.0, "black"]]
        )
    )]

    # define plot layout
    layout = plgo.Layout(
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

    # return data and layout in a dictionary
    return({"data": data, "layout": layout})
