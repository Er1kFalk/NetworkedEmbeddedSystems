# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:55:54 2024

@author: Erik
"""

class NetworkGraph:
    edges = [] # list of (n1, n2) where n1=start node, n2=end node
    vertices = [] # list of (id, s) where id is a unique integer, and s is a name for the node
    nodeId = 0
    def __init__(self, edges, vertices):
        self.edges = edges
        self.vertices = vertices
        self.nodeId = 0
        
    def addEdge(self, fromNode, toNode):
        self.edges.append(fromNode, toNode)
    
    def addVertice(self, name):
        self.vertices.append(self.nodeId, name)
        self.nodeId += 1
        
