# -*- coding:utf-8 -*-
"""
Dec:
Created on: 2017.11.05
Author: Iflier
"""
print(__doc__)

import json
import threading
from multiprocessing import Queue

import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
}
que = Queue()

with open("resultFromSelenium.json", 'r', encoding='utf-8') as file:
    lines = file.readlines()
for li in lines:
    que.put(li)
print("Read file finished, got {0} urls".format(que.qsize()))

url = json.loads(que.get(), encoding='utf-8')
resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
print(resp.url)
print("Response ok? {0}".format(resp.ok))
soup = BeautifulSoup(resp.text, 'lxml')
dl = soup.select("#app > div > div.movies-panel > div.movies-list > dl")
for dd in dl:
    print(dd.select("div.channel-detail.movie-item-title"))
    print(dd.select("div.channel-detail.channel-detail-orange")[0].string)
print("Length {}".format(len(dd)))
