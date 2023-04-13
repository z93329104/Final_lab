from final_project_part1 import *
import csv
station_line = {}
direct_dis = {}
path_length = {}


def add_different_value(list,v1,v2):
    # This function check if v1 and v2 are in the list, if not then add them to list.
    if not v1 in list:
        list.append(v1)
    if not v2 in list:
        list.append(v2)

with open('london_stations.csv', mode ='r')as file:
    ls_csv = csv.reader(file)
    for line in ls_csv:
        if line[0] == "id":
            continue
        direct_dis[line[0]] = (line[1],line[2],line[6])

with open("london_connections.csv", mode = 'r') as file:
    lc_csv = csv.reader(file)
    
    for line in lc_csv:
        if line[0] == "station1":
            continue
        if line[2] not in station_line.keys():
            station_line[line[2]] = []
        add_different_value(station_line[line[2]],line[0],line[1])
        path_length[(line[0],line[1])] = line[3]
print(direct_dis)

def h(s,d):
    return ((direct_dis[s][0] - direct_dis[d][0])**2 + (direct_dis[s][1] - direct_dis[d][1])**2)**(1/2)

def a_star(G, s, d, h):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, h(s,d))   
    while not Q.is_empty():
        current_element = Q.extract_min()
        if current_element == d:
            break
        current_node = current_element.value
        dist[current_node] = current_element.key - h[current_node]
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h(neighbour,d) )
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return (pred, path_from_pred(pred,s,d))

def create_london_graph():
    G = DirectedWeightedGraph()
    
