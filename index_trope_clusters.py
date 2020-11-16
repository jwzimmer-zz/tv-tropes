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

class IndexGraph():
    def __init__(self):
        #self.G = nx.Graph()
        self.G = nx.read_gml("BigFour_tropes_all4_top10000_top50_top20_theirtropes.gml") #read in a saved graph from gml
        self.masterlist = self.get_json('index-list/index-list.json')
        self.indices = [x for x in self.masterlist.keys()]
        #truncated list for testing things quickly or on a subset of indices
        self.masterlist = {self.indices[i]:self.masterlist[self.indices[i]] for i in range(len(self.masterlist)) if self.indices[i] in ("MediaTropes","NarrativeTropes","TopicalTropes","GenreTropes")}
        self.centraltropes = self.get_most_central_tropes_by_all_4_metrics("top_10000_central.json")
        self.masterlisttropes = self.get_json('all-tropes-with-links.json')
        self.supercat = "BigFour_tropes_all4_top10000_top50_top20_theirtropes"
        #self.add_trope_nodes()
        #self.go_thru_graph()
        self.basic_analysis(6)
    
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
        print(len(tropelist))
        return set(tropelist)
    
    def add_sets(self):
        for index in self.masterlist: #add all linked tropes as a set
            indexlinks = set(self.masterlist[index])
            self.G.add_node(index,tropes=indexlinks)
        return None
    
    def add_trope_nodes(self):
        supercat = self.supercat
        self.G.add_node(supercat,label=supercat)
        for index in self.masterlist: #add all linked tropes as nodes
            indexlinks = []
            for x in self.masterlist[index]:
                #if x not in indexlinks:
                if x in self.centraltropes and x not in indexlinks:
                    indexlinks.append(x)
                if len(indexlinks) > 50:
                    break
            self.G.add_node(index,label=index)
            self.G.add_edge(supercat,index)
            for trope in indexlinks:
                self.G.add_node(trope,label=trope)
                self.G.add_edge(index,trope)
                tropetropelinks = self.masterlisttropes[trope]
                print(len(tropetropelinks))
                tropetropenodes = []
                for tropelink in tropetropelinks:
                    if tropelink in self.centraltropes and tropelink not in tropetropenodes:
                        tropetropenodes.append(tropelink)
                    if len(tropetropenodes) > 20:
                        break
                for tr in tropetropenodes:
                    self.G.add_node(tr,label=tr)
                    self.G.add_edge(trope, tr)
                    trlinks = self.masterlisttropes[tr]
                    for trl in trlinks:
                        if trl in self.G.nodes:
                            self.G.add_edge(tr, trl)
        self.write_gml(self.G, supercat)
        return None
    
    def histogram_plot(self, datax, datay):
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(datax, bins=100)
        axs[1].hist(datay, bins=100)
        plt.show()
        return None
    
    def basic_analysis(self, k):
        girvannewman = nx.algorithms.community.centrality.girvan_newman(self.G)
        limited = itertools.takewhile(lambda c: len(c) <= k, girvannewman)
        for comm in limited:
            self.gn6 = comm
        with open(self.supercat+'girvannewman6k.json', 'w') as f:
            for setitem in self.gn6:
                json.dump(list(setitem), f)
        return None

    def go_thru_graph(self):
        for idx, node in enumerate(self.G.nodes()):
            pass
        return None

i = IndexGraph()
i.show_graph()

    