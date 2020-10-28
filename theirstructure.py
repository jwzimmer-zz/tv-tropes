#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 2020

@author: jzimmer1, philnguyen
"""

from bs4 import BeautifulSoup
import os
import json
import networkx as nx
from itertools import combinations

class TropeLists():
    def __init__(self):
        self.count = 0
        self.filename = ''
        self.urdict = {}
    def get_trope_name(self, filename):
        self.filename = filename.split("/")[-1]
        self.newname = self.filename.split(".")[0]
        return self.newname 
    
    def write_result_as_graph(self, result, outname):
        G = nx.Graph()
        for sisterlist in result:
            combo = combinations(sisterlist,2)
            for c in combo:
                G.add_edge(c[0],c[1])
        nx.write_gml(G, outname+".gml")
        return None
          
    def get_masterlist(self):
        with open('in_Masterlist.json') as f:
            masterlist = json.load(f)
        return masterlist
    
    def get_structure_sistertropes(self, filename, name, masterlist):
        sistertrope_examples = []
        self.filename = filename.split("/")[-1]
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        structure_dict = {}
        linkedtropes = []
        mydivs = soup.find_all("div", class_="article-content retro-folders")
        if len(mydivs) == 0:
            print("different structure: ",self.filename)
            #structure_dict = self.handle(filename)
        else:
            for div in mydivs:
                h2s = div.find_all("h2")
                for h2 in h2s:
                    if h2.text == "Examples:":
                        ul = h2.find_next("ul")
                        lis = ul.find_all("li")
                        for li in lis:
                            a_s = li.find_all("a")
                            li_links = []
                            for a in a_s:
                                href = a["href"]
                                tropename = href.split("/")[-1]
                                if tropename in masterlist:
                                    li_links.append(tropename)
                            sistertrope_examples.append(set(li_links))
        #print(sistertrope_examples)        
        return sistertrope_examples
    
    
    def go_thru_list_pages(self, maxn):
        i = 0
        self.masterlist = self.get_masterlist()
        
        for filename in os.scandir("their_structure"):
            if filename.name.endswith("htm"):
                #print(filename, self.count, i)
                name  = filename.name
                if i < maxn:
                    sistertrope_examples = self.get_structure_sistertropes("their_structure/" + name, name, self.masterlist)
                    self.write_result_as_graph(sistertrope_examples, "sistertropes_inmasterlist")
                    i+=1
                    self.count+=1
                else: return None
        return None
    
it = TropeLists()
it.go_thru_list_pages(10)
# for i in range(200):
#     it.go_thru_list_pages(500)


    