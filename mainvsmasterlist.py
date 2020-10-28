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
    
    def write_result_as_string(self, list1):
        with open("in_Main_not_in_Masterlist.json","w") as outfile:
            json.dump(list1, outfile)
        return None     
          
    def go_thru_masterlist_folder_pages(self,foldername):
        self.alltropes = os.listdir(foldername)
        self.namesonly = [self.get_trope_name(entry) for entry in self.alltropes]
        with open("in_Masterlist.json","w") as outfile:
            json.dump(self.namesonly, outfile)
        return None
    
    def go_thru_Main_folder_pages(self,foldername):
        self.allmain = os.listdir(foldername)
        self.mainnamesonly = [self.get_trope_name(entry) for entry in self.allmain]
        with open("in_pmwiki_Main.json","w") as outfile:
            json.dump(self.mainnamesonly, outfile)
        return None
    
it = TropeLists()
#it.get_lists_tropes("trope_list/tropes/AbsentAliens.html")

#it.go_thru_masterlist_folder_pages("trope_list/tropes")
it.go_thru_Main_folder_pages("tvtropes.org/pmwiki/pmwiki.php/Main")
    