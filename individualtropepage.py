#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 2020

@author: jzimmer1, philnguyen
"""

from bs4 import BeautifulSoup
import re
import pickle
import os
import pandas as pd
import json

class TropePage():
    def __init__(self):
        pass
        self.filename = ''
        self.urdict = {}
    def get_lists_tropes(self, filename):
        # this looks like it works for most of the trope list pages, assuming
        # they are similar to each other - i did not check that for all pages this works for,
        # the structure is actually the same as the example page (Indices/Genre Tropes - TV Tropes.htm)
        
        self.filename = filename
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        structure_dict = {}
        linkedtropes = []
        mydivs = soup.find_all("div", class_="article-content retro-folders")
        if len(mydivs) == 0:
            print("different structure: ",filename)
            #structure_dict = self.handle(filename)
        else:
            for div in mydivs:
                allps = div.find_all("p")
                for p in allps:
                    alllinks = p.find_all("a")
                    for link in alllinks:
                        href = link["href"]
                        if "Main" in href:
                            linkedtropes.append(href.split("/")[-1])
                        else:
                            #print(href)
                            pass
                #print(filename)
            self.newname = filename.name.split(".")[0]
            structure_dict[self.newname] = linkedtropes
        #print(soup.prettify)
        #print(structure_dict)
        self.urdict = structure_dict
        return structure_dict
    
    def write_dict_as_string(self, dict1):
        with open("linked_trope_dict_from_"+self.newname+".json","w") as outfile:
            json.dump(dict1, outfile)
        return None
        
    def get_df(self):
        self.dictdf = pd.DataFrame.from_dict(self.urdict)
    
            
    def go_thru_list_pages(self,foldername, maxn):
        i = 0
        while i < maxn:
            for entry in os.scandir(foldername):
                
                if entry.path.endswith(".html") and i < maxn:
                    if entry.path.split("/")[-1].startswith("Z"):
                        print(entry.path)
                        dict1 = self.get_lists_tropes(entry)
                        #print(dict1)
                        self.write_dict_as_string(dict1)
                    i+=1
                else: return None
        return None
    
it = TropePage()
it.go_thru_list_pages("trope_list/tropes", 30000)
    