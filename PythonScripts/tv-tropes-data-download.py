#!/usr/bin/env python

# # Make giant dict to analyze - run in main directory

from bs4 import BeautifulSoup
import requests
import os
import json

# change dir

os.chdir('trope_list/tropes')
trope_list = os.listdir()

d = {}

for trope in trope_list[]:
    p = open(trope)
    cur_index = 0
    str_trope = trope.split(".")[0]
    soup = BeautifulSoup(p, "html")
    d[str_trope] = {}
    links = []
    trope_links = [a for a in soup.find("div", id="main-article").find_all("a")]
    for i in np.arange(len(trope_links)):
        if trope_links[i].has_attr('href'):
            if trope_links[i]["href"].split("/")[-1]+".html" in trope_list:
                links.append(trope_links[i]["href"].split("/")[-1])
        else:
            pass
    d[str_trope] = links
    cur_index += 1

out_file = open("myfile.json", "w")
  
json.dump(d, out_file, indent = 6)
  
out_file.close()
