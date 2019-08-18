### Functions for retrieving data to be displayed or plotted from the database.
## This file subsets and formats data and passes it to plotting.py to be plotted.


# load required libraries
import pandas as pd
import numpy as np

# load the dataset from the csv file
hikes = pd.read_csv("hiking project - NWtrails (1).csv")

# integer encode difficulty
hikes["difficulty"] = hikes["difficulty"].apply(lambda x: {"green": 0, "greenBlue": 1, "blue": 2, "blueBlack": 3, "black": 4, "dblack": 5}[x])

## data formatting functions

# function trailheads_map_update
# takes no arguments
# returns a list of longitude, latitude, and name of trailheads (0, 1, 2)
# returns longitude and latitude to center mapbox on (3, 4)
def trailheads_map_update(length, difficulty):   
    # subset hikes by length and difficulty
    hikes_subset = hikes.query("length >= @length[0] & length <= @length[1]")
    hikes_subset = hikes_subset.query("difficulty >= @difficulty[0] & difficulty <= @difficulty[1]")
    
    # return data from subset
    return( 
        hikes_subset["longitude"],
        hikes_subset["latitude"],
        hikes_subset["name"],

        # longitude of center
        np.mean([hikes_subset["longitude"].min(), hikes_subset["longitude"].max()]),
        # latitude of center
        np.mean([hikes_subset["latitude"].min(), hikes_subset["latitude"].max()])
    )


# function trail_metrics_update
# takes no arguments
# returns length, ascent, and integer-encoded difficulties (0, 1, 2)
def trail_metrics_update(length, difficulty, trailheads_selection):
    # subset down to just the trails selected in the trailhead plot
    if trailheads_selection is not None:
        selected_trails = [i["pointIndex"] for i in trailheads_selection["points"]]
        hikes_subset = hikes.iloc[selected_trails, ]
    else:
        # don't subset if a selection has yet to be made
        hikes_subset = hikes

    # subset hikes by length and difficulty
    hikes_subset = hikes_subset.query("length >= @length[0] & length <= @length[1]")
    hikes_subset = hikes_subset.query("difficulty >= @difficulty[0] & difficulty <= @difficulty[1]")
    
    # return data from subset
    return(
        hikes_subset["length"],
        hikes_subset["ascent"],
        hikes_subset["name"],
        hikes_subset["difficulty"]
    )

