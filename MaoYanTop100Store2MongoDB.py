# -*- coding:utf-8 -*-
"""
Dec:
Created on : 2017.11.05
Author: Iflier
"""
print(__doc__)

import sys
import json

from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

# ***********
# 手动注释掉
# **********
sys.exit(0)

client = MongoClient(host="localhost", port=27017)
db = client["maoyanmovie"]
collection = db["top100"]

with open("top100NameAndScore.json", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        result = dict()
        content = json.loads(line, encoding='utf-8')
        result["filmname"] = content.get("filmname")
        result["releasetime"] = content.get("releaseTime")[5: 15]
        result["score"] = float(content.get("score"))
        result["performer"] = content.get("performer")[3:]
        stored = collection.insert_one(result)
        # print("ID: {0}".format(stored.inserted_id))
        # print("Acknowledged?{0}".format(stored.acknowledged))

collection.create_index([("score", ASCENDING)])
print("Done.")
