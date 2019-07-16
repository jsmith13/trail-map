### Functions for retrieving data to be displayed or plotted from the database.
## This file subsets and formats data and passes it to plotting.py to be plotted.


# load required libraries
import pandas as pd
import numpy as np

# load the dataset from the csv file
hikes = pd.read_csv("hiking project - NWtrails (1).csv")


## data formatting functions

# function trailhead_map_update
# takes no arguments
# returns a list of longitude, latitude, and name of trailheads (0, 1, 2)
# returns longitude and latitude to center mapbox on (3, 4)
def trailhead_map_update():
    return(
            hikes["longitude"],
            hikes["latitude"],
            hikes["name"],
            
            # longitude of center
            np.mean([hikes["longitude"].min(), hikes["longitude"].max()]),
            # latitude of center
            np.mean([hikes["latitude"].min(), hikes["latitude"].max()])
    )


# function trail_metrics_update
# takes no arguments
# returns length, ascent, and integer-encoded difficulties (0, 1, 2)
def trail_metrics_update():
    return(
        hikes["length"],
        hikes["ascent"],
        
        # integer-encode difficulties
        hikes["difficulty"].apply(lambda x: {"green": 0, "greenBlue": 1, "blue": 2, "blueBlack": 3, "black": 4, "dblack": 5}[x])
    )

