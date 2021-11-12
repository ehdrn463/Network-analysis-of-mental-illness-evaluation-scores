from networkx.generators.random_graphs import powerlaw_cluster_graph
import pandas as pd
import networkx as nx
import numpy as np

import plotly.express as px
import plotly.graph_objs as go

import matplotlib
import seaborn as sns
import colorsys
import math
import io
import base64


from community import community_louvain

from dash import html
from dash import dash_table
# import dash_core_components as dcc
from dash import dcc

from colour import Color, color_scale
from dash_extensions import Download
from dash.exceptions import PreventUpdate
from inverse_covariance import QuicGraphicalLassoEBIC

# def initialize_graph():
global raw, raw_df
raw = round(pd.read_csv(r'/Users/gimdong-gu/Desktop/mind_detector_v3/Network-analysis-of-mental-illness-evaluation-scores/data/psp_swn_weight_ggg_v2.csv', index_col=0), 2)
raw_v2 = raw.copy()
raw_v2.insert(0, 'Attr', raw.columns, allow_duplicates=False)


# 정신질환 질문 속성
global attrSet
attrSet = set(list(raw.columns))
# attrSet.add()

raw_df = pd.DataFrame.from_dict(raw)
raw_df = raw_df.stack().reset_index()
raw_df.columns = ['source', 'target', 'weight']
raw_df.drop(raw_df[abs(raw_df.weight) < 0.01].index, inplace=True)

global basic_graph
basic_graph = nx.from_pandas_edgelist(raw_df, 'source', 'target', ['source', 'target', 'weight'], create_using=nx.Graph())



# correlation matrix to weight array(source, target, weight)
def corr_to_target(df):
    '''
    pandas.dataframe(corr) -> weight
    '''
    # print('df', df.columns) 
    df = round(df, 2)
    target_df = pd.DataFrame.from_dict(df)
    target_df = target_df.stack().reset_index()
    target_df.columns = ['source', 'target', 'weight']
    target_df.drop(target_df[abs(target_df.weight) < 0.01].index, inplace=True)
    # print('target_df', target_df)
    
    return target_df


# weight array to networkx graph object
def target_to_graph(target_df):
    '''
    df(weight_df) -> graph
    '''
    target_df = round(target_df, 2)
    basic_graph = nx.from_pandas_edgelist(target_df, 'source', 'target', ['source', 'target', 'weight'], create_using=nx.Graph())
    return basic_graph


