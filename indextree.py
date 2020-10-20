#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:22:25 2020

@author: jzimmer1, philnguyen
"""

from bs4 import BeautifulSoup
import re
import pickle

#this is the dictionary this script outputs:
# =============================================================================
# 
# {' Sub-indexes:': ['Action/Adventure Tropes', 'Advertising Tropes', 'Alternate History Tropes', 'Comedy Tropes', 'Recorded and Stand-Up Comedy', 'Crime and Punishment Tropes', 'Drama Tropes', 'Espionage Tropes', 'Fairy Tale Tropes', 'Game Show Tropes', 'Genre Title Grab Bag', 'Horror Tropes', 'Love Tropes', 'Military and Warfare Tropes', 'Mystery Tropes', 'News Broadcast', 'News Tropes', 'Ninja Tropes', 'Opera', 'Picaresque', 'Pirate Tropes', 'Post-9/11 Terrorism Movie', 'Professional Wrestling', 'Reality TV Tropes', 'Romance Novel Tropes', 'Speculative Fiction Tropes', 'Sports Story Tropes', 'Superhero Tropes', 'Thriller', 'Tragedy', 'Tokusatsu Tropes', 'Wild West Tropes'], ' Tropes related directly to Genres:': ['Contractual Genre Blindness', 'Death by Genre Savviness', 'From Clones to Genre', 'Functional Genre Savvy', 'Gameplay Roulette', 'Genre Adultery', 'Genre Blindness', 'Genre-Busting', 'Genre Deconstruction', 'Genre-Killer', 'Genre Mashup', 'Genre Motif', 'Genre Refugee', 'Genre Relaunch', 'Genre Roulette', 'Genre Savvy', 'Genre Shift', 'Genre Throwback', 'Genre Turning Point', 'Heavy Meta', 'Out-of-Genre Experience', 'Reality Show Genre Blindness', 'Sliding Scale of Comedy and Horror', 'Unexpected Gameplay Change', 'The Universal Genre Savvy Guide', 'Wrong Genre Savvy']}
# 
# =============================================================================

class IndexTree():
    def __init__(self):
        pass
        self.filename = ''
        self.urdict = {}
    def get_lists_tropes(self, filename):
        self.filename = filename
        soup = BeautifulSoup(open(filename),features="lxml")
        # links = soup.find_all(['h2','a'])
        # #looks like the lists of tropes are organized alphabetically,
        # #so we could look at entries starting with A-Z?
        # linktxt = [x.text for x in links]
        structure_dict = {}
        headerlinks = soup.find_all("h2")
        for headerlink in headerlinks:
            nextul = headerlink.find_next("ul")
            innertropes = nextul.find_all("a")
            innertext = [x.text for x in innertropes]
            structure_dict[headerlink.text]=innertext
        self.urdict = structure_dict
        return structure_dict
    def write_dict(self):
        try:
            self.newname = self.filename.split("/")[-1]
        except:
            self.newname = self.filename
        with open("dict_from_"+self.newname+".pickle", 'wb') as outfile:
            pickle.dump(self.urdict, outfile, protocol=pickle.HIGHEST_PROTOCOL)
        return None

it = IndexTree()
#print(it.get_lists_tropes("Indices/Genre Tropes - TV Tropes.htm"))
it.write_dict()
    