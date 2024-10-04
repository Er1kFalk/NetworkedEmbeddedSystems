# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:55:54 2024

@author: Erik
"""

from enum import Enum

class DeviceType(Enum):
    NA = 0
    ES = 1
    SW = 2

class Node:
    """
    A datastructure for representing Network nodes
    """
    deviceType = DeviceType.NA
    deviceName = ''
    ports = 0
    domain = ''
    
    def __init__(self, deviceType = DeviceType.NA, deviceName = '', ports = 0, domain = ''):
        """
        Parameters
        ----------
        deviceType : Enum DeviceType, optional
            The default is DeviceType.NA.
        deviceName : String, optional
            The default is ''.
        ports : int, optional
            The default is 0.
        domain : string, optional
            The default is ''.

        Returns
        -------
        None.

        """
        self.deviceType = deviceType
        self.deviceName = deviceName
        self.ports = ports
        self.domain = domain

class Link:
    link = ''
    linkId = 0
    source = Node()
    destination = Node()

class NetworkGraph:
    """
    A datastructure for storing network graphs
    """
    edges = [] # list of (n1, n2) where n1=start node, n2=end node
    vertices = [] # list of (id, s) where id is a unique integer, and s is a name for the node
    def __init__(self, edges, vertices):
        """
        Parameters
        ----------
        edges : (n1, n2)
            - edges : list of (n1, n2) where n1=start Node, n2=end Node
            - vertices: list of (id, node) where id is a unique integer, and node is a Node
        vertices : Node
        Returns
        -------
        None.

        """
        self.edges = edges
        self.vertices = vertices
        self.nodeId = 0
        
    def addEdge(self, edge):
        """
        Adds an edge to the network graph.
        
        Parameters
        ----------
        edge : Link
            Edges are defined as links.

        Returns
        -------
        None.

        """
        self.edges.append(edge)
    
    def addVertice(self, vertice):
        """
        Adds a vertice (node) to the network graph.
        
        Parameters
        ----------
        vertice : Node

        Returns
        -------
        None.

        """
        self.vertices.append(vertice)
        
