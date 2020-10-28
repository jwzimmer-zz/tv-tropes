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
        self.count = 0
        self.filename = ''
        self.urdict = {}
    def get_lists_tropes(self, filename):
        # this looks like it works for most of the trope list pages, assuming
        # they are similar to each other - i did not check that for all pages this works for,
        # the structure is actually the same as the example page (Indices/Genre Tropes - TV Tropes.htm)
        
        self.filename = filename.split("/")[-1]
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        structure_dict = {}
        linkedtropes = []
        mydivs = soup.find_all("div", class_="article-content retro-folders")
        #print(soup.prettify)
        if len(mydivs) == 0:
            print("different structure: ",self.filename)
            #structure_dict = self.handle(filename)
        else:
            for div in mydivs:
                allps = div.find_all("p")
                uls = div.find_all("ul")
                #print(uls)
                for p in allps:
                    alllinks = p.find_all("a")
                    #print(alllinks)
                    for link in alllinks:
                        try:
                            href = link["href"]
                            if "Main" in href:
                                linkedtropes.append(href.split("/")[-1])
                            else:
                                #print(href)
                                pass
                        except:
                            idtag = link["id"]
                            linkedtropes.append(idtag)
                for ul in uls:
                    allullinks = ul.find_all("a")
                    for link2 in allullinks:
                        try:
                            href2 = link2["href"]
                            if "Main" in href2:
                                linkedtropes.append(href2.split("/")[-1])
                            else:
                                #print(href)
                                pass
                        except:
                            idtag2 = link2["id"]
                            linkedtropes.append(idtag2)
                #print(filename)
            self.newname = self.filename.split(".")[0]
            structure_dict[self.newname] = linkedtropes

        self.write_dict_as_string(structure_dict)
        self.urdict = structure_dict
        return structure_dict
    
    def write_dict_as_string(self, dict1):
        with open("linked_article_tropes/linked_trope_dict_from_"+self.newname+".json","w") as outfile:
            json.dump(dict1, outfile)
        return None
        
    def get_df(self):
        self.dictdf = pd.DataFrame.from_dict(self.urdict)
    
            
    def go_thru_list_pages(self,foldername, maxn):
        i = 0
        self.alltropes = os.listdir(foldername)
        for filename in self.alltropes[self.count:self.count+maxn]:
            print(filename, self.count, i)
            if i < maxn:
                dict1 = self.get_lists_tropes(foldername+"/"+filename)
                self.write_dict_as_string(dict1)
                i+=1
                self.count+=1
            else: return None
        return None
    
it = TropePage()
#it.get_lists_tropes("trope_list/tropes/AbsentAliens.html")

for i in range(10):
    it.go_thru_list_pages("trope_list/tropes", 500)
    