import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"


def TimeSeries(source_file_name, destination_file_name):
    df = pd.read_csv(source_file_name, sep='\t')

    # convert completedAt column to datetime datatype
    df['completedAt'] = df['completedAt'].astype('datetime64[ns]')
    # get rid of time info
    # https://stackoverflow.com/a/48155304/17627866
    df['completedAt'] = df['completedAt'].dt.normalize()

    # extract required data : date + frequency
    df = df.groupby('completedAt').size()

    fig = px.line(df,
                  title='Number of katas solved',
                  )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(showlegend=False)

    fig.update_xaxes(
        dtick="M1",
        tickformat='%d %B %Y',  # show day, month, year
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

    fig.write_html(destination_file_name)  # .pdf or .svg also available
    # fig.show()


# TimeSeries("data/creme332_compkatas", "")
