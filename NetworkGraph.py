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
    ES = 1 # end system
    SW = 2 # switch

class Node:
    """
    A datastructure for representing Network nodes
    """
    def __init__(self, deviceType : DeviceType = DeviceType.NA, deviceName = '', ports = 0, domain = ''):
        self.deviceType = deviceType
        self.deviceName = deviceName
        self.ports = ports
        self.domain = domain
    
class Link:
    def __init__(self, linkId = '', sourceDevice = '', sourcePort = 0, destinationDevice = '', destinationPort = 0, domain = ''):
        self.linkId = linkId # unique id for link
        self.sourceDevice = sourceDevice # identifier for sourcedevice
        self.sourcePort = sourcePort
        self.destinationDevice = destinationDevice # identifier for destination device
        self.destinationPort = destinationPort
        self.domain = domain # identifier of domain to which link belongs
    
class StreamType(Enum):
    NONE = 0
    ATS = 1 # ATS stream
    AVB = 2 # AVB stream
    
class Stream:
    def __init__(self, PCP = 0, streamName = '', streamType : StreamType = StreamType.NONE, sourceNode = '', destinationNode = '', size = 0, period = 0, deadline = 0):
        self.PCP = PCP # PRIORITY CODE POINT - indicating priority of stream
        self.streamName = streamName # unique identifier for the stream
        self.streamType = streamType
        self.sourceNode = sourceNode # identifier of the sourcenode (endsystems - ES) of the stream
        self.destinationNode = destinationNode # identifier of the endnode (endsystems - ES) of the stream
        self.size = size # size of stream packets in bytes
        self.period = period # period of the stream (units specified in config file)
        self.deadline = deadline # deadline of the stream (units specified in config file)


class Vertice:
    def __init__(self, node : Node):
        self.current = node
        self.parent = None

class NetworkGraph:
    
    def __init__(self):
        """
        A datastructure for storing network graphs
        """
        self.edges = [] # list of (n1, n2) where n1=start node, n2=end node
        self.vertices = [] # list of (id, s) where id is a unique integer, and s is a name for the node
        self.paths = [] # streams
    
    def addEdge(self, edge : Link):
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
    
    def addVertice(self, v : Vertice):
        """
        Adds a vertice (node) to the network graph.
        
        Parameters
        ----------
        vertice : Node

        Returns
        -------
        None.

        """
        self.vertices.append(v) # (vertice, parent)
        
    def getVerticeFromString(self, deviceName : str):
        for i in range(len(self.vertices)):
            if (self.vertices[i].current.deviceName == deviceName):
                return self.vertices[i]
        raise "vertice not found"
    
    def addPath(self, path):
        self.paths.append(path)
        
    def clearParents(self):
        for i in range(len(self.vertices)):
            self.vertices[i].parent = None
            
    def addParent(self, deviceName, parent : Vertice):
        for i in range(len(self.vertices)):
            if (self.vertices[i].current.deviceName == deviceName):
                self.vertices[i].parent = parent
                return self
        
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
                self.addVertice(Vertice(tmpNode))
                
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
    
    def getNeighbours(self, vertice : Vertice):
        neighbours = []
        # links goes both ways (not one directional)
        for link in self.edges:
            if link.sourceDevice == vertice.current.deviceName:
                neighbours.append(self.getVerticeFromString(link.destinationDevice))
            if link.destinationDevice == vertice.current.deviceName:
                neighbours.append(self.getVerticeFromString(link.sourceDevice))

        return set(neighbours)
     
    def getPathFromVertice(self, vertice : Vertice):
        getNode = vertice
        path = [getNode.current]
        while (getNode.parent):
            getNode = getNode.parent
            path.append(getNode.current)
        return path[::-1]
    
    def bfs(self, start : str, target : str):
        self.clearParents()
        startVertice = self.getVerticeFromString(start)
        endVertice = self.getVerticeFromString(target)
        
        visited = set()
        queue = deque()
        
        visited.add(startVertice.current)
        queue.append(startVertice)
        
        while len(queue) != 0:
            v = queue.popleft()
            if (v.current.deviceName == endVertice.current.deviceName):
                return v
            nb = self.getNeighbours(v)
            for neighbour in nb:
                if neighbour.current not in visited:
                    visited.add(neighbour.current)
                    self.addParent(neighbour.current.deviceName, v)
                    queue.append(neighbour)
            
            
        

nwg = NetworkGraph()
nwg.readNetworkTopology().readNetworkStream()
path = nwg.getPathFromVertice(nwg.bfs("ES_72", "ES_86"))


