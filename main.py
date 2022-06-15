# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:45:47 2022

@author: user
"""

from codewars_data_collection import CollectData
from heatmap import BasicHeatmap, InteractiveHeatmap

import time


def main(user):
    source_file_name = "data/" + str(user) + "_"
    destination_file_name = 'charts/' + str(user)

    # success = CollectData(user)
    success = True  # falsetru, Sm1l3z, Voile, manashi
    if success:
        BasicHeatmap(-1, source_file_name + "language_date_count",
                     destination_file_name +
                     "basicheatmap1.png")
        BasicHeatmap(2022, source_file_name + "language_date_count",
                     destination_file_name +
                     "basicheatmap2.png")
        InteractiveHeatmap(source_file_name + "language_rank_count",
                           destination_file_name +
                           "interactiveheatmap.html")


user = 'manashi'
start_time = time.time()
main(user)
# CollectData(user)
print("--- %s seconds ---" %
      (time.time() - start_time))  # 112 secs for  (no rate limits)
