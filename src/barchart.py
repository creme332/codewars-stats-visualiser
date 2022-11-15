import ast
import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'browser'


def HorizontalBarChart(source_file_name, destination_filename):

    df = pd.read_csv(source_file_name, sep='\t')

    # Preprocessing : Create a df with columns : rankname, count
    # https://stackoverflow.com/a/58155933/17627866
    ser = df["rank"].astype('str')
    ser = ser.apply(lambda x: ast.literal_eval(x))
    df2 = ser.apply(pd.Series)
    # to avoid confusing kata name and rank name
    df2.rename(columns={'name': 'rank name'}, inplace=True)
    df = pd.concat((df['id'], df2['rank name']), axis=1)
    ser = df.groupby('rank name').size()
    df = pd.DataFrame(ser)
    df = df.reset_index(level=0)  # convert index column to an actual column
    df.rename(columns={0: 'count'}, inplace=True)

    fig = px.bar(df, x="count", y="rank name", color='count', orientation='h',
                 hover_data=["rank name", "count"],
                 color_continuous_scale=px.colors.sequential.Plotly3,
                 # height=400,
                 title='Number of katas solved per rank')
    fig.write_html(destination_filename)
    # fig.show()
    # https://plotly.com/python/colorscales/  for more colors
# HorizontalBarChart('katainfo','')
