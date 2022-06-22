import pandas as pd
import numpy as np
import calplot
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'


def BasicHeatmap(single_year, source_file_name, destination_file_name):

    df = pd.read_csv(source_file_name, sep='\t')

    # convert completedAt column to datetime datatype
    # https://stackoverflow.com/a/16853161/17627866
    df['completedAt'] = df['completedAt'].astype('datetime64[ns]')

    if single_year == -1:  # plot for all years
        series = df.groupby('completedAt').size()

        calplot.calplot(data=series, colorbar=True,
                        suptitle='Number of katas solved')
    else:  # single year

        # filter dataframe by year
        df_filtered = df[df['completedAt'].dt.strftime(
            '%Y') == str(single_year)]

        if df_filtered.empty:
            print("BasicHeatmap() ERROR : No data available for", single_year)
            return
        # create a series
        series = df_filtered.groupby('completedAt').size()

        calplot.calplot(data=series, figsize=(10, 5), colorbar=True,
                        suptitle='Number of katas solved')

    # save file
    plt.savefig(destination_file_name, bbox_inches='tight')


#BasicHeatmap(2019, "data/creme332_compkatas", "charts/basicheatmap1.png")


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
