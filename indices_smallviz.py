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
        #truncated list for testing things quickly or on a subset of indices
        self.masterlist = {self.indices[i]:self.masterlist[self.indices[i]] for i in range(len(self.masterlist)) if self.indices[i] in ("NarrativeDevices","NarrativeTropes","NarratorTropes")}
        self.centraltropes = self.get_most_central_tropes("top_100_central.json")
        self.add_trope_nodes()
        self.go_thru_indices_sets()
    
    def write_gml(self,G,name):
        nx.write_gml(G, name+".gml")
        return None
          
    def get_json(self, filename):
        with open(filename) as f:
            jsonobj = json.load(f)
            #print(jsonobj)
        return jsonobj
    
    def write_json(self, data, filename):
        with open(filename,"w") as f:
            json.dump(data,f)
        return None
    
    def show_graph(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos)
        node_labels = nx.get_node_attributes(self.G,'label')
        #print(node_labels)
        nx.draw_networkx_labels(self.G, pos, labels=node_labels)
        return None
    
    def get_most_central_tropes(self, filename):
        centraltropes = self.get_json(filename)
        #print(centraltropes)
        tropelist = []
        for x in centraltropes.values():
            for trope in x:
                tropelist.append(trope)
        print(len(tropelist))
        return set(tropelist)
    
    def add_sets(self):
        for index in self.masterlist: #add all linked tropes as a set
            indexlinks = set(self.masterlist[index])
            self.G.add_node(index,tropes=indexlinks)
        return None
    
    def add_trope_nodes(self):
        supercat = "Narrative-relatedIndicesCentral100Tropes"
        self.G.add_node(supercat,label=supercat)
        print(len(self.centraltropes))
        for index in self.masterlist: #add all linked tropes as nodes
            indexlinks = set([x for x in self.masterlist[index] if x in self.centraltropes])
            self.G.add_node(index,label=index)
            self.G.add_edge(supercat,index)
            for trope in indexlinks:
                self.G.add_node(trope,label=trope)
                self.G.add_edge(index,trope)
        self.write_gml(self.G, supercat)
        return None
    
    def histogram_plot(self, datax, datay):
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(datax, bins=100)
        axs[1].hist(datay, bins=100)
        plt.show()
        return None

    def go_thru_indices_sets(self):
        for idx, node in enumerate(self.G.nodes()):
            pass
        return None

i = IndexGraph()
i.show_graph()

    