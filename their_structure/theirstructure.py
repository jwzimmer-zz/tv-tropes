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
        for slist in result:
            combo = combinations(slist,2)
            for c in combo:
                G.add_edge(c[0],c[1])
        nx.write_gml(G, outname+".gml")
        return None
    
    def write_cluster_result_as_graph(self,result,outname):
        G = nx.Graph()
        edgelist = []
        category = "SuperTropes"
        for res in result:
            #print(type(res), res)
            if type(res) is str:
                #print(category,res)
                G.add_edge(category,res)
                edgelist.append((category,res))
            else:
                supertrope = res[0]
                subs = res[1]
                G.add_edge(category,supertrope)
                edgelist.append((category,supertrope))
                for sub in subs:
                    G.add_edge(supertrope,sub)
                    #print(supertrope,sub)
                    edgelist.append((supertrope,sub))
        nx.write_gml(G, outname+".gml")
        #print(edgelist)
        return edgelist
          
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
    
    def get_structure_supertropes(self, filename, name, masterlist):
        supertrope_samples = []
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
                    #print(h2)
                    if h2.text == " A Sample of Super Tropes And Their Sub Tropes":
                        #print(h2)
                        ul = h2.find_next("ul")
                        #print(ul)
                        lis = ul.find_all("li")
                        for li in lis:
                            #print(li)
                            a_s = li.find_all("a")
                            li_links = []
                            for a in a_s:
                                href = a["href"]
                                #print(href)
                                tropename = href.split("/")[-1]
                                li_links.append(tropename)
                            if len(li_links) >= 2:
                                supertrope = li_links[0]
                                subtropes = li_links[1:]
                                subs_in_master = []
                                for sub in subtropes:
                                    if sub in masterlist:
                                        subs_in_master.append(sub)
                                if len(subs_in_master) > 0:
                                    supertrope_samples.append((supertrope,set(subs_in_master)))
                                else:
                                    supertrope_samples.append(supertrope)
                            elif len(li_links) == 1:
                                supertrope = li_links[0]
                                supertrope_samples.append(supertrope)
                            else:
                                pass
                            
        #print(supertrope_samples)        
        return supertrope_samples
    
    
    def go_thru_list_pages(self, maxn):
        i = 0
        self.masterlist = self.get_masterlist()
        
        for filename in os.scandir("their_structure"):
            if filename.name.endswith("htm"):
                #print(filename, self.count, i)
                name  = filename.name
                if i < maxn:
                    #sistertrope_examples = self.get_structure_sistertropes("their_structure/" + name, name, self.masterlist)
                    #self.write_result_as_graph(sistertrope_examples, "sistertropes_inmasterlist")
                    supertrope_samples = self.get_structure_supertropes("their_structure/" + name, name, self.masterlist)
                    if len(supertrope_samples) > 0:
                        self.write_cluster_result_as_graph(supertrope_samples, "supertropes")
                    i+=1
                    self.count+=1
                else: return None
        return None
    
it = TropeLists()
it.go_thru_list_pages(10)
# for i in range(200):
#     it.go_thru_list_pages(500)


    