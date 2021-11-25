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
        dcc.Markdown(d("""
        **Network Analysis Style**
        """), style={'text-align': 'center'}),
        dcc.Dropdown(
            id='dropdown-graph',
            options = [ 
                {
                    'label': 'spring (default)',
                    'value': 'spring',
                }, 
                {
                    'label': 'kamada_kawai',
                    'value': 'kamada_kawai',
                }, 
                {
                    'label': 'spectral',
                    'value': 'spectral',
                }, 
                {
                    'label': 'spiral',
                    'value': 'spiral',
                },
                {
                    'label': 'circular',
                    'value': 'circular',
                },
                # {
                #     'label': 'shell',
                #     'value': 'shell'
                # }
            ],
            value = 'spring',
            multi = False,
        ),           
        html.Br(),
        # html.P('gamma', style = {
        #     'textAlign': 'center'
        # }),
        dcc.Markdown(d("""
        **EBIC: gamma**
        """), style={'text-align': 'center'}),
        dcc.Dropdown(
            id='dropdown-gamma',
            options = [ 
                {
                    'label': '0.01',
                    'value': 0.01
                }, 
                {
                    'label': '0.1',
                    'value': 0.1,
                }, 
                {
                    'label': '0.5',
                    'value': 0.5
                },
            ],
            value = [0.5],
            multi = False,
        ),
        html.Br(),
        html.Div(
            className="twelve columns",
            children=[
                dcc.Markdown(d("""
                **Attribute to Search**.
                """)),
                dcc.Input(id="search-node", 
                          type="text"), #, placeholder="Attribute"
                html.Button('Search', id="search-btn"),
                html.Button('Reset', id="reset-btn")
            ],
            style={'textAlign': 'center'}
        ),
        html.Br(),
        html.Div(
            [
                dbc.Button(
                id='refresh-button',
                n_clicks=0,
                children="Refresh Graph Aspect",
                color='primary',
                block=True
                )
            ]
        ),
        # html.Button(
        #     'Refresh Graph Aspect',
        #     id='submit_button',
        #     n_clicks=0,
        #     style = {
        #         'color': 'skyblue',
        #         'text-align': 'center',
        #     }
        # )
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
                     figure = mg.network_to_centrality()[0]), 
                     md=12,
                     
        ),
        dbc.Col(
            dcc.Graph(id='centrality_degree_graph',
                     figure = mg.network_to_centrality()[1]), 
                     md=6,
                     
        ),
        dbc.Col(
            dcc.Graph(id='centrality_weighted_degree_graph',
                     figure = mg.network_to_centrality()[2]), 
                     md=6,
                     
        ),
        dbc.Col(
            dcc.Graph(id='centrality_closeness_graph',
                     figure = mg.network_to_centrality()[3]), 
                     md=6,
                     
        ),
        dbc.Col(
            dcc.Graph(id='centrality_between_graph',
                     figure = mg.network_to_centrality()[4]), 
                     md=6,
                     
        ),
    ],
    # style = { 'height' : '60vh'}

)

content_third_row = dbc.Row(
    dbc.Col(
        dcc.Graph(
            figure=mg.make_heatmap(),
            id = "heatmap_graph"
        ),
        md=12,
    ),
)


content_fourth_row = dbc.Row(
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
        html.Hr(),
        content_second_row,
        html.Hr(),
        content_third_row,
        html.Hr(),
        content_fourth_row
    ],
    style = CONTENT_STYLE
)

