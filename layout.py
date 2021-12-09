import dash
import pandas as pd
import networkx as nx

from dash import dcc
from dash import html
from lib import make_graph as mg
from textwrap import dedent as d

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

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
file_uploads = html.Div(
    [
        dcc.Upload(
            dbc.Button(
                [
                    dbc.Button('Upload Data', color="secondary"),
                ],
                className="d-grid gap-2",
                style={
                    'width': '80%',
                    'height': '60%',
                    'margin': '10px',
                    'margin-left': '35px',
                    # 'lineHeight': '60px',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
            ),
            # Allow multiple files to be uploaded
            multiple=False,
            id='upload-file',

        ),
        html.Div(id='output-file-upload'),
    ],
    style={
        'margin-left': 'auto',
        'margin-right': 'auto',
    }
) 


corr_file_uploads = html.Div(
    [
        dcc.Upload(
            dbc.Button(
                [
                    dbc.Button("Upload Networ Matrix", color="secondary")
                ],
                className="d-grid gap-2",
                style={
                    'width': '80%',
                    'height': '60%',
                    'margin': '10px',
                    'margin-left': '35px',
                    # 'lineHeight': '60px',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
            ),
            # Allow multiple files to be uploaded
            multiple=False,
            id='upload-corr-file'
        ),
        html.Div(id='output-corr-file-upload'),    
    ]
)

control_community_detection = html.Div(
    className="twelve columns",
    children=[
        dcc.Markdown(d("""
        **Community Detection: gamma**
        """)),
        dcc.Input(id="gamma-community", 
                    type="number",
                 ),
                    # placeholder=1.0),
        html.Button('적용', id="community-applied-btn"),
    ],
    style={'textAlign': 'center'}
)

control_network_layout = html.Div([
    dcc.Markdown(d("""
    **Network Analysis Style**
    """), style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dropdown-graph',
        style={
            'width': '90%',
            'margin-left': 'auto',
            'margin-right': 'auto',
            },
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
        ],
        value = 'spring',
        multi = False,
    )
])  

control_EBIC_gamma = html.Div(
    children = [
        html.Div(
        className="twelve columns",
        children=[
            dcc.Markdown(d("""
            **EBIC: gamma**
            """)),
            dcc.Input(id="ebic-gamma", 
                        type="number",
                    ),
                        # placeholder=1.0),
            html.Button('적용', id="ebic-gamma-btn"),
        ],
        style={'textAlign': 'center'}
        )
    ]
)

    # dcc.Dropdown(
    #     id='ebic-gamma',
    #     style={
    #         'width': '90%',
    #         'margin-left': 'auto',
    #         'margin-right': 'auto',
    #     },
    #     options = [ 
    #         {
    #             'label': '0.01',
    #             'value': 0.01
    #         }, 
    #         {
    #             'label': '0.1 (Default)',
    #             'value': 0.1,
    #         }, 
    #         {
    #             'label': '0.5',
    #             'value': 0.5
    #         },
    #     ],
    #     value = 0.1,
    #     multi = False,
    # )


control_search = html.Div(
    className="twelve columns",
    children=[
        dcc.Markdown(d("""
        **Attribute to Search**
        """)),
        dcc.Input(id="search-node", 
                    type="text"), #, placeholder="Attribute"
        html.Button('Search', id="search-btn"),
        html.Button('Reset', id="reset-btn")
    ],
    style={'textAlign': 'center'}
)


control_graph_aspect = html.Div(
    [
        dbc.Button(
        id='refresh-button',
        n_clicks=0,
        children="Refresh Graph Aspect",
        color='primary',
        block=True
        )
    ]
)

control_centrality = html.Div([
    dcc.Markdown(d("""
    **Centrality Analysis Style**
    """), style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dropdown-centrality',
        style={
            'width': '90%',
            'margin-left': 'auto',
            'margin-right': 'auto',
        },
        options = [ 
            {
                'label': 'degree',
                'value': 'degree',
            }, 
            {
                'label': 'strength (default)',
                'value': 'strength',
            }, 
            {
                'label': 'closeness',
                'value': 'closeness',
            }, 
            {
                'label': 'betweeness',
                'value': 'betweeness',
            },
        ],
        value = 'strength',
        multi = False,
    )
])  

download_controls = dbc.FormGroup(
    [
        dbc.Button(
            "Save Matrix as CSV", 
            id="corr-ggm-button",
            style = {
                
            },
            # className="d-grid gap-2",
        ),
        dcc.Download(id="download-csv"),
        
        dbc.Button(
            "Save Matrix as XLSX", 
            id="xlsx-corr-ggm-button",
            style = {
                'margin-left': '15px'
            },
            # className="d-grid gap-2",
        ),
        dcc.Download(id="download-xlsx")
    ]
)


controls = dbc.FormGroup(
    [    
        control_community_detection,
        html.Br(),
        control_network_layout,
        html.Br(),
        control_EBIC_gamma,
        html.Br(),
        control_centrality,
        html.Br(),
        control_search,
        html.Br(),
        download_controls,
        html.Br(),
        control_graph_aspect,
    ]
)


sidebar = html.Div(
    [
        file_uploads,
        corr_file_uploads,
        html.Hr(),
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls,
    ],
    style=SIDEBAR_STYLE,
)





###################### Conten Row ####################
content_row_ggm = dbc.Row([
    dbc.Col(
        dcc.Graph(
            id='network_graph',
            figure = mg.generate_network_graph()
        ), 
        style ={
            'width': '50vh',
            # 'height': '50vh'
        }
    ),
    dbc.Col(
        dcc.Graph(
            figure=mg.make_heatmap(),
            id = "heatmap_graph"
        ),
        style ={
            'width': '50vh',
            # 'height': '50vh'
        }
    ),
    dcc.Store(id='memory-ggm'),
],
style ={
    'height': '600px',
})


content_row_centrality = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='centrality_graph',
                      figure = mg.network_to_centrality()),
                      md=6,
        ),
    ],
    justify= 'center',
)





content_row_ggmtable = html.Div([
    dbc.Row(
        children = [
            mg.make_ggm_table()
        ],
        id="ggm_table"
    )
])



######################## content ######################
content = html.Div(
    [
        html.H2('Network analysis of mental illness evaluation scores', style=TEXT_STYLE),
        html.Hr(),
        
        html.H3('Gaussian Graphical Model Network Analysis', style=TEXT_STYLE),
        content_row_ggm,
        html.Hr(),

        html.H3('Centrality Analysis', style=TEXT_STYLE),
        content_row_centrality,
        html.Br(),
        # content_row_ggmtable,

    ],
    style = CONTENT_STYLE
)

