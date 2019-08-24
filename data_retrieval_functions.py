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
# returns a list of longitude, latitude, name, and highest elevation of trailheads (0, 1, 2, 3)
# returns longitude and latitude to center mapbox on (4, 5)
# returns row indices (6)
def trailheads_map_update(length, difficulty, rating):   
    # subset hikes by length, difficulty, and rating
    hikes_subset = hikes.query("length >= @length[0] & length <= @length[1]")
    hikes_subset = hikes_subset.query("difficulty >= @difficulty[0] & difficulty <= @difficulty[1]")
    hikes_subset = hikes_subset.query("stars >= @rating[0] & stars <= @rating[1]")
    
    # return data from subset
    return(
        hikes_subset["longitude"],
        hikes_subset["latitude"],
        hikes_subset["name"],
        hikes_subset["high"],
        
        # longitude of center
        np.mean([hikes_subset["longitude"].min(), hikes_subset["longitude"].max()]),
        # latitude of center
        np.mean([hikes_subset["latitude"].min(), hikes_subset["latitude"].max()]),
        
        # row indices for future reference
        hikes_subset.index
    )

# function add_selected_trails
# returns a dataframe to be displayed
def add_selected_trails(selection, previous_indices):
    # build a list of indices from the current selection
    selection_indices = [i["id"] for i in selection["points"]]
       
    # merge the two lists, removing duplicate indices
    current_indices = set(selection_indices + previous_indices)
    
    # subset hikes to the selected trailheads
    hikes_selection = hikes.iloc[list(current_indices), ]
    
    # return the subsetted data and a list of current indices
    return(hikes_selection.to_dict("records"), list(current_indices))


# function remove_selected_trails
# returns a dataframe to be displayed
def remove_selected_trails(selection, previous_indices):
    # identify the row indices of the trails selected for removal
    selected_indices = hikes.iloc[previous_indices, ].index[selection]
    
    # remove those indices from previous_indices
    current_indices = set(previous_indices).difference(set(selected_indices))
    
    # subset hikes to the selected trailheads
    hikes_selection = hikes.iloc[list(current_indices), ]
    
    return(hikes_selection.to_dict("records"), list(current_indices))