# 네트워크 분석 함수 만들기
def generate_network_graph(target_df = raw_df, layout="spring", specific_attr=None):
    '''
    target_df(pandas dataframe) -> plotly.go
    '''
    # print(specific_attr)
    target_df = round(target_df, 2)
    attrSet = set(list(target_df.columns))
    
    # networkx layout 배치를위한 중심점 정의
    shells = []

    shell1 = [] #specific_attr을 위한 리스트

    #specific_attr 있으면 추가
    shell1.append(specific_attr)
    shells.append(shell1)


    shell2 = [] #specific_attr을 제외한 요소를 위한 리스트

    # specific_attr와 다른 요소 추가
    for elem in attrSet:
        if elem != specific_attr:
            shell2.append(elem)
    shells.append(shell2)


    G = nx.from_pandas_edgelist(target_df, 'source', 'target', ['source', 'target', 'weight'], create_using=nx.Graph())
    
    # if len(shell2) > 1:
    #     pos = nx.drawing.layout.spring_layout(G)
    #     print("spring")
    # else:
    #     pos = nx.drawing.layout.shell_layout(G, shells)
    #     print("shell")

    # if len(shell2) > 1:
    #     if layout == "spring": 
    #         pos = nx.drawing.layout.spring_layout(G)
    #     elif layout == "kamda_kawai":
    #         pos = nx.drawing.layout.kamada_kawai_layout(G)
    #     elif layout == "spectral":
    #         pos = nx.drawing.layout.spectral_layout(G)
    #     elif layout == "spiral":
    #         pos = nx.drawing.layout.spiral_layout(G)
    # else:
    #     pos = nx.drawing.layout.shell_layout(G, shells)

    if layout == "spring": 
        pos = nx.drawing.layout.spring_layout(G)
    elif layout == "kamda_kawai":
        pos = nx.drawing.layout.kamada_kawai_layout(G)
    elif layout == "spectral":
        pos = nx.drawing.layout.spectral_layout(G)
    elif layout == "spiral":
        pos = nx.drawing.layout.spiral_layout(G)
    elif layout == "shell":
        pos = nx.drawing.layout.shell_layout(G)
    elif layout == "circular":
        pos = nx.drawing.layout.circular_layout(G)
    else:
        pos = nx.drawing.layout.spring_layout(G)

    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    # shell2: specific_attr을 제외한 요소를 위한 리스트
    if len(shell2) == 0:
        traceRecode = [] # contains edge_trace, node_trace, middle_node_trace
        node_trace = go.Scatter(x=tuple([1]), y=tuple([1]), text=tuple([str(specific_attr)]), 
                                textposition="bottom center",
                                mode= "markers+text",
                                marker={'size': 25, 'color': 'LightSkyBlue'},
                                opacity = 0)
        traceRecode.append(node_trace)
        node_trace1 = go.Scatter(x=tuple([1]), y=tuple([1]),
                                mode='markers',
                                marker={'size': 25, 'color': 'LightSkyBlue'},
                                opacity=0)
        traceRecode.append(node_trace1)

        figure = {
            "data": traceRecode,
            "layout": go.Layout(title='Network Analaysis Applied Search', showlegend=False,
                                margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                height=600
                                )}
        return figure
        


    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    ############################################################################################################################################################
    # pos_colors = list(Color('DarkBlue').range_to(Color('SkyBlue'), 3))
    # pos_colors = ['rgb'+str(x.rgb) for x in pos_colors]

    # neg_colors = list(Color('OrangeRed').range_to(Color('DarkRed'), 3))
    # neg_colors = ['rgb'+str(x.rgb) for x in neg_colors]
    # colors = ['rgb' + str(x.rgb) for x in colors]


    # color = matplotlib.colors.ColorConverter.to_rgb("navy")
    # rgbs = [scale_lightness(color, scale) for scale in [0, .5, 1, 1.5, 2]]

    def scale_lightness(rgb, scale_l):
        # convert rgb to hls
        h, l, s = colorsys.rgb_to_hls(*rgb)
        # manipulate h, l, s values and return as rgb
        return colorsys.hls_to_rgb(h, min(1, l * scale_l), s = s)

    pos_color = matplotlib.colors.ColorConverter.to_rgb("teal")
    pos_rgbs = ['rgb'+str(scale_lightness(pos_color, scale * 10)) for scale in np.arange(0.15, 0.1, -0.005)]

    neg_color = matplotlib.colors.ColorConverter.to_rgb("darkred")
    neg_rgbs = ['rgb'+str(scale_lightness(neg_color, scale * 10)) for scale in np.arange(0.15, 0.1, -0.005)]


    index = 0
    for edge in G.edges:

        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        weight = G.edges[edge]['weight']

        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                           mode='lines',
                           line={'width': abs(weight)*25},
                        #    marker = dict(color= 'teal' if weight >0 else 'darkred'),
                           marker=dict(color= pos_rgbs[int(round(weight*10, 0))] if weight > 0 else neg_rgbs[int(round((-weight)*10, 0))]),
                           line_shape='spline',
                           opacity=1)

        traceRecode.append(trace)
        index = index + 1

    ###############################################################################################################################################################
    # node_color_list = ["DEA5A4", "D3AFD5", "C9DECF", "C3E2DF", "B2DBBA", "F7B4BE", "F9DD7C"]
    node_color_list = ['rgb(222,165,164)', 'rgb(201,222,207)','rgb(249,221,124)', 'rgb(211,175,213)', 'rgb(195,226,223)', 'rgb(178,219,186)','rgb(247,180,190)']
    partition = community_louvain.best_partition(G)
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
                            hoverinfo="text", marker={'size': 25, 'color': []})

    index = 0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        # ex: Anxiety: 긴장 표시용 일단은 필요 X
        # hovertext = "Attribute Name: " + str(G.nodes[node]['Evaluation item'])
        # node_trace['hovertext'] += tuple([hovertext])

        # text = node1['Account'][index]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([node])
        node_trace['marker']['color'] += tuple([node_color_list[partition[node]]])
        
        index = index + 1
    
    traceRecode.append(node_trace)       


    ################################################################################################################################################################
    middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
                                    marker={'size': 20, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        hovertext = "From: " + str(G.edges[edge]['source']) +  "<br>" + "To   : " + str(G.edges[edge]['target']) + "<br>" + "correlation: " + str(G.edges[edge]['weight'])

        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
        middle_hover_trace['hovertext'] += tuple([hovertext])
        index = index + 1

    traceRecode.append(middle_hover_trace)


    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='Gaussian Graphical Model Network Analysis', showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select',

                            )}
    # print(type(figure))
    # print("끝")
    return figure



