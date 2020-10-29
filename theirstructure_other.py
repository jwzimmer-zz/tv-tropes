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
        category = "TropeTropes"
        for res in result:
            G.add_edge(category,res[0])
            edgelist.append((category,res[0]))
            if len(res) > 1:
                tropetrope = res[0]
                subs = res[1:]
                for sub in subs:
                    G.add_edge(tropetrope,sub)
                    edgelist.append((tropetrope,sub))
        nx.write_gml(G, outname+".gml")
        print(list(set(edgelist)))
        return edgelist
          
    def get_masterlist(self):
        with open('in_Masterlist.json') as f:
            masterlist = json.load(f)
        return masterlist
    
    def get_structure_tropetropes(self, filename, name, masterlist):
        trope_tropes = [['AvertedTrope'], ['BaitAndSwitch'], ['CharacteristicTrope'], ['ConversationalTroping'], ['CyclicTrope'], ['DeadHorseTrope'], ['DeadUnicornTrope', 'DeadHorseTrope'], ['DeconstructedTrope'], ['DefiedTrope'], ['DiscreditedTrope'], ['DiscussedTrope'], ['DoubleSubversion'], ['DownplayedTrope'], ['EnforcedTrope', 'MoralGuardians'], ['EverythingsWorseWithSnowclones'], ['EvolvingTrope'], ['ExaggeratedTrope'], ['ExploitedTrope'], ['ForgottenTrope'], ['GenderInvertedTrope'], ['ImpliedTrope'], ['IntendedAudienceReaction', 'AudienceReaction'], ['InvertedTrope'], ['InvokedTrope'], ['JustifiedTrope'], ['LampshadeHanging'], ['LogicalExtreme'], ['NecessaryWeasel'], ['NewerThanTheyThink'], ['NotADeconstruction'], ['NotASubversion'], ['OlderThanTheyThink'], ['OmnipresentTropes'], ['OverdosedTropes'], ['ParodiedTrope'], ['PetPeeveTrope'], ['PlayedForDrama'], ['PlayedForHorror', 'NightmareFuel'], ['PlayedForLaughs'], ['PlayingWithATrope'], ['SisterTrope'], ['SpoileredRotten'], ['SquarePegRoundTrope', 'TropeDecay'], ['SubTrope'], ['SubvertedTrope'], ['SuperTrope'], ['Trope'], ['TropeBreaker'], ['TropeDecay'], ['TropeEnjoymentLoophole', 'PetPeeveTrope'], ['TropeGrid'], ['Troperiffic'], ['TropersBlock'], ['TropeNamerSyndrome'], ['TropesAreFlexible'], ['TropesAreTools'], ['TropesInAggregate'], ['TropeTelegraphing'], ['UndeadHorseTrope', 'DeadHorseTrope'], ['UnbuiltTrope'], ['ZigZaggingTrope']]
        return trope_tropes
    
    def go_thru_list_pages(self, maxn):
        i = 0
        self.masterlist = self.get_masterlist()
        
        for filename in os.scandir("their_structure"):
            if filename.name.endswith("htm"):
                #print(filename, self.count, i)
                name  = filename.name
                if i < maxn:
                    trope_tropes = self.get_structure_tropetropes("their_structure/" + name, name, self.masterlist)
                    if len(trope_tropes) > 1:
                        self.write_cluster_result_as_graph(trope_tropes, "tropetropes")
                    i+=1
                    self.count+=1
                else: return None
        return None
    
it = TropeLists()
it.go_thru_list_pages(10)
# for i in range(200):
#     it.go_thru_list_pages(500)


    