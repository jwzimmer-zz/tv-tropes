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
import matplotlib.pyplot as plt

class IndexGraph():
    def __init__(self):
        self.G = nx.Graph()
        self.masterlist = self.get_json('index-list/index-list.json')
        self.add_sets()
        self.go_thru_indices_sets()
    
    def write_gml(self,G,name):
        nx.write_gml(G, name+".gml")
        return None
          
    def get_json(self, filename):
        with open(filename) as f:
            jsonobj = json.load(f)
        return jsonobj
    
    def write_json(self, data, filename):
        with open(filename,"w") as f:
            json.dump(data,f)
        return None
    
    def show_graph(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos)
        node_labels = nx.get_node_attributes(self.G,'label')
        nx.draw_networkx_labels(self.G, pos, labels=node_labels)
        return None
    
    def add_sets(self):
        for index in self.masterlist: #add all linked tropes as a set
            indexlinks = set(self.masterlist[index])
            self.G.add_node(index,tropes=indexlinks)
        return None
    
    def histogram_plot(self, data):
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(data, bins=100)
        axs[1].hist(data, bins=100)
        plt.show()
        return None
    
    def remove_set_attributes(self,attr):
        #need to do this in order to write the graph to gml (since the sets are not string type)
        for idx,node in enumerate(self.G.nodes()):
            del self.G.nodes[node][attr]
        return None

    def go_thru_indices_sets(self):
        for idx, node in enumerate(self.G.nodes()):
            for idy, node2 in enumerate(self.G.nodes()):
                if idx != idy:
                    firstsetoftropes = self.G.nodes[node]["tropes"]
                    secondsetoftropes = self.G.nodes[node2]["tropes"]
                    if firstsetoftropes.issuperset(secondsetoftropes):
                        self.G.add_edge(node, node2) #add an edge between indices when one completely contains the other
                    self.G.nodes[node]["unique-tropes"] = firstsetoftropes.difference(secondsetoftropes) #reduce to only the unique tropes to that index
        # for idx, node in enumerate(self.G.nodes()):
        #     setoftropes = self.G.nodes[node]["unique-tropes"]
        #     for trope in setoftropes:
        #         self.G.add_edge(node, trope)
        self.remove_set_attributes("tropes")
        self.remove_set_attributes("unique-tropes")
        self.rG = self.G
        print(len(self.G.nodes),len(self.G.edges))
        self.write_gml(self.G, "containment_uniquesets")
        return self.rG

i = IndexGraph()

    