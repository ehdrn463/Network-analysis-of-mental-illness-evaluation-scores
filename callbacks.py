import pandas as pd
import io

import dash
import json

from dash import dcc
from dash.exceptions import PreventUpdate
from app import app
from lib import make_graph as mg
from dash.dependencies import Input, Output, State
from dash_extensions.snippets import send_bytes


# 1. Data Load: Case1 (attribute)
@app.callback(
    [Output('heatmap_graph', "figure"), Output('ggm_table', 'children'), Output('memory-ggm', 'data')],
    [Input('upload-file', 'contents'), Input('upload-file', 'filename')]
)
def upload_attr(contents, filename):
    if (contents is None):
        df = pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0)
    else:
        df = mg.attr_to_ggm(contents, filename)
    df = round(df, 3)
    df_json = df.to_json(orient='table')
    return mg.make_heatmap(df), mg.make_ggm_table(df), df_json


# 1. Data Load: Case2 (correlation)
@app.callback(
    [Output('heatmap_graph', "figure"), Output('ggm_table', 'children'), Output('memory-ggm', 'data')],
    [Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename')]    
)
def upload_corr(contents, filename):
    df = mg.download_file(contents, filename)
    df = round(df, 3)
    df_json = df.to_json(orient='table')
    return mg.make_heatmap(df), mg.make_ggm_table(df), df_json


# 2. Visualize Network anlysis
@app.callback(
    [Output('network_graph', 'figure')],
    [Input('memory-ggm', 'data')],
    [State('memory-ggm', 'data')]
)
def visualize_network_attr(input_ggm_data, ggm_data2):    
    if (input_ggm_data is None) and (ggm_data2 is None):
        raise PreventUpdate

    ggm_data = pd.read_json(input_ggm_data, orient='table')
    ggm_data2 = pd.read_json(ggm_data2, orient='table')

    # source, target, weight matrix로 변환
    target_df = mg.corr_to_target(ggm_data)
    network_graph_fig = mg.generate_network_graph(target_df)
    return network_graph_fig


# 3-1. Applied Community Detection
@app.callback(
    [Output('network_graph', 'figure')],
    [Input('community-applied-btn', 'n_clicks')],
    [State('memory-ggm', 'data'), State('gamma-community', 'value')]
)
def applied_community(n_clicks, memory_ggm, gamma_community=1.0):
    print(n_clicks, memory_ggm, gamma_community)
    if n_clicks == 0:
        raise PreventUpdate
    
    if memory_ggm is None:
        ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else:  
        ggm_data = pd.read_json(memory_ggm, orient='table')
    target_df = mg.corr_to_target(ggm_data)
    network_graph_fig = mg.applied_community_detection(target_df, gamma=gamma_community)
    return network_graph_fig


# 3-2. Convert Network Layout
@app.callback(
    [Output('network_graph', 'figure')],
    [Input('dropdown-graph', 'value')],
    [State('memory-ggm', 'data'), State('gamma-community', 'value')]
)
def change_network_layout(layout, memory_ggm, gamma_community):
    # print(layout, memory_ggm, gamma_community)
    if memory_ggm is None:
        ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else:  
        ggm_data = pd.read_json(memory_ggm, orient='table')
    target_df = mg.corr_to_target(ggm_data)
    
    if gamma_community is None:
        network_graph_fig = mg.generate_network_graph(target_df)
    else:
        network_graph_fig = mg.applied_community_detection(target_df, layout=layout, gamma=gamma_community)
        
    return network_graph_fig


# 3-3. Applying Search Node 
@app.callback(
    [Output('network_graph', 'figure')],
    [Input('search-btn', 'n_clicks')],
    [State('memory-ggm', 'data'), State('gamma-community', 'value'), State('search-node','value')]
)
def applied_search(n_clicks, memory_ggm, gamma_community, search_node):
    print(n_clicks, memory_ggm, gamma_community, search_node)
    if n_clicks == 0:
        raise PreventUpdate

    if memory_ggm is None:
        ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else:  
        ggm_data = pd.read_json(memory_ggm, orient='table')
    target_df = mg.corr_to_target(ggm_data)

    if gamma_community is None:
        network_graph_fig = mg.generate_network_graph(target_df, specific_attr=search_node)
    else:
        network_graph_fig = mg.applied_community_detection(target_df, specific_attr=search_node, gamma=gamma_community)
        
    return network_graph_fig


# 4. Visualize Centrality Analysis
@app.callback(
    [Output('centrality_graph', 'figure')],
    [Input('dropdown-centrality', 'value')],
    [State('memory-ggm', 'data'), State('dropdown-centrality', 'value')]
)
def visualize_centrality(input_centrality, memory_ggm, centrality):
    # print(input_centrality, memory_ggm, centrality)

    if memory_ggm is None:
        ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else:  
        ggm_data = pd.read_json(memory_ggm, orient='table')
    # target_df = mg.corr_to_target(ggm_data)

    centrality_fig = mg.network_to_centrality(target_df=ggm_data, normalized=True, centrality=centrality)
    return centrality_fig


# 5. Convert EBIC graphical Lasso
@app.callback(
    [Output('network_graph', 'figure'), Output('heatmap_graph', "figure"), Output('centrality_graph', 'figure'), Output('memory-ggm', 'data')],
    [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename'), Input('ebic-gamma','value'), Input('dropdown-graph', 'value')],
    [State('ebic-gamma', 'value'), State('dropdown-graph', 'value')]
)
def convert_ebic_gamma(contents, filename, contents2, filename2, input_ebic_gamma, input_layout, ebic_gamma, layout):
    if ebic_gamma is None:
        raise PreventUpdate

    if (contents is None) and (contents2 is None):
        df = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    elif (contents is not None):
        df = mg.attr_to_ggm(contents, filename, gamma= ebic_gamma)
    elif (contents2 is not None):
        df = mg.attr_to_ggm(contents2, filename2, gamma= ebic_gamma)
    else:
        df = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    
    df = round(df, 3)
    df_json = df.to_json(orient='table')

    # source, target, weight matrix로 변환
    target_df = mg.corr_to_target(df)
    centrality_fig = mg.network_to_centrality(target_df=df, normalized=True, centrality='strength')
    network_graph_fig = mg.generate_network_graph(target_df=target_df, layout=layout)
    heatmap_fig = mg.make_heatmap(df)
    return network_graph_fig, heatmap_fig, centrality_fig, df_json


# 6. Refresh Graph
@app.callback(
    [Output('network_graph', 'figure')],
    [Input('refresh-button', 'n_clicks'), Input('dropdown-graph', 'value')],
    [State('memory-ggm', 'data'), State('dropdown-graph', 'value')]
)
def refresh_graph(n_clicks, input_layout, data, layout):
    if n_clicks == 0:
        raise PreventUpdate

    if data is None:
        ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else:
        ggm_data = pd.read_json(data, orient='table')
    
    # source, target, weight matrix로 변환
    target_df = mg.corr_to_target(ggm_data)
    network_graph_fig = mg.generate_network_graph(target_df, layout=layout)
    return network_graph_fig


# 7. 저장용
@app.callback(
    [Output("download-csv", "data")],
    [Input("corr-ggm-button", "n_clicks"), Input("xlsx-corr-ggm-button", "n_clicks")],
    [State("memory-ggm", "data")],
    prevent_initial_call=True,
)
def download_corr_matrix_as_csv(csv_clicks, xlsx_clicks, data):
    if (not csv_clicks) and (not xlsx_clicks):
        raise PreventUpdate

    if data is None:
        df = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
    else: 
        df = pd.read_json(data, orient='table')

    # download_buffer = io.StringIO()

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # change_xlsx = [p['xlsx-corr-matrix-save-button'] for p in dash.callback_context.triggered][0]
    
    print(type(df))
    if 'corr-ggm-button.n_clicks' == changed_id:
        return dcc.send_data_frame(df.to_csv, filename="matrix.csv")

    elif 'xlsx-corr-ggm-button.n_clicks' == changed_id:
        print(changed_id)
        return dcc.send_data_frame(df.to_excel, filename="corr_matrix.xlsx")

# @app.callback(
#     [Output("download-csv", "data"), Output("download-xlsx", "data")],
#     [Input("corr-ggm-button", "n_clicks"), Input("xlsx-corr-ggm-button", "n_clicks")],
#     [State("memory-ggm", "data")],
#     prevent_initial_call=True,
# )
# def download_corr_matrix_as_csv(csv_clicks, xlsx_clicks, data):
#     if (not csv_clicks) and (not xlsx_clicks):
#         raise PreventUpdate

#     if data is None:
#         df = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
#     else: 
#         df = pd.read_json(data, orient='table')

#     # download_buffer = io.StringIO()

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     # change_xlsx = [p['xlsx-corr-matrix-save-button'] for p in dash.callback_context.triggered][0]
    
#     print(type(df))
#     if 'corr-ggm-button.n_clicks' == changed_id:
#         print(changed_id)
#         # return dcc.send_data_frame(df.to_csv, filename="matrix.csv", index= False)
#         return dcc.send_data_frame(df.to_csv, filename="matrix.csv")
#         # df.to_csv(download_buffer, index=False)
#         # download_buffer.seek(0)
#         # return dict(content=download_buffer.getvalue(), filename="corr_matrix.csv")
#     elif 'xlsx-corr-ggm-button.n_clicks' == changed_id:
#         print(changed_id)
#         return dcc.send_data_frame(df.to_excel, filename="corr_matrix.xlsx", index= False)



# @app.callback(
#     [Output('network_graph', 'figure'),],
#     [Input('dropdown-gamma','value')],
#     [State('dropdown-gamma','value')],
# )
# def applied_EBIC_gamma(input_ebic_gamma, ebic_gamma):
#     if n_clicks == 0:
#         raise PreventUpdate

#     if memory_ggm is None:
#         ggm_data = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
#     else:  
#         ggm_data = pd.read_json(memory_ggm, orient='table')
#     target_df = mg.corr_to_target(ggm_data)

#     if gamma_community is None:
#         network_graph_fig = mg.generate_network_graph(target_df, specific_attr=search_node)
#     else:
#         network_graph_fig = mg.applied_community_detection(target_df, specific_attr=search_node, gamma=gamma_community)
        
#     return network_graph_fig


# @app.callback(
#     # [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('centrality_degree_graph', 'figure'), Output('centrality_weighted_degree_graph', 'figure'), Output('centrality_closeness_graph', 'figure'), Output('centrality_between_graph', 'figure'), Output('heatmap_graph', "figure"), Output('ggm_table', 'children')],
#     [Output('network_graph', 'figure'), Output('centrality_degree_graph', 'figure'), Output('centrality_weighted_degree_graph', 'figure'), Output('centrality_closeness_graph', 'figure'), Output('centrality_between_graph', 'figure'), Output('heatmap_graph', "figure"), Output('ggm_table', 'children')],
#     [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename'), Input('refresh-button', 'n_clicks'), Input('dropdown-graph', 'value'), Input('search-btn', 'n_clicks'), Input('dropdown-gamma','value')],
#     [State('dropdown-gamma','value'), State('search-node','value')]
# )
# def update_graph(contents, filename, contents2, filename2, refresh_clicks, layout, search_clicks, gamma_input, gamma, search_node):
#     # print(gamma)
#     # attr에 ggm을 적용해줌.    
#     if (not contents) and (not contents2):
#         df = pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0)
#         # print('stop')
#         # raise PreventUpdate
#     if contents:
#         # print('gamma: ', gamma)
#         df = mg.attr_to_ggm(contents, filename, gamma=gamma)
#     elif contents2:
#         # corr matrix는 바로 읽음 ( GGM 적용 X )
#         df = mg.download_file(contents2, filename2)
#     df = round(df, 2)    
#     # source, target, weight matrix로 변환
#     target_df = mg.corr_to_target(df)

#     # network analaysis 진행
#     # print(layout, "searchnode: ", search_node)
#     network_graph_fig = mg.generate_network_graph(target_df, layout, search_node)

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]   

#     # networkx graph객체로 변환
#     input_graph = mg.target_to_graph(target_df)
    
#     # 중심성 계산
#     centrality_graph_fig = mg.network_to_centrality(input_graph)
    
#     # search_node = None
#     if 'refresh-button.n_clicks' == changed_id:
#         # return network_graph_fig, centrality_graph_fig[0], centrality_graph_fig[1], centrality_graph_fig[2], centrality_graph_fig[3], centrality_graph_fig[4], mg.make_heatmap(df), mg.make_ggm_table(df)
#         return network_graph_fig, centrality_graph_fig[1], centrality_graph_fig[2], centrality_graph_fig[3], centrality_graph_fig[4], mg.make_heatmap(df), mg.make_ggm_table(df)
#     # return network_graph_fig, centrality_graph_fig[0], centrality_graph_fig[1], centrality_graph_fig[2], centrality_graph_fig[3], centrality_graph_fig[4], mg.make_heatmap(df), mg.make_ggm_table(df)
#     return network_graph_fig, centrality_graph_fig[1], centrality_graph_fig[2], centrality_graph_fig[3], centrality_graph_fig[4], mg.make_heatmap(df), mg.make_ggm_table(df)



# @app.callback(Output('search-node','value'),
#              [Input('reset-btn','n_clicks')])
# def update(reset):
#     return ''


# @app.callback(Output('search-node','value'),
#              [Input('dropdown-gamma','value')])
# def update(reset):
#     return ;


# 보관용
# @app.callback(
#     [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('centrality_degree_graph', 'figure'), Output('centrality_weighted_degree_graph', 'figure'), Output('centrality_closeness_graph', 'figure'), Output('centrality_between_graph', 'figure'), Output('ggm_table', 'children')],
#     [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename')]
# )
# def update_graph(contents, filename, contents2, filename2):
#     # attr에 ggm을 적용해줌.
    
#     if (not contents) and (not contents2):
#         raise PreventUpdate
#     if contents:
#         df = mg.attr_to_ggm(contents, filename)
#     elif contents2:
#         # corr matrix는 바로 읽음 ( GGM 적용 X )
#         df = mg.download_file(contents2, filename2)
#     # source, target, weight matrix로 변환
#     target_df = mg.corr_to_target(df)

#     # network analaysis 진행
#     network_graph_fig = mg.generate_network_graph(target_df)

#     # networkx graph객체로 변환
#     input_graph = mg.target_to_graph(target_df)
    
#     # 중심성 계산
#     centrality_graph_fig = mg.network_to_centrality(input_graph)
    
#     return network_graph_fig, centrality_graph_fig[0], centrality_graph_fig[1], centrality_graph_fig[2], centrality_graph_fig[3], centrality_graph_fig[4], mg.make_ggm_table(df)





    # @app.callback(
    #     Output('network_graph', 'figure'),
    #     [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'),  Input('upload-corr-file', 'filename'), Input('refresh-button', 'n_clicks')],
    # )   
    # def refresh_graph_shape(contents, filename, contents2, filename2, n_clicks):
    #     print(contents, filename, contents2, filename2, n_clicks)
        
    #     if (n_clicks == 0) and (not contents) and (not contents2):
    #         raise PreventUpdate
    #     print('okay')
    #     if contents:
    #         df = mg.attr_to_ggm(contents, filename)
    #     elif contents2:
    #         # corr matrix는 바로 읽음 ( GGM 적용 X )
    #         df = mg.download_file(contents2, filename2)
    #     # source, target, weight matrix로 변환
    #     target_df = mg.corr_to_target(df)

    #     # network analaysis 진행
    #     network_graph_fig = mg.generate_network_graph(target_df)
        

    #     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #     # change_xlsx = [p['xlsx-corr-matrix-save-button'] for p in dash.callback_context.triggered][0]

    #     # print(change_xlsx)
    #     if 'refresh-button.n_clicks' == changed_id:
    #         return network_graph_fig
    

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