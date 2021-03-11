import pymongo
import dns
from pymongo import MongoClient
import os # for using os commands
import setup # importing setup.py allows us to use the os.getenv command for calling the .env file

from flask import Flask, request, json, Response, jsonify
from flask_restful import Api, Resource
from flask_restx import Api, Resource, fields
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

# imports for machine learning
#import pandas as pd
#import numpy as np
#from sklearn import datasets, svm, linear_model
#import pickle

# -------- SETUP -------- #

mongoUrl = os.getenv("MONGO_URL")
localUrl = os.getenv("BASE_URL") # not used
herokuUrl = os.getenv("BASE_URL2") # not used and needs to be changed

client = MongoClient(mongoUrl)

knowledgeGenerator = client["KnowledgeGenerator"]
KGE_Models = knowledgeGenerator["fs.files"]

knowledgeBank = client["KnowledgeBank"]
KB_Models = knowledgeBank["models"]

app = Flask(__name__)
app.config["MONGO_URI"] = mongoUrl
#mongo = PyMongo(flask_app, uri=mongoUrl) Skjønner ikke hva denne brukes til
api = Api(app=app,
            version=0.01,
            title="Knowledge Bank",
            description="Backend for storing and managing machinelearning models in Digital Twins project")

# -------- SETUP DONE -------- #


# -------- METHODS AND ENDPOINTS -------- #

@api.route("/models/<model_name>/")
@api.doc(params={'name': 'Model name'})
class GetModel(Resource):
    def get(self, model_name):
        model = KB_Models.find_one({"name" : model_name})
        if not model:
            exception = pymongo.errors.InvalidName(error_labels=404 ,message="Model with that name could not be found...")
            return exception
        return model
'''
@api.route("/models/")
class GetAllModels(Resource):
    def get_all_models(self):
        models = list(KGE_Models.find())
        return models
'''
# -------- METHODS AND ENDPOINTS DONE -------- #



# -------- RUN APP -------- #

if __name__ == "__main__":
    app.run(debug=True)

'''
test1 = {"_id": 0, "name": "Hypertension", "Description": "Predicts risk of developing hypertension", 
"beta_0": -15.139611, "beta_1": 0.048337, "beta_2": 0.055844, "beta_3": 0.060932}

modelsCollection.insert_one(test1)
'''