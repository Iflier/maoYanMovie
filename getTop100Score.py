# -*-coding:utf-8 -*-
"""
Dec:
Created on : 2017.11.05
Author: Iflier
"""
print(__doc__)

import json
import threading
from multiprocessing import Queue

from selenium import webdriver


SERVICE_ARGS = ["--load-images=false"]
que = Queue()

with open("Top100.json", 'r', encoding='utf-8') as file:
    lis = file.readlines()
for li in lis:
    que.put(json.loads(li, encoding='utf-8'))


def store(queobject):
    """
    从队列中get一个url ->提取片名和评分-> 保存到json
    """
    if not queobject.empty():
        url = queobject.get()
        browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        browser.get(url)
        dds = browser.find_elements_by_xpath("//*[@id='app']/div/div/div[1]/dl/dd")
        print("Length of dds: {0}".format(len(dds)))
        lines = list()
        for dd in dds:
            content = dict()
            p = dd.find_element_by_xpath(".//div/div/div[2]/p")
            content["score"] = p.find_element_by_xpath(".//i[1]").text + p.find_element_by_xpath(".//i[last()]").text
            content["filmname"] = dd.find_element_by_xpath(".//div/div//div[1]/p[@class='name']/a").text
            content["releaseTime"] = dd.find_element_by_xpath(".//div/div/div[1]/p[last()]").text
            content["performer"] = dd.find_element_by_xpath(".//div/div/div[1]/p[2]").text
            # print("Performer: {0}".format(content.get("performer")))
            lines.append(json.dumps(content, ensure_ascii=False) + '\n')
        browser.quit()
        lock = threading.Lock()
        lock.acquire()
        with open("top100NameAndScore.json", 'a', encoding='utf-8') as file:
            file.writelines(lines)
        lock.release()
    else:
        pass

for i in range(0, 10, 2):
    thList = list()
    for j in (i, i + 2, 1):
        thList.append(threading.Thread(target=store, args=(que,)))
    for th in thList:
        th.start()
    for th in thList:
        th.join()

print("Done.")
