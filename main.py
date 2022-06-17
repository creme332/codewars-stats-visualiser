from dataminer import ExtractKataInfo, ExtractCompletedChallenges
from heatmap import BasicHeatmap, InteractiveHeatmap
from piechart import AnimatedPieChart, PieChart
from timeseries import TimeSeries
from barchart import HorizontalBarChart
import time

import ast
import plotly.express as px
from ast import literal_eval
import pandas as pd
import csv

def create_language_rank_df(compkatas_path, katainfo_path, destination_filename):
    # NOTE: Must find a more efficient way of getting this data.

    # 2 files required : katainfo and compkatas

    # Step 1 : Create a df with columns : id, rank
    # https://stackoverflow.com/a/58155933/17627866
    df = pd.read_csv(katainfo_path, sep='\t')
    ser = df["rank"].astype('str')
    ser = ser.apply(lambda x: ast.literal_eval(x))
    df2 = ser.apply(pd.Series)
    df2.rename(columns={'name': 'rankname'}, inplace=True)
    df = pd.concat((df['id'], df2['rankname']), axis=1)

    # Step 2 : Create a df with columns : id, completedlang
    df2 = pd.read_csv(compkatas_path, sep='\t')
    df2 = pd.concat((df2['id'], df2['completedLanguages']), axis=1)

    # Step 3 : Merge dfs from step 1, 2 using id as primary key
    df = pd.merge(df, df2, on="id")
    df.drop('id', axis=1, inplace=True)

    # Step 4 : Explode column of completedLanguages to get rid of list
    df['completedLanguages'] = df['completedLanguages'].apply(
        literal_eval)  # convert to list type
    df = df.explode("completedLanguages")

    # Step 5 : Gather required info in a dictionary
    df = df.reset_index()  # make sure indexes pair with number of rows
    language_rank_count = {}

    for index, row in df.iterrows():
        lang = row['completedLanguages']
        kata_rank = row['rankname']
        if lang in language_rank_count.keys():
            language_rank_count[lang][kata_rank] += 1
        else:
            rank_frequency = {
                '1 kyu': 0, '2 kyu': 0, '3 kyu': 0, '4 kyu': 0,
                '5 kyu': 0, '6 kyu': 0, '7 kyu': 0, '8 kyu': 0
            }
            rank_frequency[kata_rank] = 1
            language_rank_count[lang] = rank_frequency

    lang_df = pd.DataFrame.from_dict(language_rank_count)
    lang_df = lang_df.reset_index()
    lang_df.to_csv(destination_filename, sep='\t',
                   encoding='utf-8-sig', index=False)


def main(user):
    compkatas_path = "data/" + str(user) + "_" + "compkatas"
    katainfo_path = "data/" + str(user) + "_" + "katainfo"
    lang_rank_path = "data/" + str(user) + "_" + "langrank"
    
    start_time = time.time()
    # save compkata file to compkatas_path
    ExtractCompletedChallenges(user, compkatas_path)

    # use data from compkatas_path and save new file to katainfo_path
    ExtractKataInfo(compkatas_path, katainfo_path)

    print("--- %s seconds ---" % (time.time() - start_time))

    # create charts

    # Generate charts from compkatas_path
    BasicHeatmap(-1, compkatas_path, "charts/basicheatmap1.png")
    BasicHeatmap(2021, compkatas_path, "charts/basicheatmap2.png")
    TimeSeries(compkatas_path, "charts/timeseries.html")

    # Generate charts from katainfo_path
    PieChart(katainfo_path, "charts/pie1.html")
    HorizontalBarChart(katainfo_path, 'charts/bar.html')

    # Generate charts from both compkatas_path and katainfo_path
    create_language_rank_df(compkatas_path, katainfo_path,
                            lang_rank_path)
    AnimatedPieChart(lang_rank_path, "charts/pie2.html")
    InteractiveHeatmap(lang_rank_path, "charts/heatmap2.html")


main('your username here')
