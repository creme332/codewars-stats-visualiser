# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 20:29:58 2022

@author: user
"""

import requests
import json
import pandas as pd
import datetime as dt
import numpy as np


import calplot
import calmap
import matplotlib.pyplot as plt

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"


def get_kata_rank(kata_id):  # returns the rank of a kata as a string
    url = 'https://www.codewars.com/api/v1/code-challenges/' + kata_id
    input_json = requests.get(url).text
    input_dict = json.loads(input_json)
    return input_dict["rank"]["name"]


def CollectData(user):
    date_count = {}  # stores date and number of katas solved on that date
    language_rank_count = {}
# =============================================================================
# language_rank_count : each cell is the number of problems solved
# =============================================================================
#             1 kyu  2 kyu  3 kyu  4 kyu  5 kyu  6 kyu  7 kyu  8 kyu
# python          5      2      0      0      0      0      0      0
# javascript      1      5      0      0      0      0      0      9
# =============================================================================
    for page in range(0, 100):
        input_json = requests.get('http://www.codewars.com/api/v1/users/' +
                                  user +
                                  '/code-challenges/completed?page=' +
                                  str(page)).text
        input_dict = json.loads(input_json)
        try:
            data = (input_dict["data"])  # list
        except KeyError:
            print("ERROR : Invalid name probably.")
            return False
        else:
            if len(data) == 0:  # no more data to extract
                break
            for x in range(0, len(data)):  # for each kata solved

                # extract date data
                full_date = data[x]["completedAt"]  # YYYY-MM-DD TIME
                date = full_date[0:10]  # YYYY-MM-DD
                date_count[date] = date_count[date] + \
                    1 if date in date_count else 1

                # find rank of current kata
                kata_rank = get_kata_rank(data[x]["id"])

                # extract list of completed languages for current kata
                completedLanguages = data[x]["completedLanguages"]

                # update frequency for language-rank relationship
                for lang in completedLanguages:
                    if lang in language_rank_count.keys():
                        language_rank_count[lang][kata_rank] += 1
                    else:
                        rank_frequency = {
                            '1 kyu': 0, '2 kyu': 0,
                            '3 kyu': 0, '4 kyu': 0,
                            '5 kyu': 0, '6 kyu': 0,
                            '7 kyu': 0, '8 kyu': 0,
                        }
                        rank_frequency[kata_rank] = 1
                        language_rank_count[lang] = rank_frequency

    # convert date_count dictionary to dataframe
    date_df = pd.DataFrame(date_count.items(), columns=['Date', 'DateValue'])

    # convert language_rank_count dictionary to dataframe
    lang_df = pd.DataFrame.from_dict(language_rank_count, orient='index')

    # save dataframes as csv files to data folder
    file_name = "data/" + str(user) + "_language_date_count"
    date_df.to_csv(file_name, sep='\t', encoding='utf-8-sig', index=False)

    file_name = "data/" + str(user) + "_language_rank_count"
    lang_df.to_csv(file_name, sep='\t', encoding='utf-8-sig', index=False)

    return True


def CreateHeatmap(file_name):

    df = pd.read_csv(file_name, sep='\t')
    df['Date'] = pd.to_datetime(df['Date'])
    # for more uniform color distribution
    df['DateValue'] = np.log10(df['DateValue'])

    # filter dates by year
# =============================================================================
#     year = 2021
#     df = df[df['Date'].dt.year == year]
# =============================================================================

    # create a series
    column_headings = df.columns
    my_dates = df[column_headings[0]].tolist()
    my_data = df[column_headings[1]].tolist()
    my_series = pd.Series(data=my_data, index=my_dates)

    # create heatmap of all years
# =============================================================================
    calplot.calplot(data=my_series)
# =============================================================================

    # create heatmap of a single year
    # use filter dates first
# =============================================================================
#     calmap.yearplot(data=hs)
# =============================================================================
    # plt.figure(figsize=(16, 8))
    plt.suptitle('katas completed', fontsize=20, y=1.1)
    plt.savefig("test", bbox_inches='tight')


def CreateTimeSeries(file_name):
    df = pd.read_csv(file_name, sep='\t')
    df['Date'] = pd.to_datetime(df['Date'])
    # fig = px.line(df, x='Date', y="DateValue")
    # fig = go.Figure([go.Scatter(x=df['Date'], y=df['DateValue'])])

    fig = px.line(df, x="Date", y=df.columns,
                  hover_data={"Date": "|%B %d, %Y"},
                  title='Number of katas solved',
                  )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period",
        rangeslider_visible=True,  # time slider
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])))

    fig.write_html(
        "interactivegraph.html")
    # fig.write_image(destination_path + ".pdf")  # .svg or .pdf
    fig.show()


def main():
    user = 'Voile'
    file_name = str(user) + "Data"
    # success = CollectData(user)
    success = True  # falsetru, Sm1l3z, Voile
    if success:
        # CreateHeatmap(file_name)
        CreateTimeSeries(file_name)


CollectData('creme332')
# main()
