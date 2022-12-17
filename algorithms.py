import dearpygui.dearpygui as dpg
import networkx as nx
import math

### default colors ###
node_df = (255,255,255,255)
edge_df = (255,255,255,255)
node_dfhl = (255,0,255,255)
edge_dfhl = (255,0,255,255)


### highlight ###
def hl_node(ed, nodes, hl:tuple = node_dfhl): # highlights a node, or nodes in a list
    if type(nodes) == list:
        for node in nodes:
            ed.node_dict[node]["color"] = hl
    else:
        ed.node_dict[nodes]["color"] = hl
    return None
    
def hl_edge(ed, edges, hl:tuple = node_dfhl): # highlights an edge, or edges in a list
    if type(edges) == list:
        for edge in edges:
            ed.edge_dict[frozenset(edge)]["color"] = hl
    else:
        ed.edge_dict[frozenset(edges)]["color"] = hl
    return None
    

### distance properties ###
def dist(ed, source, target): # returns distance between source and target nodes
    return len(list(nx.shortest_simple_paths(ed.graph, source, target))[0])-1

def hl_shortest_path(ed, source, target, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path between source and target nodes
   
    path = list(nx.shortest_simple_paths(ed.graph, source, target))[0]
    hl_node(ed, [path[0], path[-1]], node_hl)
    
    if len(path)>1:
        hl_edge(ed, [{path[i],path[i+1]} for i in range(len(path)-1)], edge_hl)
    return None

def eccentricity(ed, *args): # returns a dictionary consisting of each node's eccentricity, or the eccentricity of a particular node
    if len(args) == 0:
        if nx.is_connected(ed.graph):
            return nx.eccentricity(ed.graph)
        else: 
            return {node:math.inf for node in ed.graph.nodes}
    if len(args) == 1:
        if nx.is_connected(ed.graph):
            return nx.eccentricity(ed.graph)[args[0]]
        else:
            return math.inf
        
def hl_eccentricity(ed, node, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path between input node and another node with its length being the eccentricity of the input node
    if nx.is_connected(ed.graph):
        for n2 in ed.node_dict:
            if dist(ed, node, n2) == eccentricity(ed, node):
                hl_shortest_path(ed, node, n2, node_hl, edge_hl)
                return None
    return None
    # this seems inefficient
        
def diameter(ed): # returns the diameter (maximum eccentricity) 
    if nx.is_connected(ed.graph):
        return nx.diameter(ed.graph)
    else:
        return math.inf  
    
def periphery(ed): # returns a list of nodes in periphery. the periphery is the set of nodes with eccentricity equal to the diameter.    
    if nx.is_connected(ed.graph):
        return nx.periphery(ed.graph)
    return None

def hl_periphery(ed, hl = node_dfhl): # highlights the periphery
    hl_node(ed, periphery(ed), hl)
    return None

def hl_diameter(ed, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path whose length is the diameter
    hl_eccentricity(ed, periphery(ed)[0], node_hl, edge_hl)
    return None

def radius(ed): # returns the radius (minimum eccentricity) 
    if nx.is_connected(ed.graph):
        return nx.radius(ed.graph)
    else:
        return math.inf  
    
def center(ed): # returns a list of center nodes. the center is the set of nodes with eccentricity equal to radius.    
    if nx.is_connected(ed.graph):
        return nx.center(ed.graph)
    return None

def hl_center(ed, hl = node_dfhl): # highlights the center
    hl_node(ed, center(ed), hl)
    return None

def hl_radius(ed, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path whose length is the radius
    hl_eccentricity(ed, center(ed)[0], node_hl, edge_hl)
    return None

                
