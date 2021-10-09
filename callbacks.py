from app import app
from lib import make_graph as mg
from dash.dependencies import Input, Output, State

@app.callback(
    [Output('network_graph', 'figure'), Output('centrality_graph', 'figure'), Output('ggm_table', 'children')],
    [Input('upload-file', 'contents'), Input('upload-file', 'filename'), Input('upload-corr-file', 'contents'), Input('upload-corr-file', 'filename')])
def update_graph(contents, filename, contents2, filename2):
    # attr에 ggm을 적용해줌.
    print('='*5, filename)
    print('='*5, filename2)
    if contents:
        df = mg.attr_to_ggm(contents, filename)
    elif contents2:
        # corr matrix는 바로 읽음 ( GGM 적용 X )
        df = mg.download_file(contents2, filename2)
    # source, target, weight matrix로 변환
    target_df = mg.corr_to_target(df)

    # network analaysis 진행
    network_graph_fig = mg.generate_network_graph(target_df, input_attr)

    # networkx graph객체로 변환
    input_graph = mg.target_to_graph(target_df)
    
    # 중심성 계산
    centrality_graph_fig = mg.network_to_centrality(input_graph)
    
    return network_graph_fig, centrality_graph_fig, mg.make_ggm_table(df)




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