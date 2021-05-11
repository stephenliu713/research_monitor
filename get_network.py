import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import research_monitor_func as func

color_nw = 'lightseagreen'

def make_edge(x,y,text,width):
    return go.Scatter(x = x,
                      y = y,
                      line = dict(width = width, color = color_nw),
                      hoverinfo = 'text',
                      text = [text],
                      textposition= "bottom center",
                      mode = 'lines',
                      )

def make_text(x,y,text):
    return go.Scatter(x = x,
                      y = y,
                      mode = 'markers',
                      text = text,
                      textposition='bottom center',
                      hoverinfo='text')

def main():
    print("Generating cooperation network of authors...")

    path_data_network = func.get_abspath_folder_lastquarter() + 'data_network_{}.xlsx'.format(func.get_last_2_quarters())
    df_result = pd.read_excel(path_data_network)
    # print(df_result)

    # get namelist
    path_namelist = func.get_abspath_researcher()
    namelist = pd.read_excel(path_namelist)
    firstname = namelist['First name']
    lastname = namelist['Last name']
    fullname_list = lastname + ', ' + firstname
    fullname_list = fullname_list.drop([0])
    # print(fullname_list)

    # edges
    dict_edges = {}
    for fullname in fullname_list:
        dict_temp = {}
        df_temp = df_result.loc[(df_result[fullname] == 1)]
        for fullname2 in fullname_list:
            if fullname2 != fullname:
                dict_temp[fullname2] = df_temp[fullname2].sum()
        dict_edges[fullname] = dict_temp
    # print(dict_edges)

    # nodes
    dict_nodes = {}
    for fullname in fullname_list:
        df_temp = df_result.loc[(df_result[fullname] == 1)]
        dict_nodes[fullname] = df_temp[fullname].sum()
    # print(dict_nodes)

    # network
    nw_author = nx.Graph()
    for node in dict_nodes.keys(): #nodes
        if dict_nodes[node]>0:
            nw_author.add_node(node,size=dict_nodes[node])

    for edge in dict_edges.keys():
        for co_edge in dict_edges[edge].keys():
            if dict_edges[edge][co_edge] > 0:
                nw_author.add_edge(edge,co_edge,weight = dict_edges[edge][co_edge])

    # get positions
    pos_ = nx.spring_layout(nw_author)

    # make edge trace
    edge_trace = []
    text_trace = []
    for edge in nw_author.edges():
        if nw_author.edges()[edge]['weight']>0:
            char_1 = edge[0]
            char_2 = edge[1]
        x0,y0 = pos_[char_1]
        x1,y1 = pos_[char_2]
        text = char_2 + ': ' + str(nw_author.edges()[edge]['weight'])
        edge_trace_tmp = make_edge([x0,x1,None],[y0,y1,None],text,width=nw_author.edges()[edge]['weight']**0.5)
        edge_trace.append(edge_trace_tmp)
    for edge in nw_author.edges():
        if nw_author.edges()[edge]['weight']>0:
            char_1 = edge[1]
            char_2 = edge[0]
        x0,y0 = pos_[char_1]
        x1,y1 = pos_[char_2]
        text = char_2 + ': ' + str(nw_author.edges()[edge]['weight'])
        edge_trace_tmp = make_edge([x0,x1,None],[y0,y1,None],text,width=nw_author.edges()[edge]['weight']**0.5)
        edge_trace.append(edge_trace_tmp)


    # make node trace
    node_trace = go.Scatter(x = [],
                            y = [],
                            text = [],
                            textposition = "top center",
                            textfont_size = 10,
                            mode = 'markers+text',
                            hoverinfo = 'none',
                            marker = dict(color=[],size=[],line=None))
    for node in nw_author.nodes():
        x,y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple([color_nw])
        # node_trace['marker']['size'] += tuple([5*nw_author.nodes()[node]['size']])
        node_trace['text'] += tuple(['<b>'+node+'</b>'])


    # customize layout
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',hovermode='x')
    fig = go.Figure(layout=layout)
    for trace in edge_trace:
        fig.add_trace(trace)
    fig.add_trace(node_trace)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    path_html = func.get_abspath_folder_lastquarter() + "network_author.html"
    fig.write_html(path_html)

    print("Successfully generated cooperation network under path: {}".format(path_html))



if __name__ == '__main__':
    main()