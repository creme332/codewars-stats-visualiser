import plotly.express as px
from ast import literal_eval
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'browser'


def PieChart(source_file_name, destination_file_name):

    df = pd.read_csv(source_file_name, sep='\t')

    # create a df with 2 columns : tags, count
    df['tags'] = df['tags'].apply(literal_eval)  # convert to list type
    df = df.explode("tags")
    series = df.groupby('tags').size()
    df = series.to_frame('count')
    df = df.reset_index()

    # Represent only tags with count > 5
    df.loc[df['count'] < 3, 'tags'] = 'Other'
    fig = px.pie(df, values=df['count'], names=df['tags'],
                 title='Number of katas solved by category')
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.write_html(destination_file_name)
    # fig.show()


def AnimatedPieChart(source_file_name, destination_file_name):
    df = pd.read_csv(source_file_name, sep='\t')
    headings = df.columns  # headings of original df

    labels = df[headings[0]].tolist()  # list of ranks

    # create first frame
    # create initial frame containing only ranks and 1 language
    new_df = pd.concat((df['index'], df[df.columns[1]]), axis=1)
    new_df.drop(new_df.loc[new_df[new_df.columns[1]] ==
                0].index, inplace=True)  # drop zeroes
    values = new_df[df.columns[1]].tolist()

    # create other frames
    frames_list = []
    for i in range(1, len(df.columns)):
        new_df = pd.concat((df['index'], df[df.columns[i]]), axis=1)
        new_df.drop(new_df.loc[new_df[new_df.columns[1]] ==
                               0].index, inplace=True)  # drop zeroes
        my_data = new_df[new_df.columns[1]].tolist()

        frames_list.append(
            go.Frame(
                data=[go.Pie(labels=labels, text=labels,
                             hovertemplate="%{value} katas solved<extra></extra>",
                             title=df.columns[i],
                             values=my_data,
                             hole=.3, sort=False)])
        )
    # create fig dictionary
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # add initial data
    fig_dict["data"] = [go.Pie(labels=labels, text=labels,
                               hovertemplate="%{value} katas solved<extra></extra>",
                               title=df.columns[1],
                               values=values, hole=.3,
                               sort=False)]
    fig_dict["layout"]["title"] = "Number of katas solved" + \
        " by rank for each language"

    # create buttons for animations : Play, Pause
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 2000,
                                              "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 1000
                                                   }}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    fig_dict["frames"] = frames_list

    fig = go.Figure(fig_dict)
    fig.update_layout(legend_title_text='kata rank')

    fig.write_html(destination_file_name)

    # fig.show()
