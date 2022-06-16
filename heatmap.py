# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 20:29:58 2022

@author: user
"""

# =============================================================================
# Purpose : Create a heatmap and save it as png image
# =============================================================================
import pandas as pd
import numpy as np
import calplot
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'


def BasicHeatmap(single_year, source_file_name, destination_file_name):

    df = pd.read_csv(source_file_name, sep='\t')
    df['Date'] = pd.to_datetime(df['Date'])

    # for more uniform color distribution use a log scale
    df['DateValue'] = np.log10(df['DateValue'])
    # note : all values in DateValue column are at least 1

    if single_year == -1:  # plot for all years
        # create a series
        column_headings = df.columns
        my_dates = df[column_headings[0]].tolist()
        my_data = df[column_headings[1]].tolist()
        my_series = pd.Series(data=my_data, index=my_dates)
        # plot
        calplot.calplot(data=my_series, figsize=(16, 8),
                        suptitle='Number of katas solved')
    else:  # single year

        # filter dataframe by year
        df = df[df['Date'].dt.year == single_year]

        if df.empty:
            print("No data available for", single_year)
            return
        # create a series
        column_headings = df.columns
        my_dates = df[column_headings[0]].tolist()
        my_data = df[column_headings[1]].tolist()
        my_series = pd.Series(data=my_data, index=my_dates)

        calplot.calplot(data=my_series, figsize=(16, 8),
                        suptitle='Number of katas solved')

    # save file
    plt.savefig(destination_file_name, bbox_inches='tight')


def InteractiveHeatmap(source_file_name, destination_file_name):
    df = pd.read_csv(source_file_name, sep='\t')

    column_headings = df.columns
    labels = df[column_headings[0]].tolist()  # ranks
    data = []
    for i in range(1, len(df.columns)):
        # replace 0s by 1s to prevent div by 0 when taking log
        df[column_headings[i]].replace(0, 1, inplace=True)
        data.append(df[column_headings[i]].tolist())

    # for more uniform color distribution use a log scale
    data = np.log10(data)
    fig = px.imshow(data,
                    labels=dict(x="Kata rank", y="language",
                                color="log(kata count)"),
                    y=column_headings[1:],
                    x=labels
                    )
    fig.update_xaxes(side="top")
    fig.write_html(destination_file_name)

    # fig.show()
