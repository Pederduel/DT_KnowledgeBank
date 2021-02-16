import pymongo
from pymongo import MongoClient
import os # for using os commands
import settings # importing settings.py allows us to use the os.getenv command for calling the .env file

# importing database url from .env file
mongoUrl = os.getenv("MONGO_URL")

# setting the cluster variable
cluster = MongoClient(mongoUrl)

# setting the database variable
db = cluster["KnowledgeBank"]

# setting collection variables
modelsCollection = db["models"]

# first connection test
'''test1 = {"_id": 0, "name": "Hypertension", "Description": "Predicts risk of developing hypertension", 
"beta_0": -15.139611, "beta_1": 0.048337, "beta_2": 0.055844, "beta_3": 0.060932, 
"Age": 25, "Systolic": 120, "Diastolic": 75}

modelsCollection.insert_one(test1)'''