# -*- coding:utf-8 -*-
"""
Dec: 爬猫眼热映电影;Use selenium
Created on ； 2017.11.04
Author: Iflier
"""
print(__doc__)

import re
import json
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

SERVICE_ARGS = ['--load-images=false']
url = "http://maoyan.com/films?showType=1"


flag = True
while flag:
    browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    browser.get(url)
    try:
        nextPageAnchor = browser.find_element_by_link_text("下一页")
    except NoSuchElementException:
        break
    nextPageLink = nextPageAnchor.get_attribute("href")
    if re.match(r'^https?', nextPageLink, re.I):
        print("Next Page: {0}".format(nextPageLink))
        url = nextPageLink
        with open("resultFromSelenium.json", 'a', encoding='utf-8') as file:
            # 仅仅是打开它，不用读取，因此不是a+
            file.write(json.dumps(url, ensure_ascii=False) + '\n')
browser.quit()
print("Done.")
