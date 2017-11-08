# -*- coding:utf-8 -*-
"""
Dec: 根据getMaoYanHotMoviesPage.py爬取的页面链接，检索出对应页面上的影片名称和评分
Created on : 2017.11.05
Author: Iflier
"""
print(__doc__)

import time
import json
import random
import threading
from multiprocessing import Queue

from selenium import webdriver


que = Queue()
with open("resultFromSelenium.json", 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if(line):
            que.put(line)
        else:
            break
print("Read file finished. Got {0} urls".format(que.qsize()))

def store(queobject):
    """
    从一个队列中获取页面链接->获取影片名称和评分->写入json文件
    """
    if not queobject.empty():
        url = json.loads(que.get(), encoding='utf-8')
        print("Fetching url: {}".format(url))
        browser = webdriver.PhantomJS()
        browser.get(url)
        time.sleep(random.uniform(5, 15))
        dds = browser.find_elements_by_xpath("//*[@id='app']/div/div[2]/div[2]/dl/dd")
        print("Length of dds: {0}".format(len(dds)))
        lines = list()
        for dd in dds:
            nameAndScore = dict()
            filmname = dd.find_element_by_xpath(".//div[@title]/a").text
            iLength = len(dd.find_elements_by_xpath(".//div[3]/i"))
            if iLength == 2:
                score = dd.find_element_by_xpath(".//div[3]/i[1]").text + dd.find_element_by_xpath(".//div[3]/i[last()]").text
            elif iLength == 0:
                score = None
            else:
                print("[INFO] Bad url: {0}".format(url))
                score = None
            nameAndScore["filmname"] = filmname
            nameAndScore["score"] = score
            lines.append(json.dumps(nameAndScore, ensure_ascii=False) + '\n')
            print("Name And Score: {0}".format(nameAndScore))
        browser.quit()
        lock = threading.Lock()
        lock.acquire()
        with open("nameAndScoreWithSelenium.json", 'a', encoding='utf-8') as file:
            file.writelines(lines)
        lock.release()
    else:
        pass

for i in range(0, 100, 4):
    thList = list()
    for j in range(i, i + 4, 1):
        thList.append(threading.Thread(target=store, args=(que,)))
    for th in thList:
        th.start()
    for th in thList:
        th.join()
