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
import re

class IndexGraph():
    def __init__(self):
        self.G = nx.Graph()
        #self.G = nx.read_gml("BigFour_tropes_all4_top10000_top50_top20.gml") #read in a saved graph from gml
        self.masterlistallindices = self.get_json('index-list/index-list.json')
        self.indices = [x for x in self.masterlistallindices.keys()]
        #truncated list for testing things quickly or on a subset of indices
        # self.masterlist = {self.indices[i]:self.masterlistallindices[self.indices[i]] for i 
        #                     in range(len(self.masterlistallindices))}
        self.masterlist = self.masterlistallindices
        self.centraltropes = self.get_most_central_tropes_by_all_4_metrics("top_10000_central.json")
        self.masterlisttropes = self.get_json('all-tropes-with-links.json')
        self.supercat = "indices_split_anygenderword"
        self.genderlist = ["man","woman","father","mother","boy","girl","uncle","aunt","husband","wife",
                           "boyfriend","girlfriend","actor","actress","prince","princess","king","queen","male","female","men","women"]
        self.malelist = [self.genderlist[i] for i in range(len(self.genderlist)) if i%2 == 0]
        print(self.malelist)
        self.femalelist = [self.genderlist[i] for i in range(len(self.genderlist)) if i%2 == 1]
        print(self.femalelist)
        # gender list based on https://www.ef.edu/english-resources/english-grammar/noun-gender/
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
        for index in self.masterlist:
            score = 0
            wordslist = re.findall('[A-Z][^A-Z]*', index)
            wordslist = [x.lower() for x in wordslist]
            print(wordslist)
            for word in wordslist:
                if word in self.genderlist:
                    score += 1
            if score != 0:
                self.G.add_node(index,label=index)
                for itr in self.masterlist[index]:
                    if itr in self.centraltropes:
                        self.G.add_node(itr,label=itr)
                        self.G.add_edge(index, itr)
            else:
                pass
        for trope in self.G.nodes:
            if trope in self.centraltropes:
                for iitr in self.masterlisttropes[trope]:
                    if iitr in self.G.nodes:
                        self.G.add_edge(trope,iitr)
                
            
        print(len(self.G.nodes), len(self.G.edges))
        self.write_gml(self.G, supercat)
        data = [x for x in self.G.edges]
        #print(data)
        self.write_json(data, supercat+"edgelist.json")
        return None
    

i = IndexGraph()
#i.show_graph()

    