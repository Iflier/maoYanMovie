# -*- coding:utf-8 -*-
"""
Dec:
Created on : 2017.11.05
Author: Iflier
"""
print(__doc__)

import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

url = "http://maoyan.com/board/4"
SERVICE_ARGS = ["--load-images=false"]

with open("Top100.json", 'a', encoding='utf-8') as file:
    file.write(json.dumps(url, ensure_ascii=False) + '\n')

while True:
    browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    browser.get(url)
    try:
        nextLinkAnchor = browser.find_element_by_link_text("下一页")
        nextLink = nextLinkAnchor.get_attribute("href")
        url = nextLink
        with open("Top100.json", 'a', encoding='utf-8') as file:
            file.write(json.dumps(url, ensure_ascii=False) + '\n')
    except NoSuchElementException:
        browser.quit()
        break
