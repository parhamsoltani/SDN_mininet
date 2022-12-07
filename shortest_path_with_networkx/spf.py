import networkx as nx
import matplotlib.pyplot as plt

# This is a modified version which gets the updated Weight_Mat after link cahnges
def calculated_shortest_path_for_P4(Weight_Mat_Update):
    # Making the weight matrix as "networkx" object, based on the text data
    G=nx.DiGraph()
    for i in range(0,len(weight_Mat_Update):
        for j in range(0,len(weight_Mat_Update)):
            if weight_Mat_Update[i][j]!=0:
                G.add_edge(i,j,weight_Mat_Update[i][j])
        
    # Calculating the shortest path between nodes "1" and "n", then returning it
    path1=nx.shortest_path(G,source=0,target=len(weight_Mat_Update) - 1, weight='weight', method='dijkstra')
    path2=nx.shortest_path(G,source=0,target=len(weight_Mat_Update) - 1, target=0, weight='weight', method='dijkstra')
    return path1, path2
