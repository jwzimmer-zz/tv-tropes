#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 2020

@author: jzimmer1, philnguyen
"""
import os
import json
from networkx import algorithms
from networkx import community
from networkx import centrality
import networkx as nx
import itertools

class IndexGraph():
    def __init__(self):
        self.G = nx.Graph()
        self.masterlist = self.get_json('index-list/index-list.json')
        self.go_thru_indices_threshold()
    
    def write_gml(self,G,name):
        nx.write_gml(G, name+".gml")
        return None
          
    def get_json(self, filename):
        with open(filename) as f:
            jsonobj = json.load(f)
        return jsonobj
    
    def show_graph(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos)
        node_labels = nx.get_node_attributes(self.G,'label')
        nx.draw_networkx_labels(self.G, pos, labels=node_labels)
        return None
    
    def go_thru_indices(self, maxn):
        i = 0        
        for index in self.masterlist:
            #self.G.add_node(index,name=index) #add some node attribute here
            if i < maxn:
                indexlinks = self.masterlist[index]
                for il in indexlinks:
                    #self.G.add_node(il,name=il) #add some node attribute here
                    self.G.add_edge(index, il)
                    #self.show_graph()
                i+=1
            else: return None
        #self.write_gml(self.G,"indices")
        return self.G
    
    def go_thru_indices_threshold(self):
        i = 0
        avgnumberlinks = 93.82385016595543 #only looking at indices with above the average number of links still yields a graph with 26747 nodes
        for index in self.masterlist:
            indexlinks = set(self.masterlist[index])
            self.G.add_node(index,tropes=indexlinks)
        for idx, node in enumerate(self.G.nodes()):
            for idy, node2 in enumerate(self.G.nodes()):
                if idx != idy:
                    scoreval = len(list(self.G.nodes[node]["tropes"].intersection(self.G.nodes[node]["tropes"])))
                    self.G.add_edge(node, node2, score=scoreval)
        for idx,node in enumerate(self.G.nodes()):
            del self.G.nodes[node]["tropes"]
        self.write_gml(self.G,"indices_common_trope_score")
        return self.G
    
    def basic_analysis(self, k):
        girvannewman = nx.algorithms.community.centrality.girvan_newman(self.G)
        limited = itertools.takewhile(lambda c: len(c) <= k, girvannewman)
        for comm in limited:
            self.gn6 = comm
        with open('girvannewman6_indices_all.json', 'w') as f:
            json.dump(self.gn6, f)
        return None

i = IndexGraph()
#i.basic_analysis(6)

    