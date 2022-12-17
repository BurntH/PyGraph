import dearpygui.dearpygui as dpg
import networkx as nx
import Core.Force as fs
import Structure.Vec2 as Vec2
import Core.DrawNode as drnd
import Core.DrawEdge as dreg
import uuid

dt = 1

# default and highlight colors
node_df = (255,255,255,255)
edge_df = (255,255,255,255)
node_hl = (255,0,255,255)
edge_hl = (255,0,255,255)


class Editor:
    '''
    Editor will only show things in edge_dict and node_dict.
    '''
    def __init__(self, window = None, graph: nx.Graph = None):
        self.window = window
        if graph == None: graph = nx.Graph()
        self.graph = graph
        self.node_dict = dict()
        self.edge_dict = dict()
        self.scale = 1
        self.offset = Vec2.Vec2(0, 0)

    def graph_to_view_coords(self, pos):
        return (pos - self.offset) * self.scale
    
    def update_window(self):
        # Implementation 1: Use self.graph only
            # Pros: 
            # Cons: Have to mod the graph
        # Implementation 2: Don't mod self.graph and use self.node_dict
            # Pros: Dont have to mod the graph
            # Cons: Don't know if the node was created
        # Problem 1: How do I know a node is created or not?
            # In Implementation 1 we 
            # In Implementation 2 we scan through self.node_dict and update 

        # New Implementaion: Scan through self.graph
            # If in self.node_dict
                # update its attr and mark as updated
            # Else
                # Add the node into self.node_dict
            # Then loop through self.node_dict
                # If it is not marked as updated
                    # Then we remove the node (from window)
                # If it is marked as updated
                    # Reset updated to False and draw it on the screen  
        
        for node in self.graph:
            if node in self.node_dict:
                new_vel = Vec2.Vec2(0, 0)
                for n2 in self.graph.nodes:
                    if node != n2: # Not needed?
                        new_vel += (self.node_dict[n2]["pos"]-self.node_dict[node]["pos"]).normalized() * fs.attraction(self.node_dict[node]["pos"], self.node_dict[n2]["pos"])
                        new_vel += (self.node_dict[node]["pos"]-self.node_dict[n2]["pos"]).normalized() * fs.repulsion(self.node_dict[node]["pos"], self.node_dict[n2]["pos"])
                self.node_dict[node]["vel"] = new_vel
                self.node_dict[node]["pos"] += new_vel*dt
                self.node_dict[node]["updated"] = True
            else:
                self.node_dict[node] = dict()
                self.node_dict[node]["pos"] = Vec2.Vec2(0, 0)
                self.node_dict[node]["vel"] = Vec2.Vec2(0, 0)
                self.node_dict[node]["uuid"] = str((uuid.uuid4()).int)[:8]
                self.node_dict[node]["color"] = (255,255,255,255)
                self.node_dict[node]["updated"] = True
                self.node_dict[node]["created"] = False
                
            for node in self.node_dict:
                if not self.node_dict[node]["updated"]:
                    self.node_dict.remove(self.graph.nodes[node])
                else:
                    if self.node_dict[node]["created"]:
                        drnd.draw_node(self.graph_to_view_coords(self.node_dict[node]["pos"]), self.window, self.node_dict[node]["uuid"],fill_color = self.node_dict[node]["color"], create = False, scale = self.scale)
                    else:
                        drnd.draw_node(self.graph_to_view_coords(self.node_dict[node]["pos"]), self.window, self.node_dict[node]["uuid"],fill_color = self.node_dict[node]["color"], create = True, scale = self.scale)
                        self.node_dict[node]["created"] = True
                        
        #draw edge                 
        for edge in self.graph.edges:
            edge = frozenset(edge)
            self.edge_dict[edge]["ends"][0][1] = self.node_dict[self.edge_dict[edge]["ends"][0][0]]["pos"]
            self.edge_dict[edge]["ends"][1][1] = self.node_dict[self.edge_dict[edge]["ends"][1][0]]["pos"] 
            self.edge_dict[edge]["updated"] = True
            if edge not in self.edge_dict:
                self.edge_dict[edge] = dict()
                self.edge_dict[edge]["uuid"] = str((uuid.uuid4()).int)[:8]
                self.edge_dict[edge]["color"] = (255,255,255,255)
                self.edge_dict[edge]["created"] = False
            
            
            for edge in self.edge_dict:
                if not self.edge_dict[edge]["updated"]:
                    self.edge_dict.remove(self.graph.edges[edge])
                else: 
                    if self.edge_dict[edge]["created"]:
                        dreg.draw_edge(self.graph_to_view_coords(self.edge_dict[edge]["ends"][0][1]), self.graph_to_view_coords(self.edge_dict[edge]["ends"][1][1]), self.window, self.edge_dict[edge]["uuid"], self.edge_dict[edge]["color"], create = False)
                    else:
                        dreg.draw_edge(self.graph_to_view_coords(self.edge_dict[edge]["ends"][0][1]), self.graph_to_view_coords(self.edge_dict[edge]["ends"][1][1]), self.window, self.edge_dict[edge]["uuid"], self.edge_dict[edge]["color"], create = True)
                        self.edge_dict[edge]["created"] = True
                    
### When users edit graph only using mouse and kbd

    def add_node(self, node, pos = [0,0], color = node_df):
        self.graph.add_node(node)
        pos = Vec2.Vec2(pos)
        self.node_dict[node] = dict()
        self.node_dict[node]["pos"] = pos
        self.node_dict[node]["vel"] = Vec2.Vec2(0, 0)
        self.node_dict[node]["uuid"] = str((uuid.uuid4()).int)[:8]
        self.node_dict[node]["color"] = color
        self.node_dict[node]["updated"] = True
        self.node_dict[node]["created"] = False
        
    def add_edge(self, node1, node2, color = edge_df):
        
        edge = frozenset({node1,node2})
        
        self.graph.add_edge(node1, node2)
        self.edge_dict[edge] = dict()
        self.edge_dict[edge]["ends"] = [[node1,self.node_dict[node1]["pos"]], [node2,self.node_dict[node2]["pos"]]]
        self.edge_dict[edge]["uuid"] = str((uuid.uuid4()).int)[:8]
        self.edge_dict[edge]["color"] = color
        self.edge_dict[edge]["updated"] = True
        self.edge_dict[edge]["created"] = False

    # def delete_node(self, node):
    #     self.graph.remove_nodes_from([node])      
    #     self.node_dict.remove(self.graph.nodes[node])

    # def set_node(self, node, data):
    #     pass

    def set_camera(self, scale: float, offset: list):
        self.scale = scale
        self.offset = Vec2.Vec2(offset)
        
    




            