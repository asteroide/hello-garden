# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.figure_factory as ff
import dash_table
import pandas as pd
from datetime import datetime, timedelta
from hello_garden import database, data

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
diag_data = None
params = [
    'Section', 'Name', 'Type', 'Start date', 'End date'
]


#@app.callback(
#    #Output('graph', 'figure'),
#    Input('submit-val', 'n_clicks'),
#)
#def add_plant(n_clicks):
#    print(f"add_plant {n_clicks}")
#    database.save("test.json")

def get_all_sections():
    all_sections = []
    dd = []
    types = []
    #for sections in diag_data['garden']:
    for key_s in diag_data['garden']:
        # print(key_s, "------------")
        all_sections.append({"label": key_s, "value": key_s})
        # dd.append(dict(Task=key_s, Start='2021-01-01', Finish='2021-12-01', Resource="section"))
        try:
            for vege in diag_data['garden'][key_s]:
                #for key_v in vege:
                for key_v in vege:
                    # print(vege[key_v])
                    dd.append(dict(
                        Task=key_v, 
                        Start=vege[key_v]['date']['start'], 
                        Finish=vege[key_v]['date']['end'], 
                        Resource=key_s,
                        Type=vege[key_v]['type']))
                _type = vege[key_v]['type']
                if {"label": _type, "value": _type} not in types:
                    types.append({"label": _type, "value": _type})
        except TypeError:
            pass
    return all_sections, dd, types

def rows_to_dict(rows):
    json_data = {}
    for row in rows:
        # print(row)
        try:
            datetime.fromisoformat(row["Finish"])
        except:
            print("Warning: found time delta", row["Finish"])
            row["Finish"] = data.__add_timedelta(row["Start"], row["Finish"])
            print("Warning: update time delta", row["Finish"])
        if row["Resource"] not in json_data:
            json_data[row["Resource"]] = []
        try:
            json_data[row["Resource"]].append(
                {row["Task"]: {
                    "type": row["Type"],
                    "date": {
                        "start": datetime.fromisoformat(row["Start"]),
                        "end": datetime.fromisoformat(row["Finish"]),
                    }
                }}
        )
        except ValueError or TypeError as e:
            print(f"Error: cannot add {row}", e)
    return {"garden": json_data}

def get_diagram():
    all_sections, dd, types = get_all_sections()

    df = pd.DataFrame(dd)

    # https://plotly.com/python-api-reference/generated/plotly.figure_factory.create_gantt.html
    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, #colors=colors, 
                          group_tasks=True, showgrid_x=True, show_hover_fill=True)

    # https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-tickmode
    fig.update_xaxes(tickmode="linear", tick0="2021-01-01", dtick="M1")

    return dcc.Graph(
            id='graph',
            figure=fig
        )

def get_form():
    all_sections, dd, types = get_all_sections()
    
    return html.Div(children=[
            html.Div(children=[
                "Nom :", 
                dcc.Input(id='name', value='', type='text')
            ]),
            dcc.RadioItems(
                options=[
                    {'label': 'Semence', 'value': 'seed'},
                    {'label': 'Plant', 'value': 'plant'}
                ],
                value="seed",
                labelStyle={'display': 'inline-block'}
            ),
            dcc.DatePickerSingle(
                id='date_start',
                date=datetime.now()
            ),
            html.Div(children=[
                "Durée :", 
                dcc.Input(id='duration', value='20', type='number')
            ]),
            html.Div(children=[
                "Sections :", 
                dcc.Dropdown(
                    id='sections',
                    options=all_sections,
                    value=''
                ),
            ]),
            html.Div(children=[
                html.Button('Ajouter', id='submit-val', n_clicks=0),
            ]),
        ],
    )

def get_image():
    return html.Div(children=[
                html.Div(children=[
                    html.Img(src=app.get_asset_url('plan.svg'))
                ]),
            ])

def get_data_list():
    all_sections, dd, types = get_all_sections()
    # TODO https://dash.plotly.com/datatable/dropdowns
    return html.Div([
        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        html.Button('Save', id='saving-rows-button', n_clicks=0),
        dash_table.DataTable(
            id='table-editing-simple',
            columns=(
                [
                    {'id': "Resource", 'name': "Section", 'presentation': 'dropdown'},
                    {'id': "Task", 'name': "Name"},
                    {'id': "Type", 'name': "type", 'presentation': 'dropdown'},
                    {'id': "Start", 'name': "Start date"},
                    {'id': "Finish", 'name': "End date"},
                ]
            ),
            data=dd,
            editable=True,
            dropdown={
                "Resource": {
                    "options": all_sections
                },
                "Type": {
                    "options": types
                },
            }
        ),
        #dcc.Graph(id='table-editing-simple-output')
    ])

def create_app(data):
    global app
    app.layout = html.Div([
        html.H1(children='Hello Garden'),
        html.Div(id="hidden-div", style={"display": "none"}),
        html.Div(id="hidden-div2", style={"display": "none"}),
        dcc.Tabs(id="tabs", value='tab-diag', children=[
            dcc.Tab(label='Diagram', value='tab-diag'),
            # dcc.Tab(label='Add Plant', value='tab-form'),
            dcc.Tab(label='Garden', value='tab-img'),
            dcc.Tab(label='List', value='tab-list'),
        ]),
        html.Div(id='tabs-content')
    ])
    return app

@app.callback(
    Output('table-editing-simple', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('table-editing-simple', 'data'),
    State('table-editing-simple', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        row = {c['id']: '' for c in columns}
        row["Start"] = datetime.now().strftime("%Y-%m-%d")
        rows.insert(0, row)
    return rows

@app.callback(
    Output("hidden-div2", 'children'),
    Input('saving-rows-button', 'n_clicks'),
    State('table-editing-simple', 'data'),
    State('table-editing-simple', 'columns'))
def save_rows(n_clicks, rows, columns):
    if n_clicks > 0:
        print("Calling save_rows", n_clicks)
        data = rows_to_dict(rows)
        print(data)
        database.save("test.yaml", data)
    return str(datetime.now())

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_tabs_content(tab):
    if tab == 'tab-diag':
        return get_diagram()
    elif tab == 'tab-form':
        return get_form()
    elif tab == 'tab-img':
        return get_image()
    elif tab == 'tab-list':
        return get_data_list()

@app.callback(
    Output("hidden-div", 'children'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))
def update_list(rows, columns):
    global diag_data
    diag_data = rows_to_dict(rows)
    #print(columns)
    return json.dumps(rows)

def run(debug=False, data=None, database=None):
    global diag_data
    diag_data = data
    # print(diag_data)
    app = create_app(data)
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=debug)
