import pymongo
from pymongo import MongoClient
import os # for using os commands
import settings # importing settings.py allows us to use the os.getenv command for calling the .env file

from flask import Flask, request, json, Response, jsonify
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

# imports for machine learning
import pandas as pd
import numpy as np
from sklearn import datasets, svm, linear_model
import pickle

# importing url's from .env file
mongoUrl = os.getenv("MONGO_URL")
localUrl = os.getenv("BASE_URL") # not used
herokuUrl = os.getenv("BASE_URL2") # not used and needs to be changed

cluster = MongoClient(mongoUrl)

knowledgeGenerator = cluster["KnowledgeGenerator"]
KGE_Models = knowledgeGenerator["fs.files"]

knowledgeBank = cluster["KnowledgeBank"]
KB_Models = knowledgeBank["models"]

app = Flask(__name__)
app.config["MONGO_URI"] = mongoUrl
mongo = PyMongo(app)
'''
class KBModelsAPI(Resource):
    def __init__(self, collection):
        self.cluster = MongoClient(mongoUrl) # setting the cluster variable
        self.knowledgeBank = cluster["KnowledgeBank"] # setting the database variable
        self.KB_Models = knowledgeBank[collection] # setting collection variables
'''
@app.route("/model/<model_name>/", methods=['GET'])
def get(model_name=str):
    model = KB_Models.find_one({"name" : model_name})
    if not model:
        exception = pymongo.errors.InvalidName(error_labels=404 ,message="Model with that name could not be found...")
        return exception
    return model

def put(self, model_id):
    return None

if __name__ == "__main__":
    app.run(debug=True)









'''
# Logistic regression
logres = linear_model.LogisticRegression(random_state=0)

def save_model_to_db(model, client, database, dbconnection, model_name):
    pickled_model = pickle.dumps(model)
    myClient = pymongo.MongoClient(client)
    mydb = myClient[database]
    mycon = mydb[dbconnection]
    info = mycon.insert_one({model_name: pickled_model, 'name': model_name, 'created_time': time.time()})
    details = {
        'inserted_id':info.inserted_id,
        'model_name':model_name,
        'created_time':time.time()
    }
    return details

def fetch_model_from_db(model_name, client, database, dbconnection):
    json_data = {}
    myClient = pymongo.MongoClient(client)
    mydb = myClient[database]
    mycon = mydb[dbconnection]
    data = mycon.find({'name':model_name})

    for i in data:
        json_data = i
    pickled_model = json_data[model_name]

    return pickle.loads(pickled_model)

# first connection test
test1 = {"_id": 0, "name": "Hypertension", "Description": "Predicts risk of developing hypertension", 
"beta_0": -15.139611, "beta_1": 0.048337, "beta_2": 0.055844, "beta_3": 0.060932, 
"Age": 25, "Systolic": 120, "Diastolic": 75}

modelsCollection.insert_one(test1)'''