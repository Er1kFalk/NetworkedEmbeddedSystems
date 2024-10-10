# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:55:54 2024

@author: Erik
"""

from enum import Enum
from CSVUtilities import getCsvLines
from collections import deque

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
    
class Link:
    linkId = 0
    sourceDevice = ''
    sourcePort = 0
    destinationDevice = ''
    destinationPort = 0
    domain = ''
    
class StreamType(Enum):
    NONE = 0
    ATS = 1
    AVB = 2
    
class Stream:
    PCP = 0
    streamName = ''
    streamType = StreamType.NONE
    sourceNode = ''
    destinationNode = ''
    size = 0
    period = 0
    deadline = 0


class NetworkGraph:
    """
    A datastructure for storing network graphs
    """
    edges = [] # list of (n1, n2) where n1=start node, n2=end node
    vertices = [] # list of (id, s) where id is a unique integer, and s is a name for the node
    paths = [] # streams
    
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
    
    def addPath(self, path):
        self.paths.append(path)
        
    def readNetworkTopology(self):
        nodeLines = getCsvLines('ExampleFiles/example_topology.csv')
        for line in nodeLines:
            if (line[0] == 'LINK'):
                tmpLink = Link()            
                tmpLink.linkId = line[1]
                tmpLink.sourceDevice = line[2]
                tmpLink.sourcePort = int(line[3])
                tmpLink.destinationDevice = line[4]
                tmpLink.destinationPort = int(line[5])
                tmpLink.domain = line[6]
                self.addEdge(tmpLink)
            else:
                tmpNode = Node()
                if (line[0] == 'ES'):
                    tmpNode.deviceType = DeviceType.ES
                elif (line[0] == 'SW'):
                    tmpNode.deviceType = DeviceType.SW
                tmpNode.deviceName = line[1]
                tmpNode.ports = int(line[2])
                tmpNode.domain = line[3]
                self.addVertice(tmpNode)
                
        return self

    def readNetworkStream(self):
        streamLines = getCsvLines('ExampleFiles/example_streams.csv')
        for line in streamLines:
            tmpStream = Stream()
            tmpStream.PCP = int(line[0])
            tmpStream.streamName = line[1]
            if (line[2] == 'ATS'):
                tmpStream.streamType = StreamType.ATS
            elif (line[2] == 'AVB'):
                tmpStream.streamType = StreamType.AVB
            else:
                raise "parsing error - not a valid streamtype"
            tmpStream.sourceNode = line[3]
            tmpStream.destinationNode = line[4]
            tmpStream.size = int(line[5])
            tmpStream.period = int(line[6])
            tmpStream.deadline = int(line[7])
            self.addPath(tmpStream)
        return self
        
nwg = NetworkGraph()
nwg.readNetworkTopology().readNetworkStream()



