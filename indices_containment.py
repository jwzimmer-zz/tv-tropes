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
        self.indices = [x for x in self.masterlist.keys()]
        self.masterlist = {self.indices[i]:self.masterlist[self.indices[i]] for i in range(1000)}
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
    
    def histogram_plot(self, datax, datay):
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(datax, bins=100)
        axs[1].hist(datay, bins=100)
        plt.show()
        return None
    
    def remove_set_attributes(self,attr):
        #need to do this in order to write the graph to gml (since the sets are not string type)
        for idx,node in enumerate(self.G.nodes()):
            try:
                del self.G.nodes[node][attr]
            except:
                pass
        return None

    def go_thru_indices_sets(self):
        for idx, node in enumerate(self.G.nodes()):
            firstsetoftropes = self.G.nodes[node]['tropes']
            self.G.nodes[node]["shared-tropes"] = 0
            for idy, node2 in enumerate(self.G.nodes()):
                if idx != idy:
                    secondsetoftropes = self.G.nodes[node2]["tropes"]
                    if len(list(firstsetoftropes))+len(list(secondsetoftropes)) == 0:
                        # print(node,node2)
                        # print(firstsetoftropes,secondsetoftropes)
                        # print(" ")
                        pass
                    else:
                        # print(node,node2)
                        # print(firstsetoftropes, secondsetoftropes)
                        # print(" ")
                        self.G.nodes[node]["shared-tropes"] += len(list(firstsetoftropes.intersection(secondsetoftropes)))/(len(list(firstsetoftropes))+len(list(secondsetoftropes)))
        nodelist = [x for x in self.G.nodes]
        for n in nodelist:
            try:
                self.G.nodes[n]["shared-tropes"] = self.G.nodes[n]["shared-tropes"]/len(nodelist)
            except:
                pass
        self.remove_set_attributes("tropes")
        self.rG = self.G
        print(len(self.G.nodes),len(self.G.edges))
        #self.write_gml(self.G, "howsimilar")
        self.scores = nx.get_node_attributes(self.G, "shared-tropes")
        self.histogram_plot(self.scores.keys(),self.scores.values())
        return self.rG

i = IndexGraph()

    