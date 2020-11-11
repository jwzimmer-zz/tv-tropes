#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 2020

@author: jzimmer1, philnguyen
"""
import os
import json
import networkx as nx
from itertools import combinations

class IndexGraph():
    def __init__(self):
        self.G = nx.Graph()
        self.masterlist = self.get_json('index-list/index-list.json')
    
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
        self.write_gml(self.G,"indices")
        return self.G

i = IndexGraph()
i.go_thru_indices(5000)
    