# 중심성 계산 함수
def network_to_centrality(input_graph=basic_graph, normalized=True):
    '''
    input_graph(networkx graph object) -> centrality plot
    '''
    fig = go.Figure()

    fig.update_layout(
        title= {
            "text": "The Result of Node Centrality Analysis",
            "xanchor" : "left",
            "yanchor": "top",
            'x': 0.3,
        },
        autosize=True,
        height=600
    )


    # degree_centrality
    '''
    input: graph-networkx.Grpah
    output: dict['attribute']=centrality
    '''
    degree_cent = nx.degree_centrality(input_graph)
    degree_cent = dict(sorted(degree_cent.items(), key=lambda item:item[1]))
    fig.add_trace(go.Scatter(x=list(degree_cent.values()), y= list(degree_cent.keys()), mode="lines+markers", name="degree", marker_color="#19D3F3"))
    
    degree_cent_fig = go.Figure(data=[go.Scatter(x=list(degree_cent.values()), y=list(degree_cent.keys()), mode="lines+markers", name="degree", marker_color="#19D3F3")])
    degree_cent_fig.update_layout(
        title = {
            'text': "Degree Centrality",
            "xanchor": 'center',
            'yanchor': 'top',
            'x': 0.55,
        }
    )

    # weight_centrality
    weight_cent = {n:0.0 for n in input_graph.nodes()}
    for u, v, d in input_graph.edges(data=True):
        weight_cent[u]+=d['weight']
        weight_cent[v]+=d['weight']
    weight_cent = dict(sorted(weight_cent.items(), key=lambda item:item[1]))
    if normalized==True:
        weighted_sum = sum(weight_cent.values())
        norm_weight_cent = {k:v/weighted_sum for k, v in weight_cent.items()}
        fig.add_trace(go.Scatter(x=list(norm_weight_cent.values()), y= list(norm_weight_cent.keys()), mode="lines+markers", name="norm weighted degree", marker_color="#00CC96"))
        weighted_cent_fig = go.Figure(data=[go.Scatter(x=list(norm_weight_cent.values()), y=list(norm_weight_cent.keys()), mode="lines+markers", name="norm weighted closeness", marker_color="#00CC96")])
    else:
        fig.add_trace(go.Scatter(x=list(weight_cent.values()), y= list(weight_cent.keys()), mode="lines+markers", name="weighted degree", marker_color="#00CC96"))     
        weighted_cent_fig = go.Figure(data=[go.Scatter(x=list(weight_cent.values()), y=list(weight_cent.keys()), mode="lines+markers", name="weighted closeness", marker_color="#00CC96")])

    weighted_cent_fig.update_layout(
        title = {
            'text': "Weighted degree Centrality",
            "xanchor": 'center',
            'yanchor': 'top',
            'x': 0.55,
        },
    )


    # closeness_centrality
    '''
    input: graph-networkx.Grpah
    output: dict['attribute']=centrality
    '''
    closeness_cent = nx.closeness_centrality(input_graph)
    closeness_cent = dict(sorted(closeness_cent.items(), key=lambda item:item[1]))
    fig.add_trace(go.Scatter(x=list(closeness_cent.values()), y= list(closeness_cent.keys()), mode="lines+markers", name="closeness", marker_color="#FF6692"))
    closeness_cent_fig = go.Figure(data=[go.Scatter(x=list(closeness_cent.values()), y=list(closeness_cent.keys()), mode="lines+markers", name="closeness", marker_color="#FF6692")])
    closeness_cent_fig.update_layout(
        title = {
            'text': "Closeness Centrality",
            "xanchor": 'center',
            'yanchor': 'top',
            'x': 0.55,
        }
    )


    # betweenness_centrality
    '''
    input: graph-networkx.Grpah
    output: dict['attribute']=centrality
    '''

    between_cent = nx.betweenness_centrality(input_graph, weight='weight', normalized=True)
    between_cent = dict(sorted(between_cent.items(), key=lambda item:item[1]))
    fig.add_trace(go.Scatter(x=list(between_cent.values()), y= list(between_cent.keys()), mode="lines+markers", name="betweenness", marker_color="#AB63FA"))  
    between_cent_fig = go.Figure(data=[go.Scatter(x=list(between_cent.values()), y=list(between_cent.keys()), mode="lines+markers", name="between", marker_color="#AB63FA")])
    between_cent_fig.update_layout(
        title = {
            'text': "Between Centrality",
            "xanchor": 'center',
            'yanchor': 'top',
            'x': 0.55,
        }
    )

    # eigenvector_cntrality
    '''
    input: graph-networkx.Grpah
    output: dict['attribute']=centrality
    '''
    try: 
        eigen_cent = nx.eigenvector_centrality(input_graph, weight='weight')
        eigen_cent = dict(sorted(eigen_cent.items(), key=lambda item:item[1]))
        fig.add_trace(go.Scatter(x=list(eigen_cent.values()), y= list(eigen_cent.keys()), mode="lines+markers", name="eigenvector"))
    except:
        print("eigenvector centrality 오류")
    
    
    # pagerank_centrality
    try:
        pagerank_cent = nx.pagerankG(input_graph, weight='weight')
        pagerank_cent = dict(sorted(between_cent.items(), key=lambda item:item[1]))
        fig.add_trace(go.Scatter(x=list(between_cent.values()), y= list(between_cent.keys()), mode="lines+markers", name="between"))              
    except:
        print("pagerank centrality 오류")
    
    return fig, degree_cent_fig, weighted_cent_fig, closeness_cent_fig, between_cent_fig
    

