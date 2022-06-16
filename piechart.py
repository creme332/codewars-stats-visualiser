import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'browser'


def InteractivePieChart(source_file_name, destination_file_name):
    df = pd.read_csv(source_file_name, sep='\t')

    column_headings = df.columns
    labels = df[column_headings[0]].tolist()  # list of ranks
    values = df[column_headings[1]].tolist()  # initial data (frequency)
    print(values)
    # create frames for animation
    frames_list = []
    for i in range(1, len(df.columns)):
        my_data = df[column_headings[i]].tolist()

        frames_list.append(
            go.Frame(data=[go.Pie(labels=labels, text=labels,
                                  hovertemplate="%{value} katas solved<extra></extra>",
                                  title=column_headings[i],
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
                               title=column_headings[1],
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
