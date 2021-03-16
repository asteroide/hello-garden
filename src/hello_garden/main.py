# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

colors = {'Semences': 'rgb(220, 0, 0)',
          'Plantation': (0, 0.9, 0.16),
          'tools': 'rgb(0, 00, 00)'}

tf = pd.DataFrame([
    dict(Task="Maison", Start='2021-01-01', Finish='2021-12-01', Resource="10"),
    #dict(Task="Serre", Start='2021-01-01', Finish='2021-12-01', Resource="20"),
])

df = pd.DataFrame([
    dict(Task="Maison", Start='2021-01-01', Finish='2021-12-01', Resource="tools"),
    dict(Task="Maïs Semences", Start='2021-01-15', Finish='2021-01-20', Resource="Semences"),
    dict(Task="Maïs Plantation", Start='2021-01-20', Finish='2021-03-15', Resource="Plantation"),
    dict(Task="Petit pois", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois1", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois2", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois3", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit poi4s", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois5", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois6", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois7", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois8", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation"),
    dict(Task="Petit pois9", Start='2021-02-17', Finish='2021-05-17', Resource="Plantation")
])

# https://plotly.com/python-api-reference/generated/plotly.figure_factory.create_gantt.html
fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                      group_tasks=True, showgrid_x=True)

#fig = px.line(df, x="Start", y="Resource", title='Category')

# https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-tickmode
fig.update_xaxes(tickmode="linear", tick0="2021-01-01", dtick="M1")

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Vege'),

    html.Div(children='''
        A web application to organize your garden.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)