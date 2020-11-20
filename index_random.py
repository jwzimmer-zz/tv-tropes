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
import pandas as pd

class IndexGraph_Random():
    def __init__(self):
        self.graphlist, self.df = self.get_random_gmls(100, 'Random-4-Indices')
    
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
    
    def analysis(self, G):
        df = {}
        df["NumberNodes"]=len(G.nodes)
        df["NumberEdges"]=len(G.edges)
        df["NumberIsolates"] = nx.algorithms.number_of_isolates(G)
        df["IsEulerian"] = nx.algorithms.is_eulerian(G)
        df["GlobalEfficiency"] = nx.algorithms.global_efficiency(G)
        
        try:
            df["Diameter"] = nx.algorithms.diameter(G)
            df["Radius"] = nx.algorithms.radius(G)
            df["NodeConnectivity"] = nx.algorithms.node_connectivity(G)
        except:
            pass
        
        return pd.Series(df)
        
    
    def get_random_gmls(self,k,folder):
        graphlist = []
        df = pd.DataFrame()
        i = 0
        while i <= k:
            for entry in os.scandir(folder):
                if entry.name.endswith(".gml"):
                    G = nx.read_gml(folder+"/"+entry.name)
                    graphlist.append(G)
                    name = entry.name[:-4]
                    df[name] = self.analysis(G)
                if i > k:
                    break
                i += 1
        df.to_csv("4RandomIndVsBgFour.csv")
        return graphlist, df

i = IndexGraph_Random()
print(i.df)