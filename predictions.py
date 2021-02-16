import pymongo
from pymongo import MongoClient
import os
import settings

mongoUrl = os.getenv("MONGO_URL")

cluster = MongoClient(mongoUrl)
db = cluster["KnowledgeBank"]
modelsCollection = db["models"]

models = modelsCollection.find({"name": "Hypertension"})

for model in models:
    print(model)