# callback 함수를 위한 다운로드 함수
def download_file(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), index_col=0 )
        elif "xls" or "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded), index_col=0)
        elif "txt" or "tsv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+", index_col=0)
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    if 'Unnamed: 0' in df.columns:
        print('Unnamed: 0 삭제')
        del df['Unnamed: 0']
        

    # 결측치 제거
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='any')
    
    # print(df.columns)
    return df
    

################ Gaussian Graphical Model =================
# npn Skeptic Algorithm
# input (x) : raw dataframe
def skeptic(x):
    y = 2 * math.sin(math.pi/6. * x)
    return y

def npn(x):
    df = x.corr(method = "spearman")
    result = df.applymap(skeptic)
    return result


# Making Lambda set
# input (df) : npn skeptic corr datatframe의 상삼각행렬
def lamSet(df):
    lamMax = max(np.max(df.values), -np.min(df.values))
    
    lamMin = 0.01 * lamMax
    lamMaxX = math.log(lamMax)
    lamMinX = math.log(lamMin)
    
    lam = np.exp(np.append(np.arange(lamMinX, lamMaxX, step = ((lamMaxX)-(lamMinX))/99), (lamMaxX)))
    
    return lam
# output (lam) : lambda 값 list
# output (result) : npn skeptic corr dataframe


################## computing EBIC ###############
# input (model) : QuicGraphicalLassoEBIC model
# input (n) : data 행 개수
# input (p) : data 열 개수
# input (tr) : npn.values (npn(x)로 계산한 값)
# input (gamma) : gamma 값 (= tuning parameter)
def compute_EBIC(model, n, p, tr, gamma):
    
    prec = model.precision_
    E = (np.sum(np.sum(prec != 0, axis=0))-p)
    MLE = (np.log(np.linalg.det(prec))-np.trace(np.dot(tr, prec))) * n
    EBIC = E * 0.5 * np.log(n) + E * gamma * np.log(p) * 2 - MLE
    
    return EBIC
# output (EBIC) : EBIC 계산값 (float)


################### computing Best Alpha ##############
# input (X): raw dataframe
# input (gamma): gamma 값 (= tuning parameter, 0.1로 설정해두었으나 변경 가능합니다.)

