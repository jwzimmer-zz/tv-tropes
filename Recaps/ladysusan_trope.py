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
import seaborn as sns
import pandas as pd

class TropeGraph():
    def __init__(self):
        self.G = nx.Graph()
        self.ladysusantropes = ["WickedStepmother", "BlackSheep", "LoveAtFirstSight", "MarryForLove", "BoardingSchool",
                                "ArrangedMarriage", "EvilPlan", "Sidekick"]
        self.centraltropes = self.get_most_central_tropes_by_all_4_metrics("top_10000_central.json")
        self.masterlist = self.get_json('all-tropes-with-links.json')
        self.scoredict = self.get_json('only_polarized_tokens.json')
        self.scoredict_mild = self.get_json('polarized_tokens.json')
        self.supercat = "ladysusan"
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
        tropelist = []
        i = 0
        for trope in self.ladysusantropes:
            self.G.add_node(trope,label=trope)
            if trope in self.scoredict:
                #print(self.scoredict[trope]['normed mean happiness'])
                whateverlist+=[self.scoredict[trope]['normed mean happiness']]
                tropelist += [trope]
                i += 1
            else:
                print("missing ",trope)
        
        for trope in self.G.nodes:
            if trope in self.masterlist:
                for inde in self.masterlist[trope]:
                    if inde in self.G.nodes:
                        self.G.add_edge(trope, inde)
                
         

        #sns.lineplot(data=df)
        plt.plot(tropelist, whateverlist)
        plt.xticks(rotation=45, ha='right')
        #print(len(self.G.nodes), len(self.G.edges))
        self.write_gml(self.G, supercat)
        
        #self.write_json(whateverlist, supercat+"genderlist.json")
        return None
    

i = TropeGraph()

    