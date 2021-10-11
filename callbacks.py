import pandas as pd
import io

import dash
from dash import dcc
from dash.exceptions import PreventUpdate
from app import app
from lib import make_graph as mg
from dash.dependencies import Input, Output, State
from dash_extensions.snippets import send_bytes




@app.callback(
    [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('ggm_table', 'children')],
    [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename')])
def update_graph(contents, filename, contents2, filename2):
    # attr에 ggm을 적용해줌.
    print('='*5, filename)
    print('='*5, filename2)
    if (not contents) or (not contents2):
        raise PreventUpdate
    if contents:
        df = mg.attr_to_ggm(contents, filename)
    elif contents2:
        # corr matrix는 바로 읽음 ( GGM 적용 X )
        df = mg.download_file(contents2, filename2)
    # source, target, weight matrix로 변환
    target_df = mg.corr_to_target(df)

    # network analaysis 진행
    network_graph_fig = mg.generate_network_graph(target_df)

    # networkx graph객체로 변환
    input_graph = mg.target_to_graph(target_df)
    
    # 중심성 계산
    centrality_graph_fig = mg.network_to_centrality(input_graph)
    
    return network_graph_fig, centrality_graph_fig, mg.make_ggm_table(df)



@app.callback(
    Output("corr-matrix-download", "data"),
    [Input("corr-matrix-save-button", "n_clicks"), Input("xlsx-corr-matrix-save-button", "n_clicks")],
    State("corr-table", "data")
)
def download_corr_matrix_as_csv(csv_clicks, xlsx_clicks, corr_table_data):
    df = pd.DataFrame.from_dict(corr_table_data)

    if (not csv_clicks) and (not xlsx_clicks):
        raise PreventUpdate
    download_buffer = io.StringIO()
    temp_columns = ['Attr']
    for col in df.columns:
        if col != 'Attr':
            temp_columns.append(col)

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    # change_xlsx = [p['xlsx-corr-matrix-save-button'] for p in dash.callback_context.triggered][0]

    # print(change_xlsx)
    if 'corr-matrix-save-button.n_clicks' == changed_id:
        print('csv')
        df.to_csv(download_buffer, index=False, columns = temp_columns)
        download_buffer.seek(0)
        return dict(content=download_buffer.getvalue(), filename="corr_matrix.csv")
    elif 'xlsx-corr-matrix-save-button.n_clicks' == changed_id:
        return dcc.send_data_frame(df.to_excel, filename="corr_matrix.xlsx", index= False)
        

# @app.callback(
#     Output("corr-matrix-download", "data"),
#     Input("corr-matrix-save-button", "n_clicks"),
#     State("corr-table", "data")
# )
# def download_corr_matrix_as_csv2(n_clicks, corr_table_data):
#     df = pd.DataFrame.from_dict(corr_table_data)
#     if not n_clicks:
#         raise PreventUpdate
#     download_buffer = io.StringIO()
#     df.to_csv(download_buffer, index=True)
#     download_buffer.seek(0)
#     return dict(content=download_buffer.getvalue(), filename="corr_matrix.csv")


# @app.callback(
#     [Output('network_graph', 'figure')],
#     [Input('input_attr', 'value')]
# )
# def applied_search_keyword(input_attr):



# @app.callback(
#     [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('ggm_table', 'children')],
#     [Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename'), Input('input_attr', 'value')]
# )
# def corr_update_graph(contents, filename, input_attr):
#     # corr matrix는 바로 읽음 ( GGM 적용 X )
#     df = mg.download_file(contents, filename)
       
#     # source, target, weight matrix로 변환
#     target_df = mg.corr_to_target(df)

#     # network analaysis 진행
#     network_graph_fig = mg.generate_network_graph(target_df, input_attr)

#     # networkx graph객체로 변환
#     input_graph = mg.target_to_graph(target_df)
    
#     # 중심성 계산
#     centrality_graph_fig = mg.network_to_centrality(input_graph)
#     return network_graph_fig, centrality_graph_fig, mg.make_ggm_table(df)


# @app.callback(
#     [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('ggm_table', 'children')],
#     [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('input_attr', 'value')])
# def update_graph(contents, filename, input_attr):
#     # attr에 ggm을 적용해줌.
#     df = mg.attr_to_ggm(contents, filename)
       
#     # source, target, weight matrix로 변환
#     target_df = mg.corr_to_target(df)

#     # network analaysis 진행
#     network_graph_fig = mg.generate_network_graph(target_df, input_attr)

#     # networkx graph객체로 변환
#     input_graph = mg.target_to_graph(target_df)
    
#     # 중심성 계산
#     centrality_graph_fig = mg.network_to_centrality(input_graph)
    
#     return network_graph_fig, centrality_graph_fig, mg.make_ggm_table(df)



# @app.callback(
#     [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('ggm_table', 'children')],
#     [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename'), Input("input_attr", "value")])
# def update_graph(contents, filename, contents2, filename2, input_attr):
#     # attr에 ggm을 적용해줌.
#     print('='*5, filename)
#     print('='*5, filename2)
#     if contents:
#         df = mg.attr_to_ggm(contents, filename)
#     elif contents2:
#         # corr matrix는 바로 읽음 ( GGM 적용 X )
#         df = mg.download_file(contents2, filename2)
#     # source, target, weight matrix로 변환
#     target_df = mg.corr_to_target(df)

#     # network analaysis 진행
#     if input_attr:
#         network_graph_fig = mg.generate_network_graph(target_df, input_attr)
#     else:
#         network_graph_fig = mg.generate_network_graph(target_df)

#     # networkx graph객체로 변환
#     input_graph = mg.target_to_graph(target_df)
    
#     # 중심성 계산
#     centrality_graph_fig = mg.network_to_centrality(input_graph)
    
#     return network_graph_fig, centrality_graph_fig, mg.make_ggm_table(df)




# @app.callback(
#     Output('graph_2', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)
#     fig = {
#         'data': [{
#             'x': [1, 2, 3],
#             'y': [3, 4, 5],
#             'type': 'bar'
#         }]
#     }
#     return fig