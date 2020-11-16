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
import collections
import random

class IndexGraph():
    def __init__(self):
        self.G = nx.Graph()
        #self.G = nx.read_gml("BigFour_tropes_all4_top10000_top50_top20.gml") #read in a saved graph from gml
        self.masterlistallindices = self.get_json('index-list/index-list.json')
        self.indices = [x for x in self.masterlistallindices.keys()]
        #truncated list for testing things quickly or on a subset of indices
        self.masterlist = {self.indices[i]:self.masterlistallindices[self.indices[i]] for i in range(len(self.masterlistallindices)) if self.indices[i] in ("MediaTropes","NarrativeTropes","TopicalTropes","GenreTropes")}
        self.centraltropes = self.get_most_central_tropes_by_all_4_metrics("top_100_central.json")
        self.masterlisttropes = self.get_json('all-tropes-with-links.json')
        self.supercat = "BigFour_subindices_and_tropes_top100_genre"
        self.bigfourdict = self.get_json("main4_subindices_dict.json")
        self.add_trope_nodes()
        #self.basic_analysis(6, "girvan_newman")
    
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
        #print(len(tropelist))
        return set(tropelist)
    
    def get_most_central_tropes_by_all_4_metrics(self, filename):
        centraltropes = self.get_json(filename)
        #print(centraltropes)
        tropelist = []
        for x in centraltropes.values():
            for trope in x:
                tropelist.append(trope)
        trope_centrality_counts = collections.Counter(tropelist)
        tropelist = [x for x in trope_centrality_counts if trope_centrality_counts[x] == 4]
        #print(len(tropelist))
        return set(tropelist)
    
    def add_trope_nodes(self):
        supercat = self.supercat
        #self.G.add_node(supercat,label=supercat)
        for index in self.bigfourdict: #add all linked tropes as nodes
            if index == "GenreTropes": #splitting network into each index because too many edges (~11000)
                bigfourtropes = self.masterlist[index]
                self.G.add_node(index,label=index)
                for subindex in self.bigfourdict[index]: #subindices and tropes (?)
                    if subindex in self.G.nodes:
                        self.G.add_edge(index,subindex)
                    else:
                        self.G.add_node(subindex,label=subindex)
                        self.G.add_edge(index,subindex)
                    for trope in [x for x in self.bigfourdict[index][subindex] if x in self.centraltropes]: #reduce trope nodes by only looking at top central ones
                        if trope in self.G.nodes:
                            self.G.add_edge(subindex,trope)
                        else:
                            self.G.add_node(trope,label=trope)
                            self.G.add_edge(subindex,trope)
                for tr in bigfourtropes:
                    if tr in self.G.nodes:
                        pass
                    else:
                        if tr in self.centraltropes:
                            self.G.add_edge(index,tr)
                        else:
                            pass
            else:
                pass
        print(len(self.G.nodes), len(self.G.edges)) #23543 - too many nodes! too slow; reduce by looking in self.centraltropes
        self.write_gml(self.G, supercat+"genre")
        return None
    
    def histogram_plot(self, datax, datay):
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(datax, bins=100)
        axs[1].hist(datay, bins=100)
        plt.show()
        return None
    
    def basic_analysis(self, k, algorithm):
        algoresult = nx.algorithms.community.centrality.girvan_newman(self.G)
        limited = itertools.takewhile(lambda c: len(c) <= k, algoresult)
        for comm in limited:
            self.gn6 = comm
        with open(self.supercat+str(algorithm)+str(k)+'.json', 'w') as f:
            for setitem in self.gn6:
                print(setitem)
                json.dump(list(setitem), f)
        return None

i = IndexGraph()
i.show_graph()

    