def compute_Best_Alpha(X, gamma = 0.1):
    
    tr = npn(X)
    tr = tr.values # npn skeptic
    triu = pd.DataFrame(np.triu(tr, 1)) # 상삼각행렬 구축
    n=X.shape[0] #data 행 개수
    p=X.shape[1] #data 열 개수
    
    lam = lamSet(triu) # lambda list 계산 값 100개
    EBICs = np.zeros(100) # lambda 개수(100개)만큼 EBIC 값 계산해주기 위해 자리 만듦
        
    # EBIC 계산을 위함, lambda 100개에 대하여 계산해야 하므로 100번 반복
    for i in range(100):
        alpha = round(lam[i], 9)
        model = QuicGraphicalLassoEBIC(lam=alpha, auto_scale = True,
                                           verbose=1, tol = 1e-04,
                                           init_method='spearman', path=100, gamma = gamma, 
                                           max_iter=10000, method='quic').fit(X.values)
        
        # lambda 100개에 대해 EBIC 값 계산
        EBIC = compute_EBIC(model, n, p, tr, gamma)
        # print("EBIC : "+str(EBIC)+" alpha : "+str(alpha))
        EBICs[i]=EBIC
    
    # EBICs 중 EBIC 값이 가장 작은 lambda 선택해서 best_alpha로 설정 
    # -> best_alpha를 model의 최종 lambda로 설정해서 계산할 것임
    best_idx=np.argmin(EBICs)
    best_alpha=lam[best_idx]
    return float(best_alpha)


################# cov to corr ##########################
# input (cov) : cov dataframe (estimator.precision_)

def cov2cor( cov ):
    d = np.sqrt(cov.diagonal())
    cor = ((cov.T/d).T)/d
    cor[ np.diag_indices( cov.shape[0] ) ] = np.ones( cov.shape[0] )
    return cor
# output (cor) : cor dataframe
####################################################

# attribute matrix를 GGM matrix로 만들어주는 함수
def attr_to_ggm(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" or "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    # ---- 알고리즘 시작 ----
    # 결측치 제거
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='any')

    # column name 추출
    columnName = list(df.columns.values)
    # print(columnName)
    # best_alpha 계산
    # gamma 값 0.1로 설정해두었으나 변경 가능합니다.
    best_alpha = compute_Best_Alpha(df) 
    print('best_alpha: ', best_alpha)
    # best_alpha 이용해서 QuicGraphicalLasso 계산, model 구축
    estimator = QuicGraphicalLassoEBIC(lam=best_alpha, auto_scale = False, 
                                       verbose=1, tol = 1e-04,
                                       init_method='spearman', path=100, gamma=0.1, 
                                       max_iter=10000, method='quic').fit(df.values)

    # model.precision_ -> corr 변환 후 상삼각행렬 도출
    df = pd.DataFrame(np.triu(-cov2cor(estimator.precision_),1))
    result = df.copy()

    df.columns = columnName
    df.index = columnName

    # # 결과 Matrix 파일 저장
    # result.to_csv (r'./my_data_frame.csv', index = True, header=True)
    return df


# matrix -> dash table
def make_ggm_table(ggm_matrix=raw_v2):
    '''
    ggm_matrix -> table 객체
    '''
    # save_df = ggm_matrix.copy()
    # print(ggm_matrix.columns)
    if 'Attr' not in ggm_matrix.columns:
         ggm_matrix.insert(0, 'Attr', ggm_matrix.columns, allow_duplicates=False)
         
    return (html.Div(
        [
            dcc.Download(id="corr-matrix-download"),
            html.Label("The Result of Gaussian Graphical Model Analaysis", style={'font-size': 20, 'font-weight': True}),
            html.Button("Save Matrix as CSV", id="corr-matrix-save-button"),
            html.Button("Save Matrix as XLSX", id="xlsx-corr-matrix-save-button"),
            dash_table.DataTable(
                id = "corr-table",
                columns=[{"name": str(i), "id": str(i)} for i in ggm_matrix.columns],
                data=ggm_matrix.to_dict("records"),
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            ),

        ],
    ))



def make_heatmap(ggm_matrix = raw_v2):
    ggm_matrix = round(ggm_matrix, 2)
    
    if 'Attr' in ggm_matrix.columns:
        ggm_matrix.drop(['Attr'], axis=1, inplace=True)

    fig = go.Figure(data=go.Heatmap(
        x = list(ggm_matrix.columns),
        y = list(ggm_matrix.columns),
        z = ggm_matrix,
        zmin= -1,
        zmax= 1,
        colorbar = dict(
            title = "GGM",
            titleside = "top",
        ),
        colorscale = #"RdBu"
            [
                [0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]
            ]
    ))

    fig.update_layout(
        title = {
            "text": "Heatmap of Correlation",
            "x": 0.52,
        },
        height = 700,
        # xaxis_nticks = 36
    )

    return fig