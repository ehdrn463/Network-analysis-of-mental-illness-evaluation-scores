import dash
import pandas as pd
import networkx as nx

from dash import dcc
from dash import html
from lib import make_graph as mg
from textwrap import dedent as d

import dash_bootstrap_components as dbc

###################### Style Sheet ###################
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}


############### Control Bar ####################3
file_uploads = html.Div([
    dcc.Upload(
        children = html.Div([
            'Attribute Matrix'
        ]),
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False,
        id='upload-file',
    ),
    html.Div(id='output-file-upload'),
]) 


corr_file_uploads = html.Div([
    dcc.Upload(
        html.Div([
            'Correlation Matrix'
        ]),
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False,
        id='upload-corr-file'
    ),
    html.Div(id='output-corr-file-upload'),    
])

controls = dbc.FormGroup(
    [                    
        html.Div(
            className="twelve columns",
            children=[
                dcc.Markdown(d("""
                **Attribute to Search**.
                """)),
                dcc.Markdown(d("""
                **Attribute to Search**.
                """)),
                dcc.Input(id="input_attr", 
                          type="text", placeholder="Attribute"),
                html.Div(id="output_attr")
            ],
            style={'textAlign': 'center'}
        )
        ,
        html.P('Dropdown', style = {
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options = [ 
                {
                    'label': 'Value One',
                    'value': 'value1'
                }, 
                {
                    'label': 'Value Twoo',
                    'value': 'value2',
                }, 
                {
                    'label': 'Value Three',
                    'value': 'value3'
                },
            ],
            value = ['value1'],
            multi = True
        ),
        html.Br(),
        html.P('Range Slider', style= {
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min = 0,
            max = 20,
            step = 0.5,
            value = [5, 15]
        ),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options = [
                {
                    'label': 'Value One',
                    'value': 'value1'
                },
                {
                    'label': 'Value Two',
                    'value': 'value2',
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value = ['value1', 'value2'],
            inline = True
        )]),
            dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[
                {
                    'label': 'Value One',
                    'value': 'value1',
                },
                {
                    'label': 'Value Two',
                    'value': 'value2',
                },
                {
                    'label': 'Value Three',
                    'value': 'value3',
                }
            ],
            value='value1',
            style = { 'margin': 'auto'}
        )]),
        html.Br(),

    ]
)


sidebar = html.Div(
    [
        file_uploads,
        corr_file_uploads,
        html.Hr(),
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)





###################### Conten Row ####################
content_first_row = dbc.Row([
    dbc.Col(
        dcc.Graph(id='network_graph',
                  figure = mg.generate_network_graph()), md=12,
    )
    
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='centrality_graph',
                     figure = mg.network_to_centrality()), 
                     md=12,
                     
        ),
    ],
    # style = { 'height' : '60vh'}

)

content_third_row = dbc.Row(
    children = [
        mg.make_ggm_table()
    ],
    id="ggm_table"
)



######################## content ######################
content = html.Div(
    [
        html.H2('Network analysis of mental illness evaluation scores', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
    ],
    style = CONTENT_STYLE
)

