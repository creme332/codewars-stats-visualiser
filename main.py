from codewars_data_collection import CollectData
from heatmap import BasicHeatmap, InteractiveHeatmap
from piechart import InteractivePieChart
from timeseries import CreateTimeSeries
import time


def main(user):
    source_file_name = "data/" + str(user) + "_"
    destination_file_name = 'charts/' + str(user)

    start_time = time.time()
    CollectData(user)
    print("--- %s seconds ---" %
          (time.time() - start_time))

    # create charts

    # To generate activity heatmap of all available years
    BasicHeatmap(-1, source_file_name + "language_date_count",
                 destination_file_name +
                 "basicheatmap1.png")

    CreateTimeSeries(source_file_name + "language_date_count",
                     destination_file_name +
                     "timeseries.html")

    # To generate activity heatmap of 2022 only
    BasicHeatmap(2022, source_file_name + "language_date_count",
                 destination_file_name +
                 "basicheatmap2.png")
    InteractiveHeatmap(source_file_name + "language_rank_count",
                       destination_file_name +
                       "interactiveheatmap.html")
    InteractivePieChart(source_file_name + "language_rank_count",
                        destination_file_name +
                        "interactivepiechart.html")


main('creme332')
