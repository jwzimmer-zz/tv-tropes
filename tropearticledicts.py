#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 2020

@author: jzimmer1, philnguyen
"""

from bs4 import BeautifulSoup
import os
import json

class TropeLists():
    def __init__(self):
        self.count = 0
        self.filename = ''
        self.urdict = {}
    def get_trope_name(self, filename):
        self.filename = filename.split("/")[-1]
        self.newname = self.filename.split(".")[0]
        return self.newname 
    
    def write_dict_as_string(self, dict1, name):
        with open("linked_article_tropes/linked_trope_dict_from_"+name+".json","w") as outfile:
            json.dump(dict1, outfile)
        return None
          
    def go_thru_masterlist_folder_pages(self,foldername):
        self.alltropes = os.listdir(foldername)
        self.namesonly = [self.get_trope_name(entry) for entry in self.alltropes]
        # with open("in_Masterlist.json","w") as outfile:
        #     json.dump(self.namesonly, outfile)
        return self.namesonly
    
    def go_thru_Main_folder_pages(self,foldername):
        self.allmain = os.listdir(foldername)
        self.mainnamesonly = [self.get_trope_name(entry) for entry in self.allmain]
        # with open("in_pmwiki_Main.json","w") as outfile:
        #     json.dump(self.mainnamesonly, outfile)
        return self.mainnamesonly
    
    def get_dicts_tropes(self, filename, name, masterlist):
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
                            name1 = href.split("/")[-1]
                            #if ("Main" in href) or (name1 in masterlist):
                            if (name1 in masterlist):
                                if name1 != name:
                                    linkedtropes.append(name1)
                                else:
                                    #print("Skipping duplicates ",name1,name)
                                    pass
                            else:
                                #print("Skipping href ",href)
                                pass
                        except:
                            idtag = link["id"]
                            linkedtropes.append(idtag)
                for ul in uls:
                    allullinks = ul.find_all("a")
                    for link2 in allullinks:
                        try:
                            href2 = link2["href"]
                            name2 = href2.split("/")[-1]
                            #if ("Main" in href2) or (name2 in masterlist):
                            if (name2 in masterlist):
                                if name2 != name:
                                    linkedtropes.append(href2.split("/")[-1])
                                else:
                                    #print("Skipping duplicates ",name2,name)
                                    pass
                            else:
                                #print("Not including: ",href2)
                                pass
                        except:
                            idtag2 = link2["id"]
                            linkedtropes.append(idtag2)
                #print(filename)
            self.newname = self.filename.split(".")[0]
            structure_dict[self.newname] = linkedtropes

        #self.write_dict_as_string(structure_dict, name)
        return structure_dict
    
    
    def go_thru_list_pages(self, maxn):
        i = 0
        self.alltropes = os.listdir("trope_list/tropes")
        self.mainnamesonly = self.go_thru_Main_folder_pages("tvtropes.org/pmwiki/pmwiki.php/Main")
        self.namesonly = self.go_thru_masterlist_folder_pages("trope_list/tropes")
        self.masterlist = self.mainnamesonly + self.namesonly
        
        for filename in self.alltropes[self.count:self.count+maxn]:
            #print(filename, self.count, i)
            name  = self.get_trope_name(filename)
            if self.namesonly[self.count] == name:
                if i < maxn:
                    dict1 = self.get_dicts_tropes("trope_list/tropes/"+filename, name, self.masterlist)
                    self.write_dict_as_string(dict1, name)
                    i+=1
                    self.count+=1
                else: return None
            else:
                print("help ",filename,self.count,self.namesonly[self.count],i)
        return None
    
it = TropeLists()
for i in range(10):
    it.go_thru_list_pages(20)


    