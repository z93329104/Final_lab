import min_heap
import random

class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d

def dijkstra_approx(G, source, k):
    pred = {}
    dist = {}
    relax = {}
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relax[node] = k
    Q.decrease_key(source, 0)
    relax[source] = relax[source] - 1
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                if relax[neighbour] > 0:
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                    relax[neighbour] = relax[neighbour] - 1 
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
    return dist
    
def bellman_ford_approx(G, source, k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    relax = {}
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        relax[node] = k
    dist[source] = 0
    relax[source] = relax[source] - 1
    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour) and relax[neighbour] > 0:
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    relax[neighbour] = relax[neighbour] - 1 
                    pred[neighbour] = node
    return dist

def a_star(G, s, d, h):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, h[s])   
    while not Q.is_empty():
        current_element = Q.extract_min()
        if current_element == d:
            break
        current_node = current_element.value
        dist[current_node] = current_element.key - h[current_node]
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour] )
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return (pred, path_from_pred(pred,s,d)) 


def path_from_pred(pred,start_node,end_node):
    path = []
    current_node = end_node
    while current_node != start_node:
        path.append(current_node)
        current_node = pred[current_node]
    path.append(current_node)
    path.reverse()
    return path

# Test
'''
G=DirectedWeightedGraph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_edge(1,2,5)
G.add_edge(2,3,5)
G.add_edge(3,4,3)
G.add_edge(4,5,3)
G.add_edge(1,5,7)
G.add_edge(5,6,1)
h = {1:2,2:4,3:3,4:2,5:1,6:0}
d=a_star(G,1,6,h)
print(d)
'''