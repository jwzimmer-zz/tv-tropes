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

class TropeGraph():
    def __init__(self):
        self.G = nx.Graph()
        self.centraltropes = self.get_most_central_tropes_by_all_4_metrics("top_10000_central.json")
        self.masterlist = self.get_json('all-tropes-with-links.json')
        self.supercat = "gender_alwaysfemale"
        self.genderlist = ["man","woman","father","mother","boy","girl","uncle","aunt","husband","wife",
                           "boyfriend","girlfriend","prince","princess","king","queen","male","female","men","women"]
        self.malelist = [self.genderlist[i] for i in range(len(self.genderlist)) if i%2 == 0]
        self.femalelist = [self.genderlist[i] for i in range(len(self.genderlist)) if i%2 == 1]
        # gender list based on https://www.ef.edu/english-resources/english-grammar/noun-gender/
        self.add_trope_nodes()
    
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
        whateverlist = []
        #self.G.add_node(supercat,label=supercat)
        gendertitles = ["AlwaysMale","AlwaysFemale"]
        male=gendertitles[0]
        female="AlwaysFemale"
        
        # for trope in self.masterlist[male]:
        #     #if trope in self.centraltropes:
        #     self.G.add_edge(male, trope)
        for trope in self.masterlist[female]:
            self.G.add_edge(female, trope)
        
        for trope in self.G.nodes:
            whateverlist.append(trope)
            if trope in self.masterlist:
                for inde in self.masterlist[trope]:
                    if inde in self.G.nodes:
                        self.G.add_edge(trope, inde)
                        whateverlist.append(inde)
                
            
        print(len(self.G.nodes), len(self.G.edges))
        self.write_gml(self.G, supercat)
        
        self.write_json(whateverlist, supercat+"genderlist.json")
        return None
    

i = TropeGraph()
#i.show_graph